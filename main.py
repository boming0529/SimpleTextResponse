from database import query_db
import json
import os

def main(event, context):
    http_method = event['requestContext']['http']['method']
    user_agent = event['headers'].get('user-agent', 'Unknown')
    if http_method == 'POST' and user_agent == os.environ.get('ALLOW_USER_AGENT'):

        raw_path = event['rawPath']
        path_parts = raw_path.split('/')

        if len(path_parts) == 3 and path_parts[1] == 'configs':
            config_id_str = path_parts[2]
            config_id = int(config_id_str)

            result = query_db(config_id)
            if result:
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'application/json; charset=utf-8'
                    },
                    'body': result
                }
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json; charset=utf-8'
        },
        'body': 'No data found'
    }