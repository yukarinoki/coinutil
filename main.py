import ar
import time
import datetime

arb = ar.Arbitrage("USDT", 9400000000000000000)
itr = 0
while True:
    time.sleep(5)
    arb.check(realmode=True)
    ct = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    print(str(ct) + ": itr = " + str(itr))
    arb.print()
    itr = itr + 1

