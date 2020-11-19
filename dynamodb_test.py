import boto3
import settings

# dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:5984",
#                             region_name='us-west-2',
#                             aws_access_key_id='ACCESS_ID',
#                             aws_secret_access_key='ACCESS_KEY')

# 開発環境ではaws-cliに下記内容で環境変数を設定
# export AWS_DEFAULT_REGION=us-west-2     # デフォルトリージョン   
# export AWS_ACCESS_KEY_ID=ACCESS_ID     # アクセスキー
# export AWS_SECRET_ACCESS_KEY=ACCESS_KEY  # シークレットアクセスキー

# dynamodb = boto3.client('dynamodb', endpoint_url="http://localhost:5984")
dynamodb = boto3.client('dynamodb', endpoint_url=settings.DYNAMODB_ENDPOINT)

print('dynamodb')
print(dynamodb)

# table = dynamodb.create_table(
#     TableName='users',
#     KeySchema=[
#         {
#             'AttributeName': 'user_id',
#             'KeyType': 'HASH'
#         }
#     ],
#     AttributeDefinitions=[
#         {
#             'AttributeName': 'user_id',
#             'AttributeType': 'N'
#         }
#     ],
#     ProvisionedThroughput={
#         'ReadCapacityUnits': 5,
#         'WriteCapacityUnits': 5
#     }
# )

# print('Table :', table)
# print('Table status:', table.table_status)

tables = dynamodb.list_tables()

print('Tables List:',tables['TableNames'])