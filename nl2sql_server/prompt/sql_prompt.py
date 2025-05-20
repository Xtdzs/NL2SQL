prompt_template = \
"""
以下是一些根据用户问题查询到的数据库信息.
---------------------
{{ context_str }}
---------------------
基于以上信息和用户的需求: {{ query_str }}
请给出{{ db_category }}查询语句来满足用户的需求（注意：只需要给出{{ db_category }}语句，不解释）
"""
    
def build(source_data):
    context_info = ""
    # context_info += source_data["db_structure"] + '\n'
    # context_info += source_data["selected_tables_names"] + '\n'
    context_info += source_data["ddl"] + '\n'
    # context_info += source_data["demo_data"] + '\n'
    prompt = prompt_template.replace("{{ context_str }}", context_info).replace("{{ query_str }}", source_data["user_response"]).replace("{{ db_category }}", source_data["db_category"])
    return prompt