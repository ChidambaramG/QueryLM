from typing import List, Dict, Any
import re
from db_connector import DatabaseConnector

class QueryAnalyzer:
    def __init__(self, schema_info: Dict[str, List[str]]):
        self.schema_info = schema_info
        
    def validate_query(self, query: str) -> bool:
        # Basic SQL injection prevention
        dangerous_patterns = [
            r';\s*\w',     # Multiple statements (only if followed by another command)
            r'--\s+',      # SQL comments (allowing dashes in table/column names)
            r'/\*.*?\*/',  # Multi-line comments
            r'xp_\w+',     # Extended stored procedures
            r'exec\s+\w+', # EXEC statements
            r'union\s+all', # UNION ALL attacks
            r'union\s+select', # UNION SELECT attacks
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                return False
                
        return True
        
    def analyze_query(self, query: str) -> Dict[str, Any]:
        return {
            'is_valid': self.validate_query(query),
            'tables_referenced': self._extract_referenced_tables(query),
            'type': self._determine_query_type(query)
        }
        
    def _extract_referenced_tables(self, query: str) -> List[str]:
        # Simple table extraction - could be enhanced
        tables = []
        for table in self.schema_info.keys():
            if table.lower() in query.lower():
                tables.append(table)
        return tables
        
    def _determine_query_type(self, query: str) -> str:
        query = query.lower().strip()
        if query.startswith('select'):
            return 'SELECT'
        elif query.startswith('insert'):
            return 'INSERT'
        elif query.startswith('update'):
            return 'UPDATE'
        elif query.startswith('delete'):
            return 'DELETE'
        return 'UNKNOWN'

class QueryExecutor:
    def __init__(self, db_connector: DatabaseConnector):
        self.db_connector = db_connector
        
    def execute(self, query: str, max_rows: int = 5) -> Dict[str, Any]:
        results = self.db_connector.execute_query(query)
        
        return {
            'query': query,
            'results': results[:max_rows],
            'total_rows': len(results),
            'trimmed': len(results) > max_rows
        } 