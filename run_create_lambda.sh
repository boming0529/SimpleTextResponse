#!/bin/bash

set -e

FUNCTION_NAME="SimpleTextResponse"
AWS_REGION="us-west-2"
AWS_PROFILE="default"
ZIP_FILE_NAME="pg_query_lambda.zip"

LAMBDA_ROLE_ARN="arn:aws:iam::YOUR_AWS_ACCOUNT_ID:role/YOUR_LAMBDA_EXECUTION_ROLE"
HANDLER_NAME="main.main" # endpoint： fineName.functionName
RUNTIME="python3.13"
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
zip -r9 $ZIP_FILE_NAME . -x "*.zip" "*.sh" ".venv/*" ".git/*" "README.md"

echo "4. create new Lambda function..."
aws lambda create-function \
    --function-name $FUNCTION_NAME \
    --zip-file fileb://$ZIP_FILE_NAME \
    --architectures arm64 \
    --handler $HANDLER_NAME \
    --runtime $RUNTIME \
    --role $LAMBDA_ROLE_ARN \
    --region $AWS_REGION \
    --profile $AWS_PROFILE
    

echo "✅ Lambda function: $FUNCTION_NAME !"