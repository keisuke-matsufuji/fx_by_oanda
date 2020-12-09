import requests

def lambda_handler(event, context):
    res = requests.get('https://www.dmm.com/')
    return res.status_code 