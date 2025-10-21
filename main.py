from database import query_db
import json
import os

def main(event, context):
    http_method = event['requestContext']['http']['method']
    if http_method == 'POST':

        raw_path = event['rawPath']
        path_parts = raw_path.split('/')

        if len(path_parts) == 3 and path_parts[1] == 'resources':
            res_id_str = path_parts[2]
            res_id = int(res_id_str)

            result = query_db(res_id)
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