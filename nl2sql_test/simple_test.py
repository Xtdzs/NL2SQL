import requests

url = "your_service_url"
table_list = ["your_table_list"]
question = ""

def one_shot_test(nl: str, table_list: list):
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
    one_shot_test(
        nl=question,
        table_list=table_list
    )