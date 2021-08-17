import datetime
import json
import os
import requests
import sys

# layerにあがっているpythonモジュール群を参照するため、pathを追加
sys.path.append('/opt')
sys.path.append('/opt/python')
# import oandapyV20
from oandapyV20 import API
from oandapyV20.endpoints import accounts, instruments, orders, positions
# 自作モジュールのインポート
# from ディレクトリ名 import モジュール名
from db import position_log
# from db.price import Price

# 
# OANDA API エラークラス
# 
class OandaApiError(Exception):
	pass

# 
# OANDA API クラス
# 
class OandaApi(object):
	# 
    # インスタンス変数
    # 
	def __init__(self):
		# OANDAアカウント読み込み
		self.oanda_account_id = os.environ.get("OANDA_API_ACCOUNT_ID")
		self.oanda_access_token = os.environ.get("OANDA_API_ACCESS_TOKEN")
		self.api = API(access_token=self.oanda_access_token, environment="practice")
		self.date = ""
		
	# 
	# ドル円データローソク足を取得する関数
	# 
	# def get_candles(min, i, r):
	def get_candles(self, min, i):
		try:
			params = {
				"count": 5,
				"granularity": "M1"
			}
			instrument = instruments.InstrumentsCandles(instrument="USD_JPY", params=params)
			response = self.api.request(instrument)
			data = response["candles"][i]

			close_time = data["time"]
			candle_d_t =  str(datetime.datetime.strptime(
				data["time"].split('.')[0] + '+00:00',
            	'%Y-%m-%dT%H:%M:%S%z')
				+ datetime.timedelta(hours=9)
			)
			candle_date = candle_d_t[0:10]
			candle_time = candle_d_t[11:16]
			candle_date_time = datetime.datetime.strptime(
				(candle_date + ' ' + candle_time), '%Y-%m-%d %H:%M'
			)
			self.date = candle_date

			# TODO:タイムゾーンの変更
			# close_time = pd.to_datetime(list(data["time"]))

			result = {
				"close_time":       close_time,
				"candle_date":      candle_date,
				"candle_time":      candle_time,
				"candle_date_time": candle_date_time,
				"open_price":       float(data["mid"]["o"]),
				"high_price":       float(data["mid"]["h"]),
				"low_price":        float(data["mid"]["l"]),
				"close_price":      float(data["mid"]["c"])
			}
		except requests.exceptions.ConnectionError as e_HTTP:
			print(response.text)
			print(e_HTTP)
		except Exception as e:
			print(e)
			raise OandaApiError(e)

		return result

	# 
	# 取得データをconsoleに表示する関数	
	# 	
	# def print_price(data):
	def print_price(self, data):
		# print("最新の価格データ")
		print( "時間: " + str(data["candle_date_time"])
					+ " 始値: " + str(data["open_price"])
					+ " 終値: " + str(data["close_price"]) )

	# 
	# 陽線かどうか・ローソク足の上昇率を判定する関数
	# 			
	def check_ascend(self, data):
		if data["close_price"] > data["open_price"]:
			if (data["close_price"] / data["open_price"] - 1) * 100 > 0.005:
				return True

	# 
	# フィルター処理
	# 
	def check_candles(self, data):
		if (data["close_price"] / data["open_price"] - 1) * 100 > 0.005:
			return True

	# 
	# 買いシグナルが出たら買い注文を出す関数
	# 
	def buy_signal(self, candle_data, info):
		# self.exec_buy_order()
		# self.close_buy_position()
		self.get_open_position()
		# ローソク足データの陽線判定
		is_asecend = self.check_ascend(candle_data)
        # フィルター処理判定
		is_checked = self.check_candles(candle_data)
		# ローソク足が陽線の場合、buy_signalをインクリメント
		if is_asecend and is_checked:
			info['buy_signal'] += 1
            # 3回連続で陽線判定の場合
			if info['buy_signal'] == 3:
                # 買い注文処理を入れる
				print('３回連続で陽線が出たので買い！')
				self.exec_buy_order()
				info['buy_position'] = True
				info['buy_signal'] = 0
            # デバッグ用
			if info['buy_signal'] == 2:
				print('２回連続で陽線が出た！！')
		else:
			info['buy_signal'] = 0
		return info
	
	# 
	# 手仕舞いのシグナルが出たら決済注文を出す関数(買い注文の決済)
	# 
	def judge_close_buy_position(self, candle_data, last_data, info):
		positions = self.get_open_position()
		# ローソク足の終値から下降トレンドに入っていると判定した場合、ポジションを決済する
		# 買い注文価格から0.3%下落でポジション決済
		if (positions["long"]["averagePrice"] / candle_data - 1) * 100 > 0.3:
			self.close_buy_position()
			info["buy_position"] = False
			
		# ローソク足の終値から上昇トレンドで利益確定ラインを超えている場合、ポジションを決済する
		# 買い注文価格から0.5%上昇でポジション決済
		if (candle_data / positions["long"]["averagePrice"] - 1) * 100 > 0.5:
			self.close_buy_position()
			info["buy_position"] = False
		
		return info

	# #出した注文が約定しているか確認する関数
	# def check_order(flag):
	# 	#一定時間で注文が通っていなければキャンセルする
	# 	flag["order"] = False
	# 	flag["position"] = True
	# 	return flag

	# ========== 新規注文操作 ==========

	# 
	# 注文方法：成行
	# 取引通貨：USD/JPY
	# 売買：買
	# 数量：10
	# 
	def exec_buy_order(self):
		try:
			data = {
				"order": {
					"instrument": "USD_JPY",
					"units": 10,
					"type": "MARKET",
					"positionFill": "DEFAULT"
				}
			}
			o = orders.OrderCreate(accountID=self.oanda_account_id, data=data)
			response = self.api.request(o)
			print('exec_buy_order response', json.dumps(response, indent=2))
		except requests.exceptions.ConnectionError as e_HTTP:
			print(response.text)
			print(e_HTTP)
		except Exception as e:
			print(e)
			raise OandaApiError(e)
	
	# ========== ポジション操作 ==========

	# 
	# 有効なポジションの取得
	# 
	def get_open_position(self):
		try:
			postion = positions.OpenPositions(accountID=self.oanda_account_id)
			response = self.api.request(postion)
			print('get_open_position response', json.dumps(response, indent=2))
		except requests.exceptions.ConnectionError as e_HTTP:
			print(response.text)
			print(e_HTTP)
		except Exception as e:
			print(e)
			raise OandaApiError(e)
	
	# 
	# 買いポジション決済
	# 数量：全て
	# 
	def close_buy_position(self):
		try:
			data = {
				"longUnits": "ALL"
			}
			positon = positions.PositionClose(
				accountID=self.oanda_account_id, instrument="USD_JPY", data=data
			)
			response = self.api.request(positon)
			result = response["longOrderFillTransaction"]
			print('close_buy_position response', json.dumps(response, indent=2))
			# ポジション決済情報をDBに登録
			params = {
				'position_id': int(result["id"]),
				'date'       : self.date,
				'instrument' : result["instrument"],
				'units'      : result["units"],
				'price'      : result["price"],
				'pl'         : result["pl"],
				'account_balance': result["accountBalance"],
			}
			PositionLog = position_log.PositionLog()
			PositionLog.put_item(params)
		except requests.exceptions.ConnectionError as e_HTTP:
			print(response.text)
			print(e_HTTP)
		except Exception as e:
			print(e)
			raise OandaApiError(e)
	
	# ========== アカウント操作 ==========

	# 
	# アカウント情報の参照
	# 
	def get_account_info(self):
		try:
			account = accounts.AccountSummary(self.oanda_account_id)
			response = self.api.request(account)
			print('get_account_inforesponse', json.dumps(response, indent=2))
		except requests.exceptions.ConnectionError as e_HTTP:
			print(response.text)
			print(e_HTTP)
		except Exception as e:
			print(e)
			raise OandaApiError(e)
		