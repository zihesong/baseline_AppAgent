import argparse
import datetime
import os
import time

from scripts.utils import print_with_color

arg_desc = "AppAgent - exploration phase"
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=arg_desc)
parser.add_argument("--app")
parser.add_argument("--task")
parser.add_argument("--root_dir", default="./")
parser.add_argument("--prompt_style", default="normal")
parser.add_argument("--test_name", default="")
parser.add_argument("--test_setting", default="naive")
args = vars(parser.parse_args())

app = args["app"]
task = args["task"]
root_dir = args["root_dir"]
prompt_style = args["prompt_style"]
test_name = args["test_name"]
test_setting = args["test_setting"]


# print_with_color("Welcome to the exploration phase of AppAgent!\nThe exploration phase aims at generating "
                #  "documentations for UI elements through either autonomous exploration or human demonstration. "
                #  "Both options are task-oriented, which means you need to give a task description. During "
                #  "autonomous exploration, the agent will try to complete the task by interacting with possible "
                #  "elements on the UI within limited rounds. Documentations will be generated during the process of "
                #  "interacting with the correct elements to proceed with the task. Human demonstration relies on "
                #  "the user to show the agent how to complete the given task, and the agent will generate "
                #  "documentations for the elements interacted during the human demo. To start, please enter the "
                #  "main interface of the app on your phone.", "yellow")
# print_with_color("Choose from the following modes:\n1. autonomous exploration\n2. human demonstration\n"
#                  "Type 1 or 2.", "blue")
user_input = "1"
# while user_input != "1" and user_input != "2":
    # user_input = input()


if not app:
    print_with_color("What is the name of the target app?", "blue")
    app = input()
    app = app.replace(" ", "")

if user_input == "1":
    if test_setting == "record":
        os.system((f"python scripts/self_explorer_recorder.py"
            f" --app {app}" 
            f" --task {task}" 
            f" --root_dir {root_dir}"
            f" --test_name {test_name}"
            f" --test_setting {test_setting}"))
    else:
        print_with_color(f"Prompt Style {prompt_style}", "red")
        os.system((f"python scripts/self_explorer.py"
            f" --app {app}" 
            f" --task {task}"
            f" --root_dir {root_dir}"
            f" --prompt {prompt_style}"
            f" --test_name {test_name}"
            f" --test_setting {test_setting}"))
else:
    demo_timestamp = int(time.time())
    demo_name = datetime.datetime.fromtimestamp(demo_timestamp).strftime(f"demo_{app}_%Y-%m-%d_%H-%M-%S")
    os.system(f"python scripts/step_recorder.py --app {app} --demo {demo_name} --root_dir {root_dir}")
    os.system(f"python scripts/document_generation.py --app {app} --demo {demo_name} --root_dir {root_dir}")
