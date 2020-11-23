import requirements
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# 環境変数の値を代入
DYNAMODB_ENDPOINT = os.environ.get("DYNAMODB_ENDPOINT", None)

ENV_PARAM_TEST = os.environ.get("ENV_PARAM_TEST", None)

OANDA_ACCOUNT_ID = os.environ.get("OANDA_API_ACCOUNT_ID") 
OANDA_ACCESS_TOKEN = os.environ.get("OANDA_API_ACCESS_TOKEN") 