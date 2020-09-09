import ar
import time
import datetime
import argparse 

parser = argparse.ArgumentParser(description='Performing arbitrage trade of stable coin.') 
parser.add_argument('--realmode', action='store_true')
parser.add_argument('--ratio', type=float, default=1.001)
parser.add_argument('--ratio_sUSD', type=float, default=1.005)
args = parser.parse_args()

initial_amount=10000
initial_coin="USDT"
dex=["Uniswap V2","Curve","Balancer","Swerve"]
#choose from ["Uniswap V2","Curve","Balancer","Swerve","Mooniswap","Pathfinder","Oasis","Uniswap","Kyber","Bancor","PMM2","0x Relays","PMM","AirSwap","DODO","dForce Swap","mStable"]

print("initial asset "+str(initial_amount)+" "+initial_coin)
arb = ar.Arbitrage(initial_coin, initial_amount*1000000000000000000,dex)
itr = 0

while True:
    time.sleep(5)
    arb.check(max_ratio=args.ratio,max_ratio_sUSD = args.ratio_sUSD,dex_valid=dex, realmode=args.realmode)
    ct = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    print(str(ct) + ": itr = " + str(itr))
    # arb.print()
    itr = itr + 1

