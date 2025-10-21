import psycopg2
import json
import os
import datetime

def json_converter(o):
    if isinstance(o, (datetime.datetime, datetime.date)):
        return o.isoformat()
    raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")

def query_db(res_id):
    connection = psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        port=os.environ.get('DB_PORT')
    )
    
    try:
        with connection.cursor() as cursor:
            table_name = os.environ.get('TABLE_NAME')
            primary_key = os.environ.get('PRIMARY_KEY')
            sql_query = f"SELECT * FROM {table_name} WHERE {primary_key} = %s"
            cursor.execute(sql_query, (res_id,))
            
            column_names = [desc[0] for desc in cursor.description]
            results = [dict(zip(column_names, row)) for row in cursor.fetchall()]
            if results:
                # 將結果轉為 JSON 格式返回
                return json.dumps(results, default=json_converter, indent=4, ensure_ascii=False)
            else:
                return json.dumps({'message': 'No data found'}, ensure_ascii=False)
    finally:
        connection.close()
