import json

sub_data_path = "test_data/sub_data"
main_data_path = "test_data"

total_data = []

# for i in range(1, 41):
#     with open(f"{sub_data_path}/cases{i}.json", "r") as f:
#         content = f.read()
#     sub_json = json.loads(content, strict=False)
#     total_data += sub_json
#     print(f"第{i}条测试用例读取成功")
    
# with open(f"{main_data_path}/test_cases.json", "w") as f:
#     json.dump(total_data, f, indent=4, ensure_ascii=False)
# print(f"Total {len(total_data)} test cases generated.")

for i in range(41, 71):
    with open(f"{sub_data_path}/cases{i}.json", "r") as f:
        content = f.read()
    sub_json = json.loads(content, strict=False)
    total_data += sub_json
    print(f"第{i}条测试用例读取成功")
    
with open(f"{main_data_path}/test_cases_2.json", "w") as f:
    json.dump(total_data, f, indent=4, ensure_ascii=False)
print(f"Total {len(total_data)} test cases generated.")
        