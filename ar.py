import coinapi
import time
swaptime = 180

class Arbitrage:
    def __init__(self, init_coin, init_amount):
        if(not coinapi.CoinNameIsValid(init_coin)):
            raise ValueError("Coin name is not contained by coinapi.coin_list")

        self.current_coin = init_coin
        self.current_amount = init_amount
        self.previous_coin = "None"
        self.maxhistory = {}

        self.maxhistory[init_coin] = init_amount

        for cn in coinapi.coin_list:
            if not cn in self.maxhistory:
                maxamount = 0
                print(cn)
                uniswapv2_amount = coinapi.Uniswapv2(init_coin, cn, init_amount)
                curve_amount = coinapi.Curve(init_coin, cn, init_amount)
                self.maxhistory[cn] = max(uniswapv2_amount, curve_amount)
        
    def check(self, realmode=False):
        check_list = {}
        amount_list = {}
        for cn in coinapi.coin_list:
            if cn != self.current_coin:
                uniswapv2_amount = coinapi.Uniswapv2(self.current_coin, cn, self.current_amount)
                curve_amount = coinapi.Curve(self.current_coin, cn, self.current_amount)
                maxamount =  max(uniswapv2_amount, curve_amount)
                check_list[cn] = maxamount / self.maxhistory[cn]
                amount_list[cn] = maxamount 
        
        print("ValueRatio: "+ str(check_list))
        max_ratio = 1.003
        max_cn = ""

        for cn in check_list:
            if check_list[cn] > max_ratio:
                max_cn = cn
                max_ratio = check_list[cn]
        
        if max_cn == "":
            print("not swap")
            return ""
        else :
            self.previous_coin = self.current_coin
            self.current_coin = max_cn
            self.current_amount = amount_list[max_cn]
            self.maxhistory[max_cn] = amount_list[max_cn]
            print("SWAP!! " + self.previous_coin + "::" + self.current_coin)
            if(realmode):
                time.sleep(swaptime)
            return self.previous_coin + "::" + self.current_coin

    def print(self):
        print("CC: " + self.current_coin + " " + str(self.maxhistory))
    

