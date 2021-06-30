# import json
import os
from os.path import join, dirname
from decimal import Decimal
from dotenv import load_dotenv
import boto3
from boto3.dynamodb.conditions import Key

# 開発環境ではaws-cliに下記内容で環境変数を設定
# export AWS_DEFAULT_REGION=us-west-2     # デフォルトリージョン   
# export AWS_ACCESS_KEY_ID=ACCESS_ID     # アクセスキー
# export AWS_SECRET_ACCESS_KEY=ACCESS_KEY  # シークレットアクセスキー

# print('getenv :', os.getenv('PATH'))
# print('environ :', os.environ['PATH'])

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# boto3取得用変数をenvファイルより取得
endpoint_url = os.environ.get("DYNAMODB_ENDPOINT_LOCAL", None)
aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
# print('endpoint_url :', endpoint_url)
# print('aws_access_key_id :', aws_access_key_id)
# print('aws_secret_access_key :', aws_secret_access_key)


"""
テーブルの作成・取得

"""
def get_table(resource, client, table_name):
    # table = resource.Table(table_name)
    # print('table before:::', table)
    # print('Table status:', table.table_status)
    # テーブル作成 or 取得
    try:
        # table = resource.create_table(
        #     TableName=table_name,
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
        table = resource.create_table(
            TableName = table_name,
            KeySchema = [
                {
                    'AttributeName': 'date',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'time',
                    'KeyType': 'RANGE'
                },
            ],
            AttributeDefinitions = [
                {
                    'AttributeName': 'date',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'time',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput = {
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            },
            # LocalSecondaryIndexes=[
            #     {
            #         'IndexName': 'typeLSIndex',
            #         'KeySchema': [
            #             {
            #                 'AttributeName': 'series',
            #                 'KeyType': 'HASH'
            #             },
            #             {
            #                 'AttributeName': 'type',
            #                 'KeyType': 'RANGE'
            #             }
            #         ],
            #         'Projection': {
            #             'ProjectionType': 'INCLUDE',
            #             'NonKeyAttributes': [
            #                 'name',
            #             ]
            #         }
            #     },
            # ],
            # GlobalSecondaryIndexes=[
            #     {
            #         'IndexName': 'birthHeightGSIndex',
            #         'KeySchema': [
            #             {
            #                 'AttributeName': 'birthday',
            #                 'KeyType': 'HASH'
            #             },
            #             {
            #                 'AttributeName': 'height',
            #                 'KeyType': 'RANGE'
            #             },
            #         ],
            #         'Projection': {
            #             'ProjectionType': 'KEYS_ONLY',
            #         },
            #         'ProvisionedThroughput': {
            #             'ReadCapacityUnits': 1,
            #             'WriteCapacityUnits': 1
            #         }
            #     },
            # ],
        )

    # すでに作成された場合、テーブル名からテーブルを取得
    except client.exceptions.ResourceInUseException:
        table = resource.Table(table_name)
        print('table exception:::', table)

    print('Table :', table)
    print('Table status:', table.table_status)
    return table

"""
テーブルの確認

"""
def check_tables(client):
    tables = client.list_tables()
    print('Tables List:',tables['TableNames'])
    return tables

"""
アイテムの登録

"""
def put_item(resource, table):
    # table.put_item(
    #     Item={
    #         'user_id': 1,
    #         'user_name': 'Keisuke2',
    #         'user_age': 30
    #     }
    # )
    # get_item = table.get_item(Key={'series': 'ミリオンライブ'})
    # print('get_item:',get_item['Item'])

    with table.batch_writer() as batch:
        # item = {
        #     'date': '2021-01-04',
        #     'time': '08:45',
        #     'open_price': Decimal('103.204'),
        #     'close_price': 104,
        #     'buy_signal': 0,
        #     'sell_signal': 0,
        #     'buy_position': False,
        #     'sell_position': False,
        # }
        # batch.put_item(Item = item)

        open_price = 103.204
        close_price = 104.456
        batch.put_item(
            Item={
                'date': '2021-01-04',
                'time': '08:45',
                'open_price': Decimal(str(open_price)),
                'close_price': Decimal(str(close_price)),
                'buy_signal': 0,
                'sell_signal': 0,
                'buy_position': False,
                'sell_position': False,
            }
        )
        # batch.put_item(
        #     Item={
        #         'date': '2021-01-04',
        #         'time': '08:46',
        #         'open_price': 104.332,
        #         'close_price': 105.231,
        #         'buy_signal': 1,
        #         'sell_signal': 0,
        #         'buy_position': False,
        #         'sell_position': False,
        #     }
        # )

"""
アイテムの参照

"""
def get_item(resource, table):
    # getitem(主キー検索)
    # get_item = table.get_item(Key={'series': 'ミリオンライブ'})
    # print('get_item:',get_item['Item'])
    # query_item = table.query(
    #     KeyConditionExpression=Key('user_id').eq(1)
    # )
    query_item1 = table.query(
        KeyConditionExpression=Key('date').eq('2021-01-04')
    )
    print('query_item1:',query_item1['Items'])
    print('query_item1の個数:',query_item1['Count'])
    query_item2 = table.query(
        KeyConditionExpression = Key('date').eq('2021-01-04'),
        ScanIndexForward = False, # 昇順か降順か(デフォルトはTrue=昇順)
        Limit = 1
    )
    print('query_item2:',query_item2['Items'])
    print('query_item2の個数:',query_item2['Count'])
    scan_item = table.scan()
    print('scan_item:',scan_item['Items'])

"""
レコードの削除

"""
def delete_item(resource, table):
    # レコードの全件取得
    items = table.scan()
    print('all item 削除前:', items['Items'])
    # レコード削除
    # table.delete_item(Key={'user_id': 1})
    table.delete_item(
        Key={
            # 'date': {'S':'2021-01-04'},
            # 'time': {'S':'08:45'}
            'date': '2021-01-04',
            'time': '08:45'
        }
    )
    # print('delete_item done')
    # 全件取得
    items = table.scan()
    print('all item 削除後:', items['Items'])

"""
テーブルの削除

"""
def delete_table(resource, client, table):
    table.delete()
    tables = client.list_tables()
    print('Tables All List:',tables['TableNames'])



"""
メイン処理

"""
resource = boto3.resource('dynamodb', 
                        endpoint_url=endpoint_url,
                        region_name='us-west-2',
                        # aws_access_key_id=aws_access_key_id,
                        # aws_secret_access_key=aws_secret_access_key
                        )
client = boto3.client('dynamodb', 
                        endpoint_url=endpoint_url,
                        region_name='us-west-2',
                        )
# テーブル作成 or テーブル取得
# table_name = 'users'
table_name = 'price_data'
table = get_table(resource, client, table_name)

# テーブル確認
# tables = check_tables(client)

# レコード登録
put_item(resource, table)

# レコード参照(get/query/scan)
get_item(resource, table)

# レコード更新

# レコード削除
# delete_item(resource, table)

# テーブル削除
# delete_table(resource, client, table)

print('All Done!!!')


"""
テーブルの作成(idle)

"""
def create_table_idle(resource):
    
    resource.create_table(
        TableName = 'idolmaster',
        KeySchema = [
            {
                'AttributeName': 'series',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'name',
                'KeyType': 'RANGE'
            },
        ],
        AttributeDefinitions = [
            {
                'AttributeName': 'series',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'name',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'type',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'birthday',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'height',
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput = {
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        },
        LocalSecondaryIndexes=[
            {
                'IndexName': 'typeLSIndex',
                'KeySchema': [
                    {
                        'AttributeName': 'series',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'type',
                        'KeyType': 'RANGE'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'INCLUDE',
                    'NonKeyAttributes': [
                        'name',
                    ]
                }
            },
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'birthHeightGSIndex',
                'KeySchema': [
                    {
                        'AttributeName': 'birthday',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'height',
                        'KeyType': 'RANGE'
                    },
                ],
                'Projection': {
                    'ProjectionType': 'KEYS_ONLY',
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                }
            },
        ],
    )