from typing import Dict, Any
import dspy
from agents import QueryAnalyzer, QueryExecutor
from db_connector import DatabaseConnector

class QueryLLM:
    def __init__(self, api_key: str, db_connector: DatabaseConnector):
        self.together_api_key = api_key
        self.db_connector = db_connector
        self.schema_info = db_connector.get_schema_info()
        self.query_analyzer = QueryAnalyzer(self.schema_info)
        self.query_executor = QueryExecutor(db_connector)
        
        # Initialize Together AI LLM
        self.lm = dspy.LM("openai/Qwen/Qwen2.5-Coder-32B-Instruct",
                         api_key=self.together_api_key,
                         api_base="https://api.together.xyz/v1",
                         max_tokens=20000)
        dspy.configure(lm=self.lm)
        
    def process_user_input(self, user_input: str) -> Dict[str, Any]:
        # Get SQL query from LLM
        result = self._generate_sql_query(user_input)
        # Extract query from between ```sql and ``` tags
        query = result.split("```sql")[1].split("```")[0].strip()
        print(query)
        # Analyze the query
        analysis = self.query_analyzer.analyze_query(query)
        
        if not analysis['is_valid']:
            return {'error': 'Invalid or potentially harmful query detected'}
            
        # Execute the query
        result = self.query_executor.execute(query)
        return result
        
    def _generate_sql_query(self, user_input: str) -> str:
        # Create a prompt that includes schema information
        schema_context = "Database schema:\n"
        for table, columns in self.schema_info.items():
            schema_context += f"Table {table}: {', '.join(columns)}\n"
            
        prompt = f"""You are a SQL query generator. Generate only the SQL query without any explanation.
        You must enclose the sql query in ```sql <Query> ``` tags.

        {schema_context}

        User question: {user_input}

        Generate a SQL query to answer this question."""
        print(prompt)
        # Get response from Together AI
        result = self.lm(prompt)[0]
        return result.strip() 