import argparse
import ast
import datetime
import json
import os
import re
import sys
import time

import prompts
import prompts_sequential
import prompts_parallel
import examples
from config import load_config
from and_controller import list_all_devices, AndroidController, traverse_tree
from model import parse_explore_rsp, parse_reflect_rsp, OpenAIModel, QwenModel
from utils import print_with_color, draw_bbox_multi

arg_desc = "AppAgent - Autonomous Exploration"
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=arg_desc)
parser.add_argument("--app")
parser.add_argument("--root_dir", default="./")
parser.add_argument("--prompt_style", default="sequential")
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

app = args["app"]
root_dir = args["root_dir"]
prompt_style = args["prompt_style"]

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

print_with_color("Please enter the description of the task you want me to complete in a few sentences:", "blue")
task_desc = input()

round_count = 0

useless_list = set()
last_act = "None"
task_complete = False
user_interaction = "None"
log_item = {}
prompt_template = ""
example_images = ""
if prompt_style == "sequential":
    prompt_template = prompts_sequential.self_explore_task_template
elif prompt_style == "parallel":   
    prompt_template = prompts_parallel.self_explore_task_template
else:
    prompt_style = prompts.self_explore_task_template
print_with_color(f"Prompt style: {prompt_style}", "red")
    
while round_count < configs["MAX_ROUNDS"]:
    round_count += 1
    print_with_color(f"Round {round_count}", "yellow")
    screenshot_before = controller.get_screenshot(f"{round_count}", task_dir)
    xml_path = controller.get_xml(f"{round_count}", task_dir)
    if screenshot_before == "ERROR" or xml_path == "ERROR":
        break
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

    prompt = re.sub(r"<task_description>", task_desc, prompt_template)
    prompt = re.sub(r"<app>", app, prompt)
    prompt = re.sub(r"<last_act>", last_act, prompt)
    # if user_interaction:
    #     prompt = re.sub(r"<user_interaction>", user_interaction, prompt)
    # else:
    #     prompt = re.sub(r"<user_interaction>", ";".join(user_interaction), prompt)
    prompt = re.sub(r"<previous_interactions>", user_interaction, prompt)
    if prompt_style == "sequential":
        example_images = re.findall(r'<([^>]+)>', examples.self_explore_task_example)
        cleaned_example_prompt = re.sub(r'<([^>]+)>', '', examples.self_explore_task_example)
        prompt = re.sub(r"<examples>", cleaned_example_prompt, prompt) 
    base64_img_before = os.path.join(task_dir, f"{round_count}_labeled.png")
    """ LLM Generation """
    print_with_color("Getting response from the model...", "yellow")
    status, rsp = mllm.get_model_response(prompt, example_images + [base64_img_before])
    print_with_color(', '.join(example_images + [base64_img_before]), 'blue')
    
    assert status, f"Error: {rsp}"
    
    res, log_dict = parse_explore_rsp(rsp)
    act_name = res[0]
    last_act = res[-1]
    res = res[:-1]
    log_item[act_name] = { 
        "action": act_name, 
        "response": log_dict, 
        "image": f"{round_count}_before_labeled.png",
        "prompt": prompt, 
    }
        # print(res)
    if prompt_style == "sequential":
        print_with_color(f"Taking a [{act_name}] action...", "green")
        if act_name == "QUESTION":
            prompt = re.sub(r"<task_description>", task_desc, prompts_sequential.self_explore_task_question_template)
            prompt = re.sub(r"<examples>", examples.self_explore_task_question_example, prompt)
        elif act_name == "ACTION":
            prompt = re.sub(r"<task_description>", task_desc, prompts_sequential.self_explore_task_action_template)
            prompt = re.sub(r"<examples>", examples.self_explore_task_action_example, prompt)
        elif act_name == "FINISH":
            task_complete = True
            break
        
        prompt = re.sub(r"<app>", app, prompt)
        prompt = re.sub(r"<last_act>", last_act, prompt)
        prompt = re.sub(r"<previous_interactions>", user_interaction, prompt)
        
        # print_with_color(f"{prompt}", "red")
        print_with_color("Getting response from the model...", "yellow")
        status, rsp = mllm.get_model_response(prompt, [base64_img_before])
            
        assert status, f"Error: {rsp}"
            
        res, log_dict = parse_explore_rsp(rsp)
        act_name = res[0]
        last_act = res[-1]
        res = res[:-1]
        # round_count += 1
        log_item[round_count] = { 
            "action": act_name, 
            "response": log_dict, 
            "image": f"{round_count}_before_labeled.png",
            "prompt": prompt, 
        }
    
    ### Process all function calls   
    if act_name == "FINISH":
        task_complete = True
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
    elif act_name == "clarification" or act_name == "confirmation":
        _, question = res
        user_response = input()
        # user_interaction.append(f"{act_name} question: {question}, user responce: {user_response}")
        user_interaction = f"{act_name} question: {question}, user responce: {user_response}."
        print_with_color(f"{user_interaction}", "green")
        # time.sleep(configs["REQUEST_INTERVAL"])
    else:
        print_with_color(f"Invalid prompt style: {prompt_style}", "red")
        break

    time.sleep(configs["REQUEST_INTERVAL"])
    # input("Enter to continue...")

if task_complete:
    print_with_color(f"Autonomous exploration completed successfully.", "yellow")
elif round_count == configs["MAX_ROUNDS"]:
    print_with_color(f"Autonomous exploration finished due to reaching max rounds.",
                     "yellow")
else:
    print_with_color(f"Autonomous exploration finished unexpectedly.", "red")

with open(explore_log_path, "a") as logfile:
    json.dump(log_item, logfile, indent=4)
    print_with_color(f"Log file saved to {explore_log_path}", "red")