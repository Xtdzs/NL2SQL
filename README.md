# ✨NL2SQL✨

This project is benchmarked against OpenAI's [Chat2DB](https://chat2db-ai.com/) project, aiming to optimize the development experience for non CS-majored developers. Currently, it supports Hive databases and API calls. 

## 🚀 Getting Started

### 1 Clone the repository

```bash
git clone https://github.com/Xtdzs/NL2SQL.git
```

### 2 Install dependencies

First you have to download `Ollama` which we will use later to run our models.

**Linux**

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows**

Please download [this](https://ollama.com/download/OllamaSetup.exe).

**maxOS**

Please download [this](https://ollama.com/download/Ollama-darwin.zip)

Then we focus on installing the python dependences.

MAKE SURE `pip` is available on your device. 

```shell
cd nl2sql_server
pip install -r requirements.txt
```

### 3 Run NL2SQL service

```bash
python main.py \
    --service_host {your_service_host} --service_port {your_service_port} --service_workers {your_workers_num)} \
    --db_host {your_database_host} --db_port {your_database_port} --db_user {your_database_user} --db_catalog {only "hive" supported} --db_schema {your_default_schema} \
    --ollama_host {your_ollama_host} \
    --common_model_name {model_name_in_your_ollama_model_list} \
    --sql_model_name {model_name_in_your_ollama_model_list}
```

**Tips:**

- **About the API service:** If you feel confused on how to set the IP address of your service or some other problems, you could find help by reading the official documents of [FastAPI](https://fastapi.tiangolo.com/). Feel free to ask me if you have any other questions. (committing it as an `issue` is recommended)
- **About the choice of the model:** 
  - Common Model: recommend LLMs with the size **between 7B to 14B**, considering to trade off between the NLU ability and the Latency.
  - SQL Model: recommend **sqlcoder** series LLMs. These models could do a great job in conversing basic NL to SQL. 

## ▶️Use the Service

Congratulations you have started your NL2SQL server! Lets now focus on how to use it.

### 