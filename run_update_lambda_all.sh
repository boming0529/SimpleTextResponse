#!/bin/bash
set -e

FUNCTION_NAME="SimpleTextResponse"
AWS_REGION="us-west-2"
AWS_PROFILE="default"
ZIP_FILE_NAME="pg_query_lambda.zip"
DOCKER_IMAGE="amazon/aws-lambda-python:3.13-arm64"

echo "1. start to package..."
rm -f $ZIP_FILE_NAME
rm -rf psycopg2*

echo "2. using Docker install and Lambda env Python Lib..."
docker run --rm -v "$(pwd):/var/task" \
--entrypoint "/bin/sh" \
$DOCKER_IMAGE \
-c "pip install -r /var/task/requirements.txt -t /var/task"

echo "3. zip..."
zip -r9 $ZIP_FILE_NAME main.py database.py psycopg2*

echo "4. update and deploy Lambda function..."
docker run --rm -v ~/.aws:/root/.aws -v $(pwd):/aws amazon/aws-cli \
    lambda update-function-code \
    --function-name $FUNCTION_NAME \
    --zip-file fileb://$ZIP_FILE_NAME \
    --region $AWS_REGION \
    --profile $AWS_PROFILE

echo "✅ Lambda function: $FUNCTION_NAME !"