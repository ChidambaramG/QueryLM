import mysql.connector
from typing import List, Dict, Any
import logging

class DatabaseConnector:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        self.connection = None
        
    def connect(self) -> None:
        try:
            self.connection = mysql.connector.connect(**self.config)
            logging.info("Successfully connected to the database")
        except Exception as e:
            logging.error(f"Error connecting to database: {str(e)}")
            raise
            
    def get_schema_info(self) -> Dict[str, List[str]]:
        if not self.connection:
            self.connect()
            
        cursor = self.connection.cursor()
        schema_info = {}
        
        try:
            # Get all tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            for table in tables:
                table_name = table[0]
                cursor.execute(f"DESCRIBE {table_name}")
                columns = cursor.fetchall()
                schema_info[table_name] = [col[0] for col in columns]
                
        finally:
            cursor.close()
            
        return schema_info
        
    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        if not self.connection:
            self.connect()
            
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        finally:
            cursor.close() 