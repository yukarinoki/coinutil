import ar
import time

initial_amount=10000
initial_coin="USDT"

print("initial asset "+str(initial_amount)+" "+initial_coin)

arb = ar.Arbitrage(initial_coin, initial_amount*1000000000000000000)

while True:
    time.sleep(5)
    arb.check()
    arb.print()

