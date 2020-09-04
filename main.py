import ar
import time

print


initial_amount=10000

arb = ar.Arbitrage("USDT", initial_amount*1000000000000000000)

while True:
    time.sleep(5)
    arb.check()
    arb.print()


