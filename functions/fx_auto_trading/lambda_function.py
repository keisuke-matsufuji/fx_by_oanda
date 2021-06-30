import os
import sys
import time
import datetime
from decimal import Decimal
# layerにあがっているpythonモジュール群を参照するため、pathを追加
sys.path.append('/opt')
sys.path.append('/opt/python')
import boto3
# 自作モジュールのインポート
# from ディレクトリ名 import モジュール名
from db import price_log
from api import oanda_api

# Lambda Handler
def lambda_handler(event, context):
    i = 1
    # while i < 5000:
    while i < 2:
        # 現在日時
        now = datetime.datetime.now()
        # current_date_time = "{0:%Y-%m-%d %H:%M:%S}".format(now)

        # 最新ローソク足日時・時刻
        Api = oanda_api.OandaApi()
        candle_data = Api.get_candles("M1", -1)

        # 最新ローソク足データが現在日付と一致していない場合（市場が閉まっていた場合）、処理を終了する
        if now - candle_data["candle_date_time"] > datetime.timedelta(minutes=2):
            print('処理を終了する')
            return

        # ------------------ 
        # メイン処理
        # ------------------
        # 前回データをDBから取得
        PriceLog = price_log.PriceLog()
        last_data = PriceLog.get_item(candle_data["candle_date"])
        # 現在日時でDBデータの取得ができなかった場合（当日初回実行時）、前日日付でデータ取得（取得できるまで）
        if len(last_data) == 0:
            return


        # last_date = last_data[0]['date']
        # last_time = last_data[0]['time']

        # 前回のフラグ情報をセット
        info = {
            'buy_signal'  : last_data[0]['buy_signal'],
            'buy_position': last_data[0]['buy_position'],
        }

        # ローソク足データ出力
        Api.print_price(candle_data)
        # 買いポジションを持っていた場合
        if info['buy_position']:
            info = Api.judge_close_buy_position(candle_data, last_data[0], info)
        else:
            info = Api.buy_signal(candle_data, info)
        # シグナルとポジション情報・価格をDBに登録
        params = {
            'date'        : candle_data["candle_date"],
            'time'        : candle_data["candle_time"],
            'open_price'  : Decimal(str(candle_data['open_price'])),
            'close_price' : Decimal(str(candle_data['close_price'])),
            'buy_signal'  : info["buy_signal"],
            # 'sell_signal': 0,
            'buy_position': info["buy_position"],
            # 'sell_position': False,
        }
        PriceLog.put_item(params)
        
        i += 1
        # Api.exec_buy_order()
        # Api.close_buy_position()
        # PositionLog = position_log.PositionLog()
        # PositionLog.get_item()
        time.sleep(60)

    print('all done')