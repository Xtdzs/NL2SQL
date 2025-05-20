import json
import os
import pandas as pd
import numpy as np

ground_truth_path_1 = "test_data/test_cases.json"
test_results_path_1 = "test_results/results.json"
ground_truth_path_2 = "test_data/test_cases_2.json"
test_results_path_2 = "test_results/results_2.json"
eval_data_path = "eval_data/eval_data.csv"

# Load ground truth data
with open(ground_truth_path_1, "r") as f:
    ground_truth_1 = json.load(f)
with open(ground_truth_path_2, "r") as f:
    ground_truth_2 = json.load(f)
ground_truth = ground_truth_1 + ground_truth_2
print(f"Total {len(ground_truth)} ground truth data loaded.")
# Load test results data
with open(test_results_path_1, "r") as f:
    test_results_1 = json.load(f)
with open(test_results_path_2, "r") as f:
    test_results_2 = json.load(f)
test_results = test_results_1 + test_results_2
print(f"Total {len(test_results)} test results data loaded.")
# Check if the number of ground truth data and test results data are equal
if len(ground_truth) != len(test_results):
    print("Error: The number of ground truth data and test results data are not equal.")
    exit(1)
# Generate eval data

eval_data = []
for i, item in enumerate(ground_truth):
    nl = item["nl"]
    level = item["level"]
    tasks = item["tasks"]
    tables = item["tables"]
    sql = item["sql"]
    test_result = test_results[i]
    
    eval_data.append({
        "nl": nl,
        "level": level,
        "tasks": tasks,
        "tables": tables,
        "ground_truth": sql,
        "test_result": test_result
    })
print(f"Total {len(eval_data)} eval data generated.")
# Save eval data to CSV
eval_df = pd.DataFrame(eval_data)
eval_df.to_csv(eval_data_path, index=False, encoding="gbk", quoting=1)
print(f"Eval data saved to {eval_data_path}.")