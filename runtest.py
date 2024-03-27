from login_utils import setup
import pandas as pd
import os
import json
import datetime
import time
import pdb
import shutil
import argparse

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
""" Test_settings:
    0. record (record ground truth)
    1. naive (no tagged images)
    2. normal (tagged images)
    3. TBD
"""
parser.add_argument("--test_setting", default="naive")
args = vars(parser.parse_args())
test_setting = args['test_setting']


def combine_test_logs(directory):
    combined_data = []

    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as json_file:
                data = json.load(json_file)
                combined_data.append(data)
    df = pd.DataFrame(combined_data)

    output_csv_path = directory + '/test_logs.csv'
    df.to_csv(output_csv_path, index=False)
    
    # Copy log folder
    for i, row in df.iterrows():
        source_dir = os.path.dirname(row['log_path'])
        dest_dir = os.path.join(directory, row['app'].replace(' ', '-'), row['task'].replace(' ', '-'))
        shutil.copytree(source_dir, dest_dir)
  
      
def main():
    test_items = pd.read_csv("test_items.csv")
    test_name = datetime.datetime.fromtimestamp(int(time.time())).strftime("test_%m-%d_%H-%M-%S")
    print(f"\n+---------------------------------------------------------+")
    print(f"| Test name: \"{test_name}\"; Test setting: \"{test_setting}\" |")
    print(f"+---------------------------------------------------------+")
    test_log_root_dir = f"./test_logs/test_setting_{test_setting}/"
    if not os.path.exists(test_log_root_dir):
        os.mkdir(test_log_root_dir)
    for i, test in test_items.iterrows():
        print(">> Login...")
        setup.setup_app(test['app']) 
        command = f"python learn.py --app {test['app']} --task {test['task']} --prompt_style {test['prompt_style']} --test_name {test_name}.{i} --test_setting {test_setting}"
        print(f"Running test {i} => {command}")
        print(">> Start Testing...")
        os.system(command)
    print("Gather Test Logs... ")
    combine_test_logs(test_log_root_dir + test_name.split('.')[0])
    
if __name__ == "__main__":
    # Login Google Account before Testing
    main()
