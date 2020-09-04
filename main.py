import ar
import time
import datetime

initial_amount=10000
initial_coin="USDT"

print("initial asset "+str(initial_amount)+" "+initial_coin)
arb = ar.Arbitrage(initial_coin, initial_amount*1000000000000000000)
itr = 0

while True:
    time.sleep(5)
    arb.check(realmode=True)
    ct = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    print(str(ct) + ": itr = " + str(itr))
    arb.print()
    itr = itr + 1

