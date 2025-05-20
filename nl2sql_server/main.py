import argparse 
import uvicorn
import config

def apiservice(
    service_host, service_port, service_reload, service_workers, 
    db_host, db_port, db_user, db_catalog, db_schema,
    ollama_host, common_model_name, sql_model_name):
    config.ollama_host = ollama_host
    config.common_model_name = common_model_name
    config.sql_model_name = sql_model_name
    config.db_host = db_host
    config.db_port = db_port
    config.db_user = db_user
    config.db_catalog = db_catalog
    config.db_schema = db_schema
    config.service_host = service_host
    config.service_port = service_port
    config.service_reload = service_reload
    config.service_workers = service_workers
    
    uvicorn.run(
        "apis.nl2sql_api:app", 
        host=config.service_host, 
        port=config.service_port, 
        reload=config.service_reload, 
        workers=config.service_workers
    )

if __name__ == "__main__" : 
    parser = argparse.ArgumentParser(description='config')
    parser.add_argument('--service_host', type=str, help='uvicorn host address')
    parser.add_argument('--service_port', type=int, help='uvicorn port')
    parser.add_argument('--service_reload', default=False, type=bool, help='uvicorn reload')
    parser.add_argument('--service_workers', type=int, help='uvicorn workers')
    parser.add_argument('--db_host', type=str, help='database host address')
    parser.add_argument('--db_port', type=int, help='database port')
    parser.add_argument('--db_user', type=str, help='database user')
    parser.add_argument('--db_catalog', type=str, help='database catalog')
    parser.add_argument('--db_schema', type=str, help='database schema')
    parser.add_argument('--ollama_host', type=str, help='ollama host address')
    parser.add_argument('--common_model_name', type=str, help='common model name')
    parser.add_argument('--sql_model_name', type=str, help='sql model name')

    args = parser.parse_args()
    apiservice(
        service_host=args.service_host,
        service_port=args.service_port,
        service_reload=args.service_reload,
        service_workers=args.service_workers,
        db_host=args.db_host,
        db_port=args.db_port,
        db_user=args.db_user,
        db_catalog=args.db_catalog,
        db_schema=args.db_schema,
        ollama_host=args.ollama_host,
        common_model_name=args.common_model_name,
        sql_model_name=args.sql_model_name
    )


"""
python main.py \
    --service_host {your_service_host} --service_port {your_service_port} --service_workers {your_workers_num)} \
    --db_host {your_database_host} --db_port {your_database_port} --db_user {your_database_user} --db_catalog {only "hive" supported} --db_schema {your_default_schema} \
    --ollama_host {your_ollama_host} \
    --common_model_name {model_name_in_your_ollama_model_list} \
    --sql_model_name {model_name_in_your_ollama_model_list}
"""