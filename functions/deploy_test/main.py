import pytz


def lambda_handler(event, context):

    print('run')

    jst = pytz.timezone('Asia/Tokyo')
    jst_now = datetime.datetime.now(tz=jst)
    print('jst_now')
    print(jst_now)

    print('all done')