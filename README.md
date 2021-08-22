# OANDA APIを用いたFX自動売買

## どうやったか

### 取引口座
OANDAという会社がREST APIを公開しています。
指定通貨ペアのローソク足価格データ取得・新規注文処理・ポジションの決済処理など、
FX市場で行うことを、APIで操作することができます。
（意外とFX取引のAPIを公開している会社は少ない）

日本版の公式ホームページ  
https://developer.oanda.com/docs/jp/

※2021/8/22現在、日本版のOANDA APIのAPIトークンについては発行が一時停止となっているようです。  
https://www.oanda.jp/info/758


また、日本版のOANDA APIはv1、それ以外の国ではv20(バージョン2)が使われているため、私は米国版OANDAで口座を作成しました。
なお、口座はデモアカウントとして作成可能で、自動売買についてはデモの口座で実施することが可能です。


### 本番環境
下記環境でプログラムを実行しています。
- Python 3.8
- AWS Lambda(PythonプログラムをLambda関数として実行)
- DynamoDb
- AWS CloudWatch(Lambda関数の定期実行)


### 開発環境
docker-composeでAWS Lambda + DynamoDB環境の構築を行いました。  
- [Dockerfile](/Dockerfile)
- [docker-compose.yml](/docker-compose.yml)

### CI/CD
Github Actions + Serverless Frameworkを用い、mainブランチにマージがされるとAWS上にデプロイされるような仕組みにしています。  
- [deploy.yml](/.gihub/workflows/deploy.yml)
- [serverless.yml](/functions/fx_auto_trading/serverless.yml)


### プログラムの概略
- FX市場がオープンしている時間帯に、USD_JPYのローソク足データを取得します。  
- 1分置きに価格データを取得し前回の終値よりも価格が上がっている状態(価格+価格の0.005%よりも高い状態)が3回連続で続けば、買いトレンドとし、新規買い注文を発行する
- 買いポジションを持っている状態で、ローソク足データの終値が0.3%下落した場合、下降トレンドに入ったとして、ポジションを決済する
- 買いポジションを持っている状態で、ローソク足データの終値が0.5%上昇した場合、利益確定のためポジションを決済する
