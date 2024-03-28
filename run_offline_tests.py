import os
import shutil
from tqdm import tqdm
import pdb
import re
import datetime, time

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

def extract_number(file_name):
    match = re.search(r'(\d+)\.png$', file_name)
    if match:
        return int(match.group(1))
    return 0  # In case there's no number in the file name


def main():
    base_path = './ground_truth'  
    ground_truth_data = {}

    for app_name in os.listdir(base_path):
        app_path = os.path.join(base_path, app_name)
        if os.path.isdir(app_path):
            ground_truth_data[app_name] = {}  
            for task_name in os.listdir(app_path):
                task_path = os.path.join(app_path, task_name)
                if os.path.isdir(task_path):
                    image_files = [os.path.join(task_path, img).replace("\\","/") for img in os.listdir(task_path) if img.endswith('.png')]
                    ground_truth_data[app_name][task_name] = image_files
    
    
    log_root_dir = "./test_logs"
    if not os.path.exists(log_root_dir):
        os.mkdir(log_root_dir)
        
    for app_name in ground_truth_data:
        app_log_dir = os.path.join(log_root_dir, app_name)
        if not os.path.exists(app_log_dir):
            os.mkdir(app_log_dir)
        for task_name in ground_truth_data[app_name]:
            task_log_root_dir = os.path.join(app_log_dir, task_name)
            if not os.path.exists(task_log_root_dir):
                os.mkdir(task_log_root_dir)
            task_log_dir = os.path.join(task_log_root_dir, "logs")
            if not os.path.exists(task_log_dir):
                os.mkdir(task_log_dir)
            # Sorting the list using the extracted number as key
            log_name = datetime.datetime.fromtimestamp(int(time.time())).strftime("log_%m-%d_%H-%M-%S")
            sorted_image_list = sorted(ground_truth_data[app_name][task_name], key=extract_number)
            for image_path in tqdm(sorted_image_list, desc=f"Processing: {app_name}/{task_name}", colour="red"):
                shutil.copy(image_path, task_log_root_dir)
                # print(f">> App: {app_name}, Task: {task_name}, image: {image_path}")
                command = f"python ./scripts/offline_tests.py --app {app_name} --task {task_name} --image_path {image_path} --log_path {task_log_dir} --log_name {log_name}.json"
                os.system(command)
        print("-"*50)

            
if __name__ == "__main__":
    main()