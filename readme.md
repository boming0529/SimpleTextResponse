

### zip 
```
zip -r9 ../pg_query_lambda.zip main.py database.py psycopg2/ psycopg2_binary.libs/ psycopg2_binary-2.9.10.dist-info/
```

### create lambda function
```
aws lambda create-function \
--function-name SimpleTextResponse \
--zip-file fileb://pg_query_lambda.zip \
--handler main.main \
--runtime python3.11 \
--role arn:aws:iam::YOUR_AWS_ACCOUNT_ID:role/YOUR_LAMBDA_EXECUTION_ROLE \
--profile default \
--region us-west-2
```
where handler <filename>:<functionName>


### update configuration
aws lambda update-function-configuration \
--function-name SimpleTextResponse \
--region us-west-2 \
--environment "Variables={DB_HOST=xxxxxxxxxx.us-west-2.rds.amazonaws.com,DB_NAME=xxxxxxx,DB_USER=xxxxx,DB_PASSWORD=xxxxx,DB_PORT=xxxx,TABLE_NAME=xxxx}"

### update function deployment package (and deployment)
function ARN : arn:aws:lambda:us-west-2:YOUR_AWS_ACCOUNT_ID:function:SimpleTextResponse
```
aws lambda update-function-code \
--function-name SimpleTextResponse \
--zip-file fileb://pg_query_lambda.zip \
--profile default \
--region us-west-2
```
