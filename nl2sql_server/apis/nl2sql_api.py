from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Literal
from prepare.db_loader import SQLiteDBServer, HiveDBServer
from prepare.structure_parser import format_structure
from prompt import optimize_prompt, sql_prompt
from core import query_optimizer, sql_generator
from llms import ollama_client
import config

app = FastAPI()

class Query(BaseModel):
    query: str
    related_table: List[str]
    engine: Literal["presto", "spark"]
    function: Literal["NL2SQL"]

@app.get("/test_connect/")
async def test():
    return {"message": "Connection successful!"}

@app.post("/service/")
async def service(query: Query):
    user_response = query.query
    db_category = query.engine
    selected_tables_names = query.related_table
    f = query.function
    client = ollama_client.OllamaClient(
        host=config.ollama_host,
    )
    
    if f == "NL2SQL":
        db_server = HiveDBServer(
            host=config.db_host,
            port=config.db_port,
            user=config.db_user,
            catalog=config.db_catalog,
            schema=config.db_schema,
        )
        print("Hive数据库连接成功")            
        raw_prepared_data = db_server.get_prepared_data(
            selected_tables_names=selected_tables_names
        )
        processed_data = format_structure(
            server_type=db_server.server_type,
            raw_data=raw_prepared_data
        )
        print("structured_data:\n", processed_data["db_structure"])
        processed_data["db_category"] = db_category
        processed_data["user_response"] = user_response
        
        tobe_optimized_prompt = optimize_prompt.build(
            source_data=processed_data,
        )
        
        # print("intent_classify_prompt:", intent_classify_prompt)
        # print("intent_classify_prompt_type:", type(intent_classify_prompt))
        
        optimized_prompt = query_optimizer.generate(
            client=client,
            model_name=config.common_model_name,
            prompt=tobe_optimized_prompt,
        )
        
        print("optimized_prompt:", optimized_prompt)
        
        processed_data["user_response"] = optimized_prompt
        
        # print("intent_index:", intent_index)
            
        input_prompt = sql_prompt.build(
            source_data=processed_data
        )
        
        client_reply = sql_generator.generate(
            client=client,
            model_name=config.sql_model_name,
            prompt=input_prompt,
        )
        
        return {
            "result": client_reply
        }
            
       
        
    else:
        raise ValueError("Unsupported function type")
    

    
    
