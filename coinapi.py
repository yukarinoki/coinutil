import requests

baseurl = "https://api.1inch.exchange/v1.1/quote?"
FOOTURL = "&disabledExchangesList=Pathfinder,Oasis,Uniswap,Kyber,Balancer,Bancor,PMM2,0x Relays,Mooniswap,PMM,AirSwap,DODO,dForce Swap,mStable"
# fromTokenSymbol=DAI&toTokenSymbol=sUSD&amount=1000000000000000000000
n18 = 1000000000000000000
n6 = 1000000
n12 = 1000000000000
coin_list = {"DAI": 18, "USDC": 6, "USDT": 6, "TUSD": 18, "BUSD": 18, "sUSD": 18}
transaction_fee = 0

def CoinNameIsValid(coin_name):
    return coin_name in coin_list

def get_coin_amount(from_coin, to_coin, amount, footurl = FOOTURL, DEBUG=False):
    if (not from_coin in coin_list) or (not to_coin in coin_list):
        return 0

    apiurl =  baseurl + "fromTokenSymbol=" + from_coin + "&toTokenSymbol=" + to_coin + "&amount=" + str(int(amount / n12 if coin_list[from_coin] == 6 else amount)) + footurl
    res = requests.get(apiurl).json()
    if DEBUG:
        print(res)
    to_amount = 0

    if not "toToken" in res:
        print("cannot exchange in UniswapV2:  from " + from_coin + ", to: " + to_coin)
        # print(res)
        return 0
    
    if res["toToken"]["decimals"] == 6:
        to_amount = int(res["toTokenAmount"]) * n12
    else:
        to_amount = int(res["toTokenAmount"])
    
    return to_amount

def Uniswapv2(from_coin, to_coin, amount, DEBUG=False):
    return get_coin_amount(from_coin, to_coin, amount, footurl = FOOTURL + ",Curve.fi v2,Curve.fi iearn,Curve.fi BUSD,Curve.fi sUSD,Curve.fi PAX", DEBUG=DEBUG)
def Curve(from_coin, to_coin, amount):
    return get_coin_amount(from_coin, to_coin, amount, footurl = FOOTURL + ",Uniswap V2")