import gradio as gr
from llm_handler import QueryLLM
from db_connector import DatabaseConnector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the database connector
db_connector = DatabaseConnector(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)

# Initialize the QueryLLM
query_llm = QueryLLM(
    api_key=os.getenv('TOGETHER_API_KEY'),
    db_connector=db_connector
)

def process_query(message: str, history: list) -> str:
    try:
        result = query_llm.process_user_input(message)
        
        if 'error' in result:
            return f"Error: {result['error']}\n\nQuery attempted:\n```sql\n{result['query']}\n```"
            
        # Format the response with markdown
        response = f"**SQL Query:**\n```sql\n{result['query']}\n```\n\n**Results:**\n"
        
        # Create table headers from the first result
        if result['results']:
            headers = result['results'][0].keys()
            # Create markdown table header
            response += "| " + " | ".join(headers) + " |\n"
            response += "| " + " | ".join(["---" for _ in headers]) + " |\n"
            
            # Add table rows
            for row in result['results']:
                response += "| " + " | ".join(str(row[col]) for col in headers) + " |\n"
            
        if result['trimmed']:
            response += f"\n*(Showing first 5 rows out of {result['total_rows']} total rows)*"
            
        return response
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Create the Gradio interface
iface = gr.ChatInterface(
    fn=process_query,
    title="Database Query Agent",
    description="Ask questions about your database in natural language",
    theme="default",
    examples=[
        "Show me the employee names and their departments",
        "What is the average salary of employees?",
        "What are the departments with the highest average salary?"
    ]
)

if __name__ == "__main__":
    iface.launch(share=False) 