import requests
import json

def transaction_fee(dex):

    GAS_API_KEY = "1fad4079916a4fdb95bf5a1b433c1357184575f81dc6513d7f3e3d0bb4ac"
    gas_apiurl = "https://ethgasstation.info/api/ethgasAPI.json?" + GAS_API_KEY
    gas_price= int(requests.get(gas_apiurl).json()["fast"] )/ 10
    consumed_ratio = 0.5

    binance_ETH_apiurl="https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"
    ETH_price = float(requests.get(binance_ETH_apiurl).json()["price"])

    if dex == "Uniswap V2":
        gas_limit = 150000
    elif dex == "Curve.fi" or dex == "Curve.fi iearn" or dex == "Curve.fi PAX":
        gas_limit = 1600000
    elif dex == "Curve.fi sUSD":
        gas_limit = 300000
    elif dex == "Balancer":
        swap_pool_num = 3 # 10000$だと3くらい必要
        gas_limit = 360000 * swap_pool_num
    elif dex == "Swerve.fi":
        gas_limit = 200000
    else:
        print("transaction fee is unknown")
        gas_limit = 1000000

    fee =  gas_limit * consumed_ratio * gas_price /1000000000 * ETH_price
    return fee

if __name__ == "__main__":
    print(transaction_fee("Uniswap V2"))