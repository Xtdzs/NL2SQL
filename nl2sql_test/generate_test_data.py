import random
import json
from ollama import Client

ollama_client_host = "http://localhost:11434"

ddls = \
"""
CREATE TABLE Customers (
customer_id INT,
customer_full_name STRING,
customer_email_address STRING,
customer_contact_number STRING,
customer_shipping_address STRING,
customer_registered_date DATE,
PRIMARY KEY (customer_id)
);

说明：记录客户的基本信息。

Products（产品信息表）

CREATE TABLE Products (
product_id INT,
product_name STRING,
product_category STRING,
product_description STRING,
product_launch_date DATE,
warranty_period_in_months INT,
product_sku_code STRING,
product_status STRING,
PRIMARY KEY (product_id)
);

说明：记录电脑产品的基本信息，如型号、分类、SKU 等。

ProductSpecifications（产品配置表）

CREATE TABLE ProductSpecifications (
specification_id INT,
product_id INT,
processor_model STRING,
ram_capacity_in_gb INT,
storage_type STRING,
storage_capacity_in_gb INT,
graphics_card_model STRING,
screen_size_in_inches DOUBLE,
battery_life_estimation_hours DOUBLE,
has_touchscreen BOOLEAN,
maximum_wireless_connectivity_standard_supported STRING,
number_of_usb_type_c_ports_supported_by_the_motherboard INT,
PRIMARY KEY (specification_id),
FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

说明：详细的硬件参数，字段名复杂且长。

Suppliers（供应商表）

CREATE TABLE Suppliers (
supplier_id INT,
supplier_name STRING,
supplier_contact_email STRING,
supplier_contact_number STRING,
supplier_country STRING,
PRIMARY KEY (supplier_id)
);

说明：供应商的基本信息。

ProductSupplierMapping（产品供应商关系表）

CREATE TABLE ProductSupplierMapping (
mapping_id INT,
product_id INT,
supplier_id INT,
supply_price DECIMAL(10,2),
supply_lead_time_days INT,
PRIMARY KEY (mapping_id),
FOREIGN KEY (product_id) REFERENCES Products(product_id),
FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id)
);

说明：记录产品由哪个供应商供应及供货周期。

Orders（订单表）

CREATE TABLE Orders (
order_id INT,
customer_id INT,
order_date DATE,
order_total_amount DECIMAL(10,2),
order_status STRING,
shipping_tracking_number STRING,
estimated_delivery_date DATE,
PRIMARY KEY (order_id),
FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

说明：订单基本信息。

OrderItems（订单商品明细表）

CREATE TABLE OrderItems (
order_item_id INT,
order_id INT,
product_id INT,
quantity INT,
unit_price DECIMAL(10,2),
discount_percentage DECIMAL(5,2),
PRIMARY KEY (order_item_id),
FOREIGN KEY (order_id) REFERENCES Orders(order_id),
FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

说明：每个订单中的产品信息。

Inventory（库存表）

CREATE TABLE Inventory (
inventory_id INT,
product_id INT,
warehouse_location STRING,
quantity_in_stock INT,
last_restock_date DATE,
reorder_threshold INT,
FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

说明：记录库存位置和数量。

AfterSalesServiceRequests（售后服务申请表）

CREATE TABLE AfterSalesServiceRequests (
request_id INT,
order_id INT,
product_id INT,
request_date DATE,
issue_description STRING,
resolution_status STRING,
resolution_date DATE,
PRIMARY KEY (request_id),
FOREIGN KEY (order_id) REFERENCES Orders(order_id),
FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

说明：客户对已购产品的售后记录。

PaymentTransactions（支付信息表）

CREATE TABLE PaymentTransactions (
transaction_id INT,
order_id INT,
payment_method STRING,
transaction_date TIMESTAMP,
transaction_amount DECIMAL(10,2),
transaction_status STRING,
PRIMARY KEY (transaction_id),
FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

说明：支付方式、金额、状态。
"""
table_list = [
    "Customers", "Products", "ProductSpecifications",
    "Suppliers", "ProductSupplierMapping", "Orders",
    "OrderItems", "Inventory", "AfterSalesServiceRequests",
    "PaymentTransactions"
]
level_list = [1, 2, 3]
task_list = ["insert", "update", "delete", "join", "aggregate", "group_by", "order_by", "filter", "subquery", "union", "intersect", "except", "case_when", "window_function", "cte", "pivot", "unpivot", "json_agg", "jsonb_agg"]

client = Client(host=ollama_client_host)

prompt_template = \
"""
{{ ddl }}
以上是一个数据库的 DDL 语句。
我想做nl2sql的测试，想要一些测试用例。包含不同难度等级，不同任务类型，涉及不同表的字段。
任务包括但不限于以下类型：
{{ task_list }}
其中难度要求如下:
level为1：要求简单的查询，涉及单表的简单字段等
level为2：要求中等难度的查询，涉及多表连接，简单的聚合函数和分组等
level为3：要求复杂的查询，涉及多表连接，复杂的聚合函数和分组，子查询，窗口函数等。
请根据以上要求生成测试用例，要求包含一个list套json：
例如：
[
    {
        "level": 2,
        "tasks": ["select", "join"],
        "tables": ["Products", "Suppliers"],
        "nl": "查询所有产品的名称和对应的供应商名称",
        "sql": "SELECT Products.product_name, Suppliers.supplier_name FROM Products JOIN ProductSupplierMapping ON Products.product_id = ProductSupplierMapping.product_id JOIN Suppliers ON ProductSupplierMapping.supplier_id = Suppliers.supplier_id"
    },
    {
        "level": 3,
        "tasks": ["select", "join", "aggregate"],
        "tables": ["Products", "Suppliers", "Orders"],
        "nl": "查询每个供应商的产品数量和总销售额",
        "sql": "SELECT Suppliers.supplier_name, COUNT(Products.product_id) AS product_count, SUM(OrderItems.unit_price * OrderItems.quantity) AS total_sales FROM Suppliers JOIN ProductSupplierMapping ON Suppliers.supplier_id = ProductSupplierMapping.supplier_id JOIN Products ON ProductSupplierMapping.product_id = Products.product_id JOIN OrderItems ON Products.product_id = OrderItems.product_id GROUP BY Suppliers.supplier_name"
    }
]
帮我生成*5*条测试用例，要求每条测试用例的内容都不一样，且要包含不同的难度等级、仅包含增删查改中的改的任务和表的字段。
其中*1*条测试用例的难度等级为1，*2*条测试用例的难度等级为2，*2*条测试用例的难度等级为3。
只需要返回list套json格式的测试用例，不需要其他任何解释。
"""

# 生成测试用例
test_cases = []

for i in range(60, 70):
    prompt = prompt_template.replace("{{ ddl }}", ddls)
    response = client.chat(
        model="gemma2:9b",
        messages=[{"role": "user", "content": prompt}],
        options={"num_ctx": 16384},
    )
    content = response["message"]["content"]
    if "```json" in content:
        content = content.replace("```json", "").replace("```", "")
    # print(content)
    try:
        content_ = json.loads(content)
    except json.JSONDecodeError:
        print("JSON Decode Error")
        continue
    with open(f"test_data/sub_data/cases{i+1}.json", "a") as f:
        json_content = json.dumps(content_, ensure_ascii=False, indent=4)
        # 先清空文件
        f.truncate(0)
        f.write(json_content)
    print(f"第{i+1}条测试用例生成成功")