import argparse
import ast
import datetime
import json
import os
import re
import sys
import time

import pdb

import prompts_factory
from config import load_config
from and_controller import list_all_devices, AndroidController, traverse_tree
from model import parse_explore_rsp, parse_reflect_rsp, OpenAIModel, QwenModel
from utils import print_with_color, draw_bbox_multi


arg_desc = "AppAgent - Autonomous Exploration"
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=arg_desc)
parser.add_argument("--app")
parser.add_argument("--task", default="")
parser.add_argument("--root_dir", default="./")
parser.add_argument("--prompt_style", default="sequential")
parser.add_argument("--test_name", default="")
parser.add_argument("--test_setting", default="naive")
args = vars(parser.parse_args())

configs = load_config()

if configs["MODEL"] == "OpenAI":
    mllm = OpenAIModel(base_url=configs["OPENAI_API_BASE"],
                       api_key=configs["OPENAI_API_KEY"],
                       model=configs["OPENAI_API_MODEL"],
                       temperature=configs["TEMPERATURE"],
                       max_tokens=configs["MAX_TOKENS"])
elif configs["MODEL"] == "Qwen":
    mllm = QwenModel(api_key=configs["DASHSCOPE_API_KEY"],
                     model=configs["QWEN_MODEL"])
else:
    print_with_color(f"ERROR: Unsupported model type {configs['MODEL']}!", "red")
    sys.exit()

app = args["app"].replace("-", "")
task = args["task"].replace("-", " ")
root_dir = args["root_dir"]
prompt_style = args["prompt_style"]
test_name = args["test_name"]
test_setting = args["test_setting"]


if not app:
    print_with_color("What is the name of the target app?", "blue")
    app = input()
    app = app.replace(" ", "")

work_dir = os.path.join(root_dir, "apps")
if not os.path.exists(work_dir):
    os.mkdir(work_dir)

work_dir = os.path.join(work_dir, app)
if not os.path.exists(work_dir):
    os.mkdir(work_dir)
demo_dir = os.path.join(work_dir, "demos")
if not os.path.exists(demo_dir):
    os.mkdir(demo_dir)
demo_timestamp = int(time.time())
task_name = datetime.datetime.fromtimestamp(demo_timestamp).strftime("self_explore_%Y-%m-%d_%H-%M-%S")

if test_name:
    test_log_dir = os.path.join(root_dir, 'test_logs', f'test_setting_{test_setting}', test_name.split('.')[0])
    if not os.path.exists(test_log_dir):
        os.mkdir(test_log_dir)

task_dir = os.path.join(demo_dir, task_name)
os.mkdir(task_dir)
docs_dir = os.path.join(work_dir, "auto_docs")
if not os.path.exists(docs_dir):
    os.mkdir(docs_dir)
explore_log_path = os.path.join(task_dir, f"log_explore_{task_name}.json")

device_list = list_all_devices()
if not device_list:
    print_with_color("ERROR: No device found!", "red")
    sys.exit()
print_with_color(f"List of devices attached:\n{str(device_list)}", "yellow")
if len(device_list) == 1:
    device = device_list[0]
    print_with_color(f"Device selected: {device}", "yellow")
else:
    print_with_color("Please choose the Android device to start demo by entering its ID:", "blue")
    device = input()
controller = AndroidController(device)
width, height = controller.get_device_size()
if not width and not height:
    print_with_color("ERROR: Invalid device size!", "red")
    sys.exit()
print_with_color(f"Screen resolution of {device}: {width}x{height}", "yellow")

if not task:
    print_with_color("Please enter the description of the task you want me to complete in a few sentences:", "blue")
    task_desc = input()
else:
    task_desc = task
    print_with_color(f"Task description: {task_desc} | App: {app}", "blue")


round_count = 0
useless_list = set()
last_act = "None"
task_complete = False
user_interaction = "None"
log_item = {}
image_list = []

if test_name:
    test_log = {
        "app": app,
        "task": task_desc,
        "rounds": 0,
        "actions_seq": [],
        "question_sets": {},
        "complete": False,
        "log_path": "",
        "result_image": ""
    }
    

system_prompt = prompts_factory.get_system_prompt(task_desc, app)
    
while round_count < configs["MAX_ROUNDS"]:
    round_count += 1
    print_with_color(f"< Round {round_count} >", "red")
    screenshot_before = controller.get_screenshot(f"{round_count}", task_dir, resized_percent=50)
    xml_path = controller.get_xml(f"{round_count}", task_dir)
    if screenshot_before == "ERROR" or xml_path == "ERROR":
        break
    if test_setting != "naive":
        clickable_list = []
        focusable_list = []
        traverse_tree(xml_path, clickable_list, "clickable", True)
        traverse_tree(xml_path, focusable_list, "focusable", True)
        elem_list = []
        for elem in clickable_list:
            if elem.uid in useless_list:
                continue
            elem_list.append(elem)
        for elem in focusable_list:
            if elem.uid in useless_list:
                continue
            bbox = elem.bbox
            center = (bbox[0][0] + bbox[1][0]) // 2, (bbox[0][1] + bbox[1][1]) // 2
            close = False
            for e in clickable_list:
                bbox = e.bbox
                center_ = (bbox[0][0] + bbox[1][0]) // 2, (bbox[0][1] + bbox[1][1]) // 2
                dist = (abs(center[0] - center_[0]) ** 2 + abs(center[1] - center_[1]) ** 2) ** 0.5
                if dist <= configs["MIN_DIST"]:
                    close = True
                    break
            if not close:
                elem_list.append(elem)
        draw_bbox_multi(screenshot_before, os.path.join(task_dir, f"{round_count}_labeled.png"), elem_list,
                        dark_mode=configs["DARK_MODE"])
        base64_img_before = os.path.join(task_dir, f"{round_count}_labeled.png")
    else:
        base64_img_before = os.path.join(task_dir, f"{round_count}.png")
        
    prompt, image_list = prompts_factory.get_prompts(prompt_style, "decision", last_act, user_interaction, base64_img_before)
    print_with_color(f"Images: {', '.join(image_list)}", "blue")
    
    """ First: Q or A """
    print_with_color("[Step 1] Q/A ->", "red")
    status, rsp = mllm.get_model_response(system_prompt, prompt, image_list)
    assert status, f"Error: {rsp}"
    
    res, log_dict = parse_explore_rsp(rsp)
    act_name = res[0]
    # last_act = res[-1]
    res = res[:-1]
    log_item[round_count]= {
        "Decision": {
            "action": act_name, 
            "response": log_dict, 
            "last_act": last_act,
            "image": f"{round_count}_before_labeled.png",
            "prompt": prompt
        }
    }
       
    if act_name == "FINISH":
        task_complete = True
        if test_name:
            test_log["complete"] = True
            test_log["rounds"] = round_count
        break
    
    """ Sceond: if Q, what Q?"""
    if act_name == "QUESTION":
        prompt, image_list = prompts_factory.get_prompts(prompt_style, act_name, last_act, user_interaction, base64_img_before) 
        print_with_color("[Step 1.5] Q ->", "red")
        status, rsp = mllm.get_model_response(system_prompt, prompt, image_list)
        
        res, log_dict = parse_explore_rsp(rsp)
        act_name = res[0]
        last_act = res[-1]
        res = res[:-1]
        log_item[round_count]["Question"] = {
            "action": act_name, 
            "response": log_dict, 
            "last_act": last_act,
            "image": f"{round_count}_before_labeled.png",
            "prompt": prompt
        }
        
        print_with_color(f"{act_name} question: {res}", "green")    
        test_log["actions_seq"].append(act_name)
        if test_name:
            test_log["question_sets"][res[-1]] = base64_img_before.replace("\\", "/")
        act_name = "ACTION"

    
    """ Third: A """
    prompt, image_list = prompts_factory.get_prompts(prompt_style, act_name, last_act, user_interaction, base64_img_before)    
    print_with_color("[Step 2] A ->", "red")
    status, rsp = mllm.get_model_response(system_prompt, prompt, image_list)
    assert status, f"Error: {rsp}"
        
    res, log_dict = parse_explore_rsp(rsp)
    act_name = res[0]
    last_act = res[-1]
    res = res[:-1]
    # round_count += 1
    log_item[round_count]["Action"] = { 
        "action": act_name, 
        "response": log_dict, 
        "last_act": last_act,
        "image": f"{round_count}_before_labeled.png",
        "prompt": prompt, 
    }
    
    
    ### Process all function calls   
    try:
        if act_name == "FINISH":
            task_complete = True
            if test_name:
                test_log["complete"] = True
                test_log["rounds"] = round_count
            break
        if act_name == "tap":
            _, area = res
            tl, br = elem_list[area - 1].bbox
            x, y = (tl[0] + br[0]) // 2, (tl[1] + br[1]) // 2
            ret = controller.tap(x, y)
            if ret == "ERROR":
                print_with_color("ERROR: tap execution failed", "red")
                break
        elif act_name == "text":
            _, input_str = res
            ret = controller.text(input_str)
            if ret == "ERROR":
                print_with_color("ERROR: text execution failed", "red")
                break
            ret = controller.enter()
            if ret == "ERROR":
                print_with_color("ERROR: enter execution failed", "red")
                break
        elif act_name == "long_press":
            _, area = res
            tl, br = elem_list[area - 1].bbox
            x, y = (tl[0] + br[0]) // 2, (tl[1] + br[1]) // 2
            ret = controller.long_press(x, y)
            if ret == "ERROR":
                print_with_color("ERROR: long press execution failed", "red")
                break
        elif act_name == "swipe":
            _, area, swipe_dir, dist = res
            tl, br = elem_list[area - 1].bbox
            x, y = (tl[0] + br[0]) // 2, (tl[1] + br[1]) // 2
            ret = controller.swipe(x, y, swipe_dir, dist)
            if ret == "ERROR":
                print_with_color("ERROR: swipe execution failed", "red")
                break
        # elif act_name == "clarification" or act_name == "confirmation":
        #     _, question = res
        #     user_response = input()
        #     user_interaction = f"{act_name} question: {question}, user responce: {user_response}."
        #     print_with_color(f"{user_interaction}", "green")
        #     # time.sleep(configs["REQUEST_INTERVAL"])
        else:
            print_with_color(f"Invalid prompt style: {prompt_style}", "red")
            break
        with open(explore_log_path, "w") as logfile:
            json.dump(log_item, logfile, indent=4)
    except Exception as e:
        test_log["complete"] = "Error"
        break

    time.sleep(configs["REQUEST_INTERVAL"])
    test_log["actions_seq"].append(act_name)

    # input("Enter to continue...")
    

if task_complete:
    print_with_color(f"Autonomous exploration completed successfully.", "yellow")
    if test_name:
        test_log["complete"] = True
elif round_count == configs["MAX_ROUNDS"]:
    print_with_color(f"Autonomous exploration finished due to reaching max rounds.",
                     "yellow")
else:
    print_with_color(f"Autonomous exploration finished unexpectedly.", "red")

with open(explore_log_path, "w") as logfile:
    json.dump(log_item, logfile, indent=4)
print_with_color(f"Log file saved to {explore_log_path}", "red")

if test_name:
    test_log["log_path"] = explore_log_path.replace("\\", "/")
    test_log["result_image"] = base64_img_before.replace("\\", "/")
    test_log["rounds"] = round_count
    test_log_path = os.path.join(test_log_dir, f"{test_name}.json")
    with open(test_log_path, "w") as logfile:
        json.dump(test_log, logfile, indent=4)
    print_with_color(f"Test log file saved to {test_log_path}", "red")