import ar
import time

arb = ar.Arbitrage("USDT", 9400000000000000000)

while True:
    time.sleep(5)
    arb.check()
    arb.print()

