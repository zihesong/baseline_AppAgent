import os
import json
from collections import OrderedDict
import pdb
import re, csv
import datetime

def extract_number(file_name):
    match = re.search(r'(\d+)\.png$', file_name)
    if match:
        return int(match.group(1))
    return 0  # In case there's no number in the file name

def remove_json_files(directory="./ground_truth"):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            remove_json_files(item_path)
        elif item.endswith(".json"):
            os.remove(item_path)
            print(f"Removed {item_path}")
            
            
def add_ground_truth():
    # Path to the root directory
    root_dir = "./ground_truth"

    # Loop through the directories and subdirectories
    for app_dir in os.listdir(root_dir):
        app_path = os.path.join(root_dir, app_dir)
        if os.path.isdir(app_path):
            for task_dir in os.listdir(app_path):
                task_path = os.path.join(app_path, task_dir)
                if os.path.isdir(task_path):
                    # Initialize an empty ordered dictionary
                    data = OrderedDict()

                    # Loop through the image files in the task directory
                    for filename in sorted([f for f in os.listdir(task_path) if os.path.isfile(os.path.join(task_path, f))], key=lambda x: int(os.path.splitext(x)[0])):
                        if filename.endswith(".png"):
                            image_name = os.path.splitext(filename)[0]
                            image_path = os.path.join("./ground_truth", app_dir, task_dir, filename).replace("\\", "/")

                            # Create the dictionary for each image
                            data[int(image_name)] = {
                                "app": app_dir,
                                "task": task_dir,
                                "image_path": image_path,
                                "ground_truth": ""
                            }

                    ground_truth_path = os.path.join(task_path, "ground_truth")
                    if not os.path.exists(ground_truth_path):
                        os.makedirs(ground_truth_path)
                    # Create the JSON file in the task directory
                    json_file = os.path.join(ground_truth_path, "ground_truth.json").replace("\\", "/")
                    with open(json_file, "w") as f:
                        json.dump(data, f, indent=4)

def get_timestamp(filename):
    timestamp_str = filename.split("_")[1] + "_" + filename.split("_")[2].split(".")[0]
    return datetime.datetime.strptime(timestamp_str, "%m-%d_%H-%M-%S")



def combine_test_logs():
        # Path to the root directory
    root_dir = "./test_logs"
    result_dir = os.path.join(root_dir, "result")
    os.makedirs(result_dir, exist_ok=True)

    total_data = {}

    # Traverse the directory structure
    for app_dir in os.listdir(root_dir):
        app_path = os.path.join(root_dir, app_dir)
        if os.path.isdir(app_path):
            for task_dir in os.listdir(app_path):
                task_path = os.path.join(app_path, task_dir)
                if os.path.isdir(task_path):
                    logs_dir = os.path.join(task_path, "logs")
                    if os.path.isdir(logs_dir):
                        latest_log = None
                        latest_timestamp = None

                        # Find the latest log file in the logs directory
                        for log_file in os.listdir(logs_dir):
                            if log_file.endswith(".json"):
                                log_path = os.path.join(logs_dir, log_file)
                                timestamp = get_timestamp(log_file)
                                if timestamp and (not latest_timestamp or timestamp > latest_timestamp):
                                    latest_log = log_path
                                    latest_timestamp = timestamp

                        # Load the latest log file and add its data to the total_data dictionary
                        if latest_log:
                            with open(latest_log, "r") as f:
                                log_data = json.load(f)
                                app_task_name = f"{app_dir}/{task_dir}"
                                for key, value in log_data.items():
                                    value["total"] = app_task_name
                                    total_data[f"{app_task_name}/{key}"] = value

    # Write the combined data to the total.json file
    total_json_path = os.path.join(result_dir, "total.json")
    with open(total_json_path, "w") as f:
        json.dump(total_data, f, indent=4)

    # Write the combined data to the total.csv file
    total_csv_path = os.path.join(result_dir, "total.csv")
    fieldnames = list(total_data.values())[0].keys()  # Get the fieldnames from the first value dictionary

    with open(total_csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for value in total_data.values():
            writer.writerow(value)

    print(f"Combined data written to {total_json_path} and {total_csv_path}")

if __name__ == "__main__":
    # remove_json_files()
    # add_ground_truth()
    combine_test_logs()
    pass