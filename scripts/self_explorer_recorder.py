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
parser.add_argument("--test_name", default="")
parser.add_argument("--test_setting", default="naive")
args = vars(parser.parse_args())

configs = load_config()

app = args["app"].replace("-", "")
task = args["task"].replace("-", " ")
root_dir = args["root_dir"]
test_name = args["test_name"]
test_setting = args["test_setting"]


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
    

    
while True:
    round_count += 1
    print_with_color(f"\n-------------------------------------------", "magenta")
    print_with_color(f"< Round {round_count}, task: {task_desc} >", "red")
    print_with_color(f"Press [ENTER] if screen is ready or enter [Q] to quit:", "green", new_line=False)
    user_input = input()
    if user_input == "Q":
        break
    print_with_color(f"Generating screenshots...", "yellow")
    pdb.set_trace()
    screenshot_before = controller.get_screenshot(f"{round_count}", task_dir, resized_percent=50)
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
    
    pdb.set_trace()
    draw_bbox_multi(screenshot_before, os.path.join(task_dir, f"{round_count}_labeled.png"), elem_list,
                    dark_mode=configs["DARK_MODE"])
    base64_img_before = os.path.join(task_dir, f"{round_count}_labeled.png")
        
    # prompt, image_list = prompts_factory.get_prompts(prompt_style, "decision", last_act, user_interaction, base64_img_before)
    # print_with_color(f"Images: {', '.join(image_list)}", "blue")
    
    """ First: Q or A """
    
    print_with_color(f"[Step 1] Q/A -> {base64_img_before}", "red")
    while True:
        print_with_color(f"Decision? (Q or A or F): ", "yellow", new_line=False)
        act_name = input().lower()
        if act_name in ["q", "a", "f"]:
            break
        
    if act_name == "q":
        act_name = "QUESTION"
    elif act_name == "a":
        act_name = "ACTION"
    elif act_name == "f":
        act_name = "FINISH"

        
        
    log_item[round_count]= {
        "Decision": {
            "action": act_name, 
            "image": f"{round_count}_before_labeled.png",
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
        print_with_color(f"[Step 1.5] Q -> {base64_img_before}", "red")
        print_with_color(f"Question?: ", "yellow", new_line=False)
        act_name = input()
        print_with_color(f"Answer?: ", "yellow", new_line=False)
        answer = input()
        res = f"Question: {act_name}, Answer: {answer}"
        log_item[round_count]["Question"] = {
            "action": res, 
            "image": f"{round_count}_before_labeled.png",
        }
        
        print_with_color(f"{res}", "green")    
        test_log["actions_seq"].append(res)
        if test_name:
            test_log["question_sets"][res] = base64_img_before.replace("\\", "/")

    
    """ Third: A """
    print_with_color(f"[Step 2] A -> {base64_img_before}", "red")
    while True:
        print_with_color(f"Action? (tap, text, long_press, swipe(21, \"up\", \"medium\")): ", "yellow", new_line=False)
        act_name = input().lower()
        if act_name.split("(")[0] in ["tap", "text", "long_press", "swipe"]:
            break
            
    # round_count += 1
    log_item[round_count]["Action"] = { 
        "action": act_name, 
        "image": f"{round_count}_before_labeled.png",
    }
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