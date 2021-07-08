import json
import os
import sys
# layerにあがっているpythonモジュール群を参照するため、pathを追加
sys.path.append('/opt')
sys.path.append('/opt/python')
import boto3
from boto3.dynamodb.conditions import Key

# DynamoDb PositionLogクラス
class PositionLog(object):
    """
    クラス変数

    """
    # エンドポイントURL
    endpoint_url = os.environ.get("DYNAMODB_ENDPOINT", None)
    region_name = os.environ.get("DYNAMODB_REGION", None)
    # DynamoDb接続情報取得
    resource = boto3.resource('dynamodb',     
                        endpoint_url=endpoint_url,
                        region_name=region_name,
                        )
    client = boto3.client('dynamodb',     
                        endpoint_url=endpoint_url,
                        region_name=region_name,
                        )
    table_name = 'position_log'

    # 
    # テーブルの作成・取得
    # 
    def get_table(self):
        resource = self.resource
        client = self.client
        table_name = self.table_name
        # テーブル作成 or 取得
        try:
            table = resource.create_table(
                TableName = table_name,
                KeySchema = [
                    {
                        'AttributeName': 'position_id',
                        'KeyType': 'HASH'
                    },
                    # {
                    #     'AttributeName': 'date',
                    #     'KeyType': 'RANGE'
                    # },
                ],
                AttributeDefinitions = [
                    {
                        'AttributeName': 'position_id',
                        'AttributeType': 'N'
                    },
                    # {
                    #     'AttributeName': 'date',
                    #     'AttributeType': 'S'
                    # },
                ],
                ProvisionedThroughput = {
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                },
                # GlobalSecondaryIndexes=[
                #     {
                #         'IndexName': 'dateIndex',
                #         'KeySchema': [
                #             {
                #                 'AttributeName': 'date',
                #                 'KeyType': 'HASH'
                #             },
                #             {
                #                 'AttributeName': 'position_id',
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

        return table

    # 
    # アイテムの参照
    # 
    # def get_item(self, date):
    def get_item(self):
        # テーブルの取得
        table = self.get_table()
        # GSI(セカンダリーインデックス：日付によるソートキー検索)
        # index = self.resource.Table(table)

        # 全件スキャン=>日付で絞り込み
        item = table.scan(
            FilterExpression = Key('date').between('2021-06-28', '2021-07-04')
        )
        # print('item', item)

        # テーブル削除
        # table.delete()

        return item['Items']
    
    # 
    # アイテムの参照
    # 
    def put_item(self, item):
        # テーブルの取得
        table = self.get_table()
        with table.batch_writer() as batch:
            batch.put_item(Item=item)
        