import sys
import datetime
from decimal import Decimal
# layerにあがっているpythonモジュール群を参照するため、pathを追加
sys.path.append('/opt')
sys.path.append('/opt/python')
# 自作モジュールのインポート
# from ディレクトリ名 import モジュール名
from db import price_log
from api import oanda_api

# Lambda Handler
def lambda_handler(event, context):
    i = 1
    # while i < 5000: // Local 動作確認用
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
        # TODO:前回データをログに出力
        # print('last_data', last_data)
        # 現在日時でDBデータの取得ができなかった場合（当日初回実行時）、前日日付でデータ取得（取得できるまで）
        if len(last_data) == 0:
            loop_flg = True
            loop_count = 1
            while loop_flg:
                pre_date =  str(datetime.datetime.strptime(
                    candle_data["close_time"].split('.')[0] + '+00:00',
                    '%Y-%m-%dT%H:%M:%S%z')
                    + datetime.timedelta(days=-loop_count)
                )
                print('pre_date', pre_date)
                last_data = PriceLog.get_item(pre_date)
                if len(last_data) > 0:
                    loop_flg = False
                    break
                loop_count += 1
                if loop_count == 3:
                    params = {
                        'date'        : candle_data["candle_date"],
                        'time'        : candle_data["candle_time"],
                        'open_price'  : Decimal(str(candle_data['open_price'])),
                        'close_price' : Decimal(str(candle_data['close_price'])),
                        'buy_signal'  : 0,
                        # 'sell_signal': 0, // TODO：売り注文は現時点で未実装
                        'buy_position': False,
                        # 'sell_position': False, // TODO：売り注文は現時点で未実装
                    }
                    PriceLog.put_item(params)
                    print('DBからデータの取得ができなかったため、ローソク足データを格納し処理を終了')
                    return


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
            # 'sell_signal': 0, // TODO：売り注文は現時点で未実装
            'buy_position': info["buy_position"],
            # 'sell_position': False, // TODO：売り注文は現時点で未実装
        }
        PriceLog.put_item(params)
        
        i += 1

        # TODO：開発環境用
        # Api.exec_buy_order()
        # Api.close_buy_position()
        # PositionLog = position_log.PositionLog()
        # PositionLog.get_item()
        # time.sleep(60)

    print('all done')