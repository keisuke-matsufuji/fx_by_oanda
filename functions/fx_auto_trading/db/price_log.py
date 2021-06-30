import os
import sys
# layerにあがっているpythonモジュール群を参照するため、pathを追加
sys.path.append('/opt')
sys.path.append('/opt/python')
import boto3
from boto3.dynamodb.conditions import Key

# DynamoDb Priceクラス
class PriceLog(object):
    """
    クラス変数

    """
    # エンドポイントURL
    endpoint_url = os.environ.get("DYNAMODB_ENDPOINT", None)
    # print('endpoint_url:::', endpoint_url)
    # DynamoDb接続情報取得
    resource = boto3.resource('dynamodb',     
                        endpoint_url=endpoint_url,
                        region_name='us-west-2',
                        )
    client = boto3.client('dynamodb',     
                        endpoint_url=endpoint_url,
                        region_name='us-west-2',
                        )
    table_name = 'price_log'

    # 
    # テーブルの作成・取得
    # 
    def get_table(self):
        # table = resource.Table(table_name)
        # print('table before:::', table)
        # print('Table status:', table.table_status)
        resource = self.resource
        client = self.client
        table_name = self.table_name
        # テーブル作成 or 取得
        try:
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
            )

        # すでに作成された場合、テーブル名からテーブルを取得
        except client.exceptions.ResourceInUseException:
            table = resource.Table(table_name)
        
        return table

    # 
    # アイテムの参照
    # 
    def get_item(self, date):
        # テーブルの取得
        table = self.get_table()
        query_item = table.query(
            KeyConditionExpression = Key('date').eq(date),
            ScanIndexForward = False, # 昇順か降順か(デフォルトはTrue=昇順)
            Limit = 1
        )
        return query_item['Items']
    
    # 
    # アイテムの登録
    #
    def put_item(self, item):
        # テーブルの取得
        table = self.get_table()
        with table.batch_writer() as batch:
            batch.put_item(Item=item)
        