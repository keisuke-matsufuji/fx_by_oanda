import boto3
import os

# import settings

def lambda_handler(event, context):

    print('run')

    # message = settings.ENV_PARAM_TEST
    message = os.environ.get("ENV_PARAM_TEST", None)

    print('message')
    print(message)

    endpoint_url = os.environ.get("DYNAMODB_ENDPOINT", None)
    dynamodb = boto3.client('dynamodb', 
                            endpoint_url=endpoint_url,
                            region_name='us-west-2',
                            )

    print('dynamodb')
    print(dynamodb)

    # print('反映されている')

    print('all done')