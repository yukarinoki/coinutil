import requests
import json
import coinapi
import os

n18 = 1000000000000000000

API_KEY = "HNAEZWNGRX3BT15NG7PWEZC1CJZDM1G4Z2"
MEW_ADDRESS = "0x751BF82449F4D8Ac4E8524E920F33D5849C995be"


contract_address_list = {}
ethToken_path = os.path.join(os.path.dirname(__file__), "ethTokens.json")
tokens = json.load(open(ethToken_path, "r"))



for cn_info in tokens:
    if cn_info["symbol"] in coinapi.coin_list:
        contract_address_list[cn_info["symbol"]] = cn_info["address"]


baseurl = "https://api.etherscan.io/api?"

def get_account_balance(coin_name,address=MEW_ADDRESS,api_key=API_KEY):
    if coin_name == "ETH":
        apiurl = baseurl + "module=account&action=balance&address=" + MEW_ADDRESS + "&tag=latest&apikey="+ API_KEY
    else:
        apiurl = baseurl + "module=account&action=tokenbalance&contractaddress=" + contract_address_list[coin_name] + "&address=" + MEW_ADDRESS + "&tag=latest&apikey="+ API_KEY
    res = requests.get(apiurl).json()
    if "result" in res:
        coin_amount = int(res["result"]) /n18
        return coin_amount
    else:
        print(res)
        return 0

def get_max_coin():
    max_coin_amount = 0
    max_coin = "No stable coin"
    for cn in coinapi.coin_list:
        coin_amount = get_account_balance(cn)
        if coin_amount > max_coin_amount:
            max_coin_amount = coin_amount
            max_coin = cn
    return {"coin_name": max_coin, "coin_amount": max_coin_amount}


if __name__ ==  "__main__":
    print(get_account_balance("DAI"))
    print(get_account_balance("ETH"))
    print(get_max_coin())
    
