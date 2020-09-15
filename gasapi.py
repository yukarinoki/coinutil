import requests
import json

def transaction_fee(from_coin="USDT",to_coin="USDC",dex="Uniswap"):

    gas_limit = 150000 #通貨ペアごと、取引所ごとに違う。Uniswapは150000
    GAS_API_KEY = "1fad4079916a4fdb95bf5a1b433c1357184575f81dc6513d7f3e3d0bb4ac"
    gas_apiurl = "https://ethgasstation.info/api/ethgasAPI.json?" + GAS_API_KEY
    gas_price= int(requests.get(gas_apiurl).json()["fast"] )/ 10
    consume_ratio = 0.5

    binance_ETH_apiurl="https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"
    ETH_price = float(requests.get(binance_ETH_apiurl).json()["price"])

    fee =  gas_limit * consume_ratio * gas_price /1000000000 * ETH_price

    return fee

if __name__ == "__main__":
    print(transaction_fee())