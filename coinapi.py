import requests

baseurl = "https://api.1inch.exchange/v1.1/quote?"

# fromTokenSymbol=DAI&toTokenSymbol=sUSD&amount=1000000000000000000000
n18 = 1000000000000000000
n6 = 1000000
n12 = 1000000000000
coin_list = {"DAI": 18, "USDC": 6, "USDT": 6, "TUSD": 18, "BUSD": 18, "sUSD": 18}
dex_list = {"Uniswap V2":"Uniswap V2", "Curve":"Curve.fi,Curve.fi v2,Curve.fi iearn,Curve.fi BUSD,Curve.fi sUSD,Curve.fi PAX","Balancer":"Balancer","Swerve":"Swerve.fi","Mooniswap":"Mooniswap","Sushi Swap":"Sushi Swap","Pathfinder":"Pathfinder","Oasis":"Oasis","Uniswap":"Uniswap","Kyber":"Kyber","Bancor":"Bancor","PMM2":"PMM2","0x Relays":"0x Relays", "PMM":"PMM", "AirSwap":"AirSwap", "DODO":"DODO", "dForce Swap":"dForce Swap", "mStable":"mStable"}


def CoinIsValid(coin_name):
    return coin_name in coin_list
def DexIsValid(dex_name):
    return dex_name in dex_list

def get_coin_amount(from_coin, to_coin, amount, dex_valid=["Uniswap V2","Curve","Balancer","Swerve"], DEBUG=False):
    dex_used = {}
    to_amount = 0
    
    if (not CoinIsValid(from_coin)) or (not CoinIsValid(to_coin)):
        raise ValueError("Coin name is not contained by coinapi.coin_list")
    if not all(DexIsValid(i) for i in dex_valid):
        raise ValueError("Dex name is not contained by coinapi.dex_list")
        
    footurl = "&disabledExchangesList="
    for dex in dex_list:
        if dex not in dex_valid:
            if footurl != "&disabledExchangesList=":
                footurl = footurl + ","
            footurl = footurl + dex_list[dex]        

    apiurl =  baseurl + "fromTokenSymbol=" + from_coin + "&toTokenSymbol=" + to_coin + "&amount=" + str(int(amount / n12 if coin_list[from_coin] == 6 else amount)) + footurl
    if __name__ == '__main__':
        print(apiurl)
    try:
        res = requests.get(apiurl).json()
    except Exception as e:
        print(e)
        return {"to_amount":to_amount, "dex_used":dex_used, "Error": "API request Error"}

    if DEBUG: print(res)

    if not "toToken" in res:
        if __name__ == '__main__':
            print("cannot exchange in" + str(dex_valid) + ":  from " + from_coin + ", to: " + to_coin)
        return {"to_amount":to_amount, "dex_used":dex_used, "Error": "cannot exchange in" + str(dex_valid) + ":  from " + from_coin + ", to: " + to_coin}

    for exch in res["exchanges"]:
        if exch["part"] != 0:
            dex_used[exch["name"]] = exch["part"]
    
    if res["toToken"]["decimals"] == 6:
        to_amount = int(res["toTokenAmount"]) * n12
    else:
        to_amount = int(res["toTokenAmount"])
    
    return {"to_amount":to_amount, "dex_used": dex_used}

def Uniswapv2(from_coin, to_coin, amount, DEBUG=False):
    return get_coin_amount(from_coin, to_coin, amount, dex_valid=["Uniswap V2"], DEBUG=DEBUG)["to_amount"]
def Curve(from_coin, to_coin, amount, DEBUG=False):
    return get_coin_amount(from_coin, to_coin, amount, dex_valid=["Curve"], DEBUG=DEBUG)["to_amount"]
def Balancer(from_coin, to_coin, amount, DEBUG=False):
    return get_coin_amount(from_coin, to_coin, amount, dex_valid=["Balancer"], DEBUG=DEBUG)["to_amount"]
def Swerve(from_coin, to_coin, amount, DEBUG=False):
    return get_coin_amount(from_coin, to_coin, amount, dex_valid=["Swerve"], DEBUG=DEBUG)["to_amount"]


def best_dex(from_coin, to_coin, amount, dex_valid = ["Uniswap V2","Curve","Balancer","Swerve"]):
    best_amount = 0
    a_dex_used = "None"
    for dex in dex_valid:
        output = get_coin_amount(from_coin, to_coin, amount, [dex])
        if output["to_amount"] > best_amount:
            best_amount = output["to_amount"]
            a_dex_used = list(output["dex_used"].keys())[0]
    return {"to_amount":best_amount, "dex_used":a_dex_used}

if __name__ == '__main__':
    print(best_dex("USDT","DAI",n18*10000))
    print(best_dex("USDT","DAI",n18*1000))
    print(best_dex("USDT","DAI",n18*100))
    print(best_dex("USDT","DAI",n18*10))
    print(best_dex("USDT","DAI",n18*1))
    print("====================")
    print(get_coin_amount("USDT","DAI",n18*10000))
    print(get_coin_amount("USDT","DAI",n18*1000))
    print(get_coin_amount("USDT","DAI",n18*100))
    print(get_coin_amount("USDT","DAI",n18*10))
    print(get_coin_amount("USDT","DAI",n18*1))
    
