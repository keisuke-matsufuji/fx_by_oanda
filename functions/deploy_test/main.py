import boto3

# import settings

def lambda_handler(event, context):

    print('run')

    message = settings.ENV_PARAM_TEST

    print('message')
    print(message)

    dynamodb = boto3.client('dynamodb', endpoint_url=settings.DYNAMODB_ENDPOINT)

    print('dynamodb')
    print(dynamodb)

    print('all done')