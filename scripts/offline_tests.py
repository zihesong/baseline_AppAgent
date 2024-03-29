import sys
import os
import pandas as pd
import argparse
import json
import pdb
import re

from config import load_config
from model import OpenAIModel, parse_explore_rsp
from utils import print_with_color
from prompts_offline import decision_template, question_template
import prompts_factory

configs = load_config()
if configs["MODEL"] == "OpenAI":
    mllm = OpenAIModel(base_url=configs["OPENAI_API_BASE"],
                    api_key=configs["OPENAI_API_KEY"],
                    model=configs["OPENAI_API_MODEL"],
                    temperature=configs["TEMPERATURE"],
                    max_tokens=configs["MAX_TOKENS"])
elif configs["MODEL"] == "Qwen":
    pass
else:
    print_with_color(f"ERROR: Unsupported model type {configs['MODEL']}!", "red")
    sys.exit()

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("--app")
parser.add_argument("--task", default="")
parser.add_argument("--image_path", default="")
parser.add_argument("--log_path", default="")
parser.add_argument("--log_name", default="")
args = vars(parser.parse_args())
app = args["app"]
task_desc = args["task"].replace("-", " ")
image_path = args["image_path"]
log_path = args["log_path"]
log_name = args["log_name"]

test_count = image_path.split("/")[-1].split(".")[0]
task_complete = False

test_content = {
    "app": app,
    "task": task_desc,
    "image_path": image_path,
}

system_prompt = prompts_factory.get_system_prompt(task_desc, app)

"""1: Q or A"""
decision_template = re.sub(r"<task_description>", task_desc, decision_template)
decision_template = re.sub(r"<app>", app, decision_template)
status, rsp = mllm.get_model_response(system_prompt, decision_template, [image_path])
assert status, f"Error: {rsp}"

# Parse rsp
try:
    decision = re.findall(r"decision: (.*?)$", rsp, re.MULTILINE)[0]
except:
    decision = "ERROR"
print_with_color(f"decision: {decision}", "green")
test_content["decision"] = decision

if decision.lower() == "true":
    question_template = re.sub(r"<task_description>", task_desc, question_template)
    question_template = re.sub(r"<app>", app, question_template)
    status, rsp = mllm.get_model_response(system_prompt, question_template, [image_path])
    assert status, f"Error: {rsp}"
    try:
        question = re.findall(r"question: (.*?)$", rsp, re.MULTILINE)[0]
    except:
        question = ""
    print_with_color(f"question: {question}", "green")
    test_content["question"] = question
else:
    test_content["question"] = ""

log_name = os.path.join(log_path, log_name).replace("\\", "/")
if not os.path.exists(log_name):
    with open(log_name, 'w') as file:
        json.dump({test_count: test_content}, file, indent=4)
else:
    with open(log_name, 'r+') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = {}
        data[test_count] = test_content
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

print_with_color(f"[{task_desc}, {test_count}]: Data saved/updated in {log_name}", "blue")