import os
import sys
# layerにあがっているpythonモジュール群を参照するため、pathを追加
sys.path.append('/opt')
sys.path.append('/opt/python')
import boto3

# import settings

def lambda_handler(event, context):

    print('run')
    print('sys.path:', sys.path)

    # message = settings.ENV_PARAM_TEST
    message = os.environ.get("ENV_PARAM_TEST", None)

    print('message')
    print(message)

    endpoint_url = os.environ.get("DYNAMODB_ENDPOINT", None)

    print('endpoint_url')
    print(endpoint_url)

    dynamodb = boto3.client('dynamodb', 
                            endpoint_url=endpoint_url,
                            region_name='us-west-2',
                            )

    print('dynamodb')
    print(dynamodb)

    print('反映されている')
    print('反映されている2!!!')

    print('all done')