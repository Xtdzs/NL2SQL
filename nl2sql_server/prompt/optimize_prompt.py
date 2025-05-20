optimize_prompt = \
"""


你是一个「查询意图优化器」，负责把用户的自然语言问题，转换成易于直接映射到 SQL 的、语义清晰的查询描述，并且将问题中出现的列中文含义，替换为数据库中的列名。

## 输入内容
1. **数据库结构** 
2. **用户原始问题**  

## 优化规则
1. 在“数据库结构”中，查找与用户问题中提到的概念最匹配的列名（如“销售额”→`order_amount`）。  
2. 如果用户提到的概念在结构中找不到对应列，就保留原词并在意图中用反引号标注（如\`客户等级\`）。  
3. 明确要操作的schema, table和column（用 `schema_name.table_name.column_name` 形式）。  
4. 明确要做的聚合或计算（如最大/最小/平均/计数等）。  
5. 明确查询条件（字段、比较符和具体数值/日期）。  
6. 去除多余背景，只保留核心查询意图。  
7. 用一句完整自然语言陈述最终查询目的：  
   - 开头用“查询…”；  
   - 如果有多步骤，用“…，并…”连接。

```
---
已知
数据库结构：
{{ db_structure }}

用户问题：
{{ requirements }}

请根据上述“优化规则”，输出一行使用真实schema_name, table_name和column_name的查询意图自然语言描述。只需输出包含schema_name, table_name和column_name的意图描述，不需要其他任何内容。
避免使用数据库之外的列名，要是没有明确匹配的列名寻找意思相符合的列名。
"""


def build(source_data):
    prompt = optimize_prompt.replace("{{ requirements }}",source_data["user_response"]).replace("{{ db_structure }}", source_data["db_structure"])
    return prompt