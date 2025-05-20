def format_structure(server_type, raw_data):
    if server_type == "SQLite":
        db_structure_str = ""
        selected_tables_names_str = ""
        ddl_str = ""
        demo_data_str = ""
        if raw_data["selected_tables_names"] is None:
            raise ValueError("用户选中的表格为空")
        else:
            selected_tables_names = raw_data["selected_tables_names"]
            selected_tables_names_str = "用户选中的表格:\n" + "\n".join(
                [f"{i}. {table_name}" for i, table_name in enumerate(selected_tables_names, start=1)]) + "\n"
        if raw_data["structure"] is None:
            raise ValueError("数据库结构信息为空")
        else:
            db_structure = raw_data["structure"]
            structure_str = ""
            i = 1
            for table_name, columns in db_structure.items():
                structure_str += f"{i}. 表名: {table_name}\n"
                columns_str = [f"{col[0]} ({col[1]})" for col in columns]
                structure_str += "列名: " + ", ".join(columns_str) + "\n"
                i += 1
            db_structure_str = "表格结构信息:\n" + structure_str + "\n"
        if raw_data["ddl"] is None:
            raise ValueError("表格DDL信息为空")
        else:
            ddl = raw_data["ddl"]
            ddl_str = "表格DDL信息:\n" + "\n".join(
                [f"{table_name}:\n{ddl[table_name]}" for table_name in selected_tables_names]) + "\n"
        if raw_data["demo_data"] is None:
            raise ValueError("表格示例数据为空")
        else:
            demo_data = raw_data["demo_data"]
            demo_data_str = "表格示例数据:\n" + "\n".join(
                [f"{table_name}:\n{demo_data[table_name]}" for table_name in selected_tables_names]) + "\n"
    elif server_type == "hive":
        db_structure_str = ""
        selected_tables_names_str = ""
        ddl_str = ""
        demo_data_str = ""
        if raw_data["selected_tables_names"] is None:
            raise ValueError("用户选中的表格为空")
        else:
            selected_tables_names = raw_data["selected_tables_names"]
            selected_tables_names_str = "用户选中的表格:\n" + "\n".join(
                [f"{i}. {table_name}" for i, table_name in enumerate(selected_tables_names, start=1)]) + "\n"
        if raw_data["structure"] is None:
            raise ValueError("数据库结构信息为空")
        else:
            db_structure = raw_data["structure"]
            structure_str = ""
            # 变成 table_name, column_name, description 的表格样式的string
            structure_str += "schema_name\ttable_name\tcolumn_name\tdescription\n"
            for table_name, columns in db_structure.items():
                schema_name, table_name = table_name.split(".")
                for col in columns:
                    structure_str += f"{schema_name}\t{table_name}\t{col[0]}\t{col[1]}\n"
            # i = 1
            # for table_name, columns in db_structure.items():
            #     structure_str += f"<table_name>{table_name}</table_name>:\n"
            #     columns_str = [f"{col[0]} ({col[1]})" for col in columns]
            #     structure_str += "- 列名: " + ", ".join(columns_str) + "\n"
            #     i += 1
            db_structure_str = "表格结构信息:\n" + structure_str + "\n"
        if raw_data["ddl"] is None:
            raise ValueError("表格DDL信息为空")
        else:
            ddl = raw_data["ddl"]
            ddl_str = "表格DDL信息:\n" + "\n".join(
                [f"{table_name}:\n{ddl[table_name]}" for table_name in selected_tables_names]) + "\n"
        if raw_data["demo_data"] is None:
            raise ValueError("表格示例数据为空")
        else:
            demo_data = raw_data["demo_data"]
            demo_data_str = "表格示例数据:\n" + "\n".join(
                [f"{table_name}:\n{demo_data[table_name]}" for table_name in selected_tables_names]) + "\n"
    else:
        db_structure_str = ""
        selected_tables_names_str = ""
        ddl_str = ""
        demo_data_str = ""
        raise ValueError("不支持的数据库服务类型")
        
    return {
        "db_structure": db_structure_str,
        "selected_tables_names": selected_tables_names_str,
        "ddl": ddl_str,
        "demo_data": demo_data_str
    }
        