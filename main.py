import ar
import etherscanapi
import time
import datetime
import argparse
import requests

def line_notify(notification_message): # LINEに通知
    line_notify_token = 'bGK1XgQkByxlZLw9Shyuy0q1Bi84tMw8x2gCtjbySnR'#僕のアカウントです、適宜変更してください
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': f'message: {notification_message}'}
    requests.post(line_notify_api, headers = headers, data = data)

parser = argparse.ArgumentParser(description='Performing arbitrage trade of stable coin.') 
parser.add_argument('--realmode', action='store_true')
parser.add_argument('--ratio', type=float, default=1.003)
parser.add_argument('--ratio_high', type=float, default=1.01)
args = parser.parse_args()


# initial_asset = etherscanapi.get_max_coin()#僕のwalletで一番多いstable coinです
# initial_amount = initial_asset["coin_amount"]
# initial_coin = initial_asset["coin_name"]

initial_amount = 10000
initial_coin = "USDC"



dex=["Uniswap V2","Curve","Balancer","Swerve","Sushi Swap"]
#choose from ["Uniswap V2","Curve","Balancer","Swerve","Mooniswap","Sushi Swap","Pathfinder","Oasis","Uniswap","Kyber","Bancor","PMM2","0x Relays","PMM","AirSwap","DODO","dForce Swap","mStable"]

print("initial asset ... "+initial_coin+ " : " + str(initial_amount))
line_notify("initial asset ... "+initial_coin+ " : " + str(initial_amount))
arb = ar.Arbitrage(initial_coin, initial_amount * pow(10,18), dex)
line_notify("Start!! : "+str(arb.maxhistory_unit))
itr = 0

while True:
    ct = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    print(str(ct) + ": itr = " + str(itr))
    res = arb.check(max_ratio=args.ratio, max_ratio_high = args.ratio_high, dex_valid=dex, realmode=args.realmode)
    if res["swap"]:
        line_notify("Swap in　"+ res["dex_used"] +" ... "+ arb.previous_coin +" : "+ str(arb.maxhistory_unit[arb.previous_coin]) + " -> " + arb.current_coin + " : "+str(arb.maxhistory_unit[arb.current_coin]))
        line_notify("maxhistory : "+str(arb.maxhistory_unit))

    arb.print()
    itr = itr + 1

