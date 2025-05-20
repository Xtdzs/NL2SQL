import sqlite3
from trino.dbapi import connect

class BaseDBServer:
    def __init__(self):
        self.server_type = None

    def disconnect(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def execute_query(self, query):
        raise NotImplementedError("Subclasses should implement this method.")

    def get_ddl(self):
        """
        Get the Data Definition Language (DDL) of the database.
        This method should be implemented by subclasses to return the DDL.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    def get_demo(self):
        """
        Get the demo data from the database.
        This method should be implemented by subclasses to return the demo data.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    def get_structure(self):
        """
        Get the structure of the database.
        This method should be implemented by subclasses to return the structure.
        """
        raise NotImplementedError("Subclasses should implement this method.")
    
    def get_server_type(self):
        """
        Get the type of the database server.
        This method should be implemented by subclasses to return the server type.
        """
        return self.server_type
    
    def get_prepared_data(self):
        """
        Get the prepared data from the database.
        This method should be implemented by subclasses to return the prepared data.
        """
        raise NotImplementedError("Subclasses should implement this method.")
    
    
class DemoBuilder:
    def __init__(self):
        pass

    def build_demo(self, private_data, method='mask'):
        """
        Build a demo dataset from the private data.

        :param private_data: The private data to be used for building the demo.
        :param method: The method to be used for building the demo. Options are 'mask' or 'sample'.
        :return: The demo dataset.
        """
        if method == 'mask':
            # Masking logic
            demo_data = private_data.copy()
            for column in demo_data.columns:
                if demo_data[column].dtype == 'object':
                    demo_data[column] = demo_data[column].apply(lambda x: '*' * len(x))
                else:
                    demo_data[column] = demo_data[column].apply(lambda x: None)
            return demo_data
        else:
            raise ValueError("Invalid method. Choose either 'mask' or 'sample'.")
        
        
class HiveDBServer(BaseDBServer):
    def __init__(self, host, port, user, catalog, schema):
        super().__init__()
        self.server_type = "hive"
        self.schema = schema
        self.connection = connect(
            host=host,
            port=port,
            user=user,
            catalog=catalog,
            schema=schema,
        )

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def get_ddl(self, table_list=None):
        if self.connection is None:
            raise Exception("Database connection is not established. Call connect() first.")
        cursor = self.connection.cursor()
        if table_list is None:
            cursor.execute("SHOW TABLES")
            table_list = [table[0] for table in cursor.fetchall()]
        ddl_dict = {}
        for table in table_list:
            cursor.execute(f"SHOW CREATE TABLE {table}")
            ddl = cursor.fetchone()[0]
            ddl_dict[table] = ddl
        return ddl_dict

    def get_demo(self, table_list=None, demo_num=5):
        if self.connection is None:
            raise Exception("Database connection is not established. Call connect() first.")
        cursor = self.connection.cursor()
        if table_list is None:
            cursor.execute("SHOW TABLES")
            table_list = [table[0] for table in cursor.fetchall()]
        demo_data = {}
        # demo_builder = DemoBuilder()
        for table in table_list:
            cursor.execute(f"SELECT * FROM {table} LIMIT {demo_num}")
            private_data = cursor.fetchall()
            # column_names = [description[0] for description in cursor.description]
            demo_data[table] = private_data
            # import pandas as pd
            # private_data = pd.DataFrame(private_data, columns=column_names)
            # demo_data[table] = demo_builder.build_demo(private_data, method='mask')
        return demo_data

    def get_structure(self, selected_tables_names=None):
        if self.connection is None:
            raise Exception("Database connection is not established. Call connect() first.")
        cursor = self.connection.cursor()
        if selected_tables_names is None:
            cursor.execute("SHOW TABLES")
            table_list = [self.schema + "." + table[0] for table in cursor.fetchall()]
        else:
            table_list = selected_tables_names
        structure = {}
        for table in table_list:
            cursor.execute(f"DESCRIBE {table}")
            structure[table] = cursor.fetchall()
        return structure
    
    def get_prepared_data(self, selected_tables_names):
        db_structure = self.get_structure(selected_tables_names)
        ddl = self.get_ddl(selected_tables_names)
        demo_data = self.get_demo(selected_tables_names, demo_num=1)
        return{
            "selected_tables_names": selected_tables_names,
            "structure": db_structure,
            "ddl": ddl,
            "demo_data": demo_data
        }
        

class SQLiteDBServer(BaseDBServer):
    def __init__(self, db_name):
        super().__init__(db_name)
        self.server_type = "SQLite"
        self.connection = sqlite3.connect(self.db_name)


    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def get_ddl(self, table_list=None):
        """
        Get the Data Definition Language (DDL) of the SQLite database.
        This method retrieves the DDL for all tables in the database.
        """
        if self.connection is None:
            raise Exception("Database connection is not established. Call connect() first.")
        cursor = self.connection.cursor()

        # Get the list of all tables in the database
        if table_list is None:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            table_list = [table[0] for table in cursor.fetchall()]

        ddl_dict = {}
        for table in table_list:
            # Get the DDL for each table
            cursor.execute(f"SELECT sql FROM sqlite_master WHERE name='{table}';")
            ddl = cursor.fetchone()[0]
            ddl_dict[table] = ddl

        return ddl_dict

    def get_demo(self, table_list=None, demo_num=5):
        """
        Get the demo data from the SQLite database.
        This method retrieves a sample of demo data from the specified tables.
        """
        if self.connection is None:
            raise Exception("Database connection is not established. Call connect() first.")
        cursor = self.connection.cursor()

        # Get the list of all tables in the database
        if table_list is None:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            table_list = [table[0] for table in cursor.fetchall()]

        demo_data = {}
        demo_builder = DemoBuilder()
        for table in table_list:
            # Get a sample of demo data from each table
            cursor.execute(f"SELECT * FROM {table} LIMIT {demo_num};")
            private_data = cursor.fetchall()
            # Get the column names
            column_names = [description[0] for description in cursor.description]
            # Convert to DataFrame
            import pandas as pd
            private_data = pd.DataFrame(private_data, columns=column_names)
            # Build demo data using the DemoBuilder
            demo_data[table] = demo_builder.build_demo(private_data, method='mask')

        return demo_data

    def get_structure(self):
        """
        Get the structure of the SQLite database.
        This method retrieves the structure of all tables in the database.
        """
        if self.connection is None:
            raise Exception("Database connection is not established. Call connect() first.")
        cursor = self.connection.cursor()

        # Get the list of all tables in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_list = [table[0] for table in cursor.fetchall()]

        structure = {}
        for table in table_list:
            # Get the structure of each table
            cursor.execute(f"PRAGMA table_info({table});")
            structure[table] = cursor.fetchall()

        return structure
    
    def get_prepared_data(self, selected_tables_names):
        db_structure = self.get_structure()
        ddl = self.get_ddl(selected_tables_names)
        demo_data = self.get_demo(selected_tables_names, demo_num=1)
        return{
            "selected_tables_names": selected_tables_names,
            "structure": db_structure,
            "ddl": ddl,
            "demo_data": demo_data
        }
