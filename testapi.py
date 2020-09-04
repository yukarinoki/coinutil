import requests

baseurl = "https://api.1inch.exchange/v1.1/quote?"
FOOTURL = "&disabledExchangesList=Pathfinder,Oasis,Uniswap,Kyber,Balancer,Bancor,PMM2,0x Relays,Mooniswap,PMM,AirSwap,DODO,dForce Swap,mStable"
# fromTokenSymbol=DAI&toTokenSymbol=sUSD&amount=1000000000000000000000
n18 = 1000000000000000000
n6 = 1000000
n12 = 1000000000000
coin_list = {"DAI": 18, "USDC": 6, "USDT": 6, "TUSD": 18, "BUSD": 18, "sUSD": 18, "PAX": 18}
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
        print("ERROR:  from " + from_coin + ", to: " + to_coin)
        print(res)
        return 0
    
    if res["toToken"]["decimals"] == 6:
        to_amount = int(res["toTokenAmount"]) * n12
    else:
        to_amount = int(res["toTokenAmount"])
    
    #取引所の確認
    for exch in res["exchanges"]:
        if exch["part"] != 0:
            print("exchange "+str(exch["name"]+":"+str(exch["part"])+"%"))
    
    return to_amount

def Uniswapv2(from_coin, to_coin, amount, DEBUG=False):
    return get_coin_amount(from_coin, to_coin, amount, footurl = FOOTURL + ",Curve.fi v2,Curve.fi iearn,Curve.fi BUSD,Curve.fi sUSD,Curve.fi PAX", DEBUG=DEBUG)
def Curve(from_coin, to_coin, amount):
    return get_coin_amount(from_coin, to_coin, amount, footurl = FOOTURL + ",Uniswap V2")

init_amount=10000*n18


# init_amount=1*n18
# for i in [1,10,100,1000,10000,100000,1000000]:
  
#     print(str(i)+"USDT = "+str(Uniswapv2("USDT","USDC",init_amount*i)/n18)+" USDC")

for cn in coin_list:
    if cn not in ["USDT"]:
        print(cn+ " Uniswapv2:"+str(Uniswapv2("USDT",cn,init_amount)/n18))
        print("     Curve:"+str(Curve("USDT",cn,init_amount)/n18))
        print("   ")
        







