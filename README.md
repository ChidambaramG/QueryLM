# QueryLM

A natural language to SQL query interface powered by Large Language Models. QueryLM allows users to interact with databases using plain English, with built-in safety measures and elegant result formatting.

## Key Features

- 🤖 Natural Language to SQL conversion using Together AI's Qwen2.5-Coder model
- 🛡️ Built-in SQL injection prevention and query validation
- 📊 Automatic result formatting with markdown tables
- 🔍 Schema-aware query generation
- 🌐 User-friendly Gradio web interface

## Quick Start

1. Copy the example environment file and set up your variables:

```bash
cp .env.example .env
```

Then configure your environment variables in `.env`:

```bash
DB_HOST=your_host
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=your_database
TOGETHER_API_KEY=your_api_key
```

2. Install dependencies:

```
bash
pip install -r requirements.txt 
```

3. Run the application:

```
bash
python app.py
```


## Architecture

- `app.py`: Gradio web interface and main application logic
- `llm_handler.py`: LLM integration for query generation
- `agents.py`: Query analysis and execution components
- `db_connector.py`: Database connection and schema management

## Security Features

- Query validation against common SQL injection patterns
- Restricted query execution with analysis
- Maximum row limit protection

## Requirements

- Python 3.10+
- MySQL database
- Together AI API key