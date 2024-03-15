from login_utils import setup
import pandas as pd
import os
import json
import datetime
import time
import pdb

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'



def combine_test_logs(directory, test_name):
    # List to hold combined data
    combined_data = []
    json_files_to_delete = []

    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as json_file:
                data = json.load(json_file)
                combined_data.append(data)
                json_files_to_delete.append(filepath)
    df = pd.DataFrame(combined_data)

    result_dir = os.path.join('./test_logs/', test_name)
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    output_csv_path = result_dir + '/test_logs.csv'
    df.to_csv(output_csv_path, index=False)

    if os.path.exists(output_csv_path) and not df.empty:
        for filepath in json_files_to_delete:
            os.remove(filepath)
            print(f"Deleted: {filepath}")    
    
   
def main():
    test_items = pd.read_csv("test_items.csv")
    test_name = datetime.datetime.fromtimestamp(int(time.time())).strftime("test_%m-%d_%H-%M-%S")
    print(f"Test name: [{test_name}]")
    for i, test in test_items.iterrows():
        setup.setup_app(test['app'])
        input("Enter to continue///")
        # command = f"python learn.py --app {test['app']} --task {test['task']} --prompt_style {test['prompt_style']} --test_name {test_name}.{i}"
        # print(f"Running test {i} => {command}")
        # os.system(command)
    print("Gather Test Logs... ")
    combine_test_logs("./test_logs", test_name.split('.')[0])
    
if __name__ == "__main__":
    # print(f"Login Google Account...")
    # setup.setup_googleaccount()
    # Manually login may be better
    main()
