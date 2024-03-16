from login_utils import setup
import pandas as pd
import os
import json
import datetime
import time
import pdb
import shutil

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'



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
    pdb.set_trace()
    for i, row in df.iterrows():
        source_dir = os.path.dirname(row['log_path'])
        dest_dir = os.path.join(directory, row['app'].replace(' ', '-'), row['task'].replace(' ', '-'))
        shutil.copytree(source_dir, dest_dir)
  
    
   
def main():
    test_items = pd.read_csv("test_items.csv")
    test_name = datetime.datetime.fromtimestamp(int(time.time())).strftime("test_%m-%d_%H-%M-%S")
    print(f"Test name: [{test_name}]")
    test_log_root_dir = "./test_logs"
    if not os.path.exists(test_log_root_dir):
        os.mkdir(test_log_root_dir)
    for i, test in test_items.iterrows():
        setup.setup_app(test['app'])     
        command = f"python learn.py --app {test['app']} --task {test['task']} --prompt_style {test['prompt_style']} --test_name {test_name}.{i}"
        print(f"Running test {i} => {command}")
        os.system(command)
    test_name = "test_03-15_22-59-29"
    print("Gather Test Logs... ")
    combine_test_logs("./test_logs/" + test_name.split('.')[0])
    
if __name__ == "__main__":
    # print(f"Login Google Account...")
    # setup.setup_googleaccount()
    # Manually login may be better
    main()
