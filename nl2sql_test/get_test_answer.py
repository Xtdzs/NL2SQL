import requests
import json

url = ""
schema = ""

def one_shot_test(nl: str, table_list: list):
    # configure
    table_list = [schema + "." + table for table in table_list]

    query = {
        "query": nl,
        "related_table": table_list,
        "engine": "presto",
        "function": "NL2SQL",
    }

    response = requests.post(url, json=query)

    if response.status_code == 200:
        result = response.json()
        print(result['result'])
        return result['result']
    else:
        print("Error:", response.status_code, response.text)
        return None


if __name__ == "__main__":
    # generate test answer
    data_path = "test_data/test_cases_2.json"
    with open(data_path, "r") as f:
        data = json.load(f)
    print(f"Total {len(data)} test cases loaded.")
    test_results = []
    for i, item in enumerate(data):
        nl = item["nl"]
        table_list = item["tables"]
        print(f"第{i+1}条测试用例：")
        test_result = one_shot_test(nl, table_list)
        test_results.append(test_result)
        
    # save test results
    with open("test_results/results_2.json", "w") as f:
        json.dump(test_results, f, indent=4, ensure_ascii=False)