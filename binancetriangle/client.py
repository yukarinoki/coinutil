import ccxt
from datetime import datetime
from datetime import timedelta
import pandas as pd
import numpy as np
import random, string
import requests

def randomid(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k = n))

price_api = 'https://coinanalyza.herokuapp.com/binance/price'
id_api = 'https://coinanalyza.herokuapp.com/binance/id'

# send own id
uid = randomid(8)
id_param = {'id': uid}
response = requests.post(id_api, data=id_param)
print(response)

# 初期準備
pd.set_option('display.max_rows', 1500)  # 省略させない
binance = ccxt.binance()
binance.load_markets()


# 取引ペア取得
while True:
    print(str(datetime.today())[0:19] + ' 全ての取引種を取得')
    Pairlists = list(binance.markets.keys())
    Pl_sum = len(Pairlists)

    print(str(datetime.today())[0:19] + ' ' +  str(Pl_sum) + '種')
    print()

    print(str(datetime.today())[0:19] + ' 全ての取引値を取得')
    cp = datetime.today()
    s = []
    for i in range(Pl_sum):
        name = str(Pairlists[i])
        c1 = name.split("/")[0]
        c2 = name.split("/")[1]
        ask = ccxt.binance().fetch_ticker(Pairlists[i])['ask']
        bid = ccxt.binance().fetch_ticker(Pairlists[i])['bid']

        s.append([name, c1, c2, ask, bid, str(datetime.today())[0:19]])

        price = pd.DataFrame(s, columns=["name", "c1", "c2", "ask", "bid", "time"])

        t = datetime.today() - cp
        if i == 0 or i < 10:
            nj = 0
            nji = 0
        else:
            nj = (Pl_sum - i) * (t.seconds / i)
            if nj > nji != 0:
                nj = nji
            nji = nj
        print('\r  └  ' + str(i)+ '/' + str(Pl_sum) + '  残り ' +'{:,.0f}'.format(nj) + '秒  ' + c1 + '/' + c2 + '  ask:' + '{:.5f}'.format(ask) + '  bid:' + '{:.5f}'.format(bid), end='')

    price = price.set_index("name")

    print()

    # 通貨リスト取得
    print(str(datetime.today())[0:19] + ' 全ての通貨種を取得')
    c = []
    c = price['c1'].tolist() + price['c2'].tolist()

    l = set(c)
    l = sorted(l)

    print(str(datetime.today())[0:19] + ' ' + str(len(l)) + '種')
    print()


    # ルート探索
    # 基礎通貨宣言
    print(str(datetime.today())[0:19] + ' 組み合わせ探索と計算')
    AbiPair = []
    BaseCurrency = ["BTC", "ETH", "USDT", "BNB"]
    mk = 0

    for i0 in range(len(BaseCurrency)):
        T0 = BaseCurrency[i0]
        for i1 in range(len(l)):
            T1 = l[i1]
            if T0 + "/" + T1 in Pairlists or T1 + "/" + T0 in Pairlists:
                # T1確定

                for i2 in range(len(l)):
                    T2 = l[i2]
                    if T2 + "/" + T1 in Pairlists or T1 + "/" + T2 in Pairlists:
                        # T2確定

                        if T2 + "/" + T0 in Pairlists or T0 + "/" + T2 in Pairlists:
                            # ルート確定
                            # 1st buy
                            if T1 + "/" + T0 in price.index.values:
                                buyT1 = 1 / price.at[str(T1 + "/" + T0), 'ask']
                            else:
                                buyT1 = price.at[str(T0 + "/" + T1), 'bid']

                            # 2nd buy
                            if T2 + "/" + T1 in price.index.values:
                                buyT2 = buyT1 / price.at[str(T2 + "/" + T1), 'ask']
                            else:
                                buyT2 = buyT1 * price.at[str(T1 + "/" + T2), 'bid']

                            # 3rd buy
                            if T0 + "/" + T2 in price.index.values:
                                buyT0 = buyT2 / price.at[str(T0 + "/" + T2), 'ask'] - 1
                            else:
                                buyT0 = buyT2 * price.at[str(T2 + "/" + T0), 'bid'] - 1

                            if float('inf') in [buyT1, buyT2, buyT0] or 0 in [buyT1, buyT2, buyT0] :
                               # print(str(datetime.today())[0:19] + '  └ 無効 ' + '  ' + T0 + '/' + T1 + '/' + T2)
                                mk += 1
                            else:
                               # print(str(datetime.today())[0:19] + '  └ calc ' + '  ' + T0 + '/' + T1 + '/' + T2)
                                AbiPair.append([T0, T1, T2, buyT1, buyT2, '{:.5f}'.format(buyT0)])

    AbiPair = pd.DataFrame(AbiPair, columns=["T0", "T1", "T2", "BuyT1", "BuyT2", "BuyT0"])
    AbiPair = AbiPair.sort_values('BuyT0', ascending=False)

    print()
    print('3通貨ルートの総数は ' + str(len(AbiPair)) + ' 種')
    print('(無効値 ' + str(mk) + '種')
    print()
    print()

    pd.set_option('display.max_rows', 6) 
    AbiPair.dropna(subset=['BuyT1', 'BuyT2', 'BuyT0'], inplace=True)

    first_ratio = AbiPair.iloc[0]['BuyT0']
    first_1 = AbiPair.iloc[0]['T0']
    first_2 = AbiPair.iloc[0]['T1']
    first_3 = AbiPair.iloc[0]['T2']
    second_ratio = AbiPair.iloc[1]['BuyT0']
    second_1 = AbiPair.iloc[1]['T0']
    second_2 = AbiPair.iloc[1]['T1']
    second_3 = AbiPair.iloc[1]['T2']
    third_ratio = AbiPair.iloc[2]['BuyT0']
    third_1 = AbiPair.iloc[2]['T0']
    third_2 = AbiPair.iloc[2]['T1']
    third_3 = AbiPair.iloc[2]['T2']

    price_params = {'id': uid, 'first_ratio': first_ratio, 'first_1': first_1, 'first_2': first_2, 'first_3': first_3, 'second_ratio': second_ratio, 'second_1': second_1, 'second_2': second_2, 'second_3': second_3, 'third_ratio': third_ratio, 'third_1': third_1, 'third_2': third_2, 'third_3': third_3 }
    response = requests.post(price_api, data=price_params)
    print(response.text)