import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# 環境変数の値を代入
ACCOUNT_ID = os.environ.get("API_ACCOUNT_ID") 
ACCESS_TOKEN = os.environ.get("API_ACCESS_TOKEN") 