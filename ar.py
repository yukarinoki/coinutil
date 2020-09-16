import coinapi
import gasapi
import time
import requests

transaction_time = 180
n18 = 1000000000000000000
amount_small = 100

class Arbitrage:
    def __init__(self, init_coin, init_amount, dex_valid):
        if(not coinapi.CoinIsValid(init_coin)):
            raise ValueError("Coin name is not contained by coinapi.coin_list")

        self.current_coin = init_coin
        self.current_amount = init_amount
        self.previous_coin = "None"
        self.maxhistory = {}
        self.maxhistory_unit = {}
        self.current_rate = {}

        self.maxhistory[init_coin] = init_amount
        self.maxhistory_unit[init_coin] = init_amount / n18
        self.current_rate[init_coin] = 1

        for cn in coinapi.coin_list:
            if not cn in self.maxhistory:                
                print(cn)
                coin_info = coinapi.best_dex(init_coin, cn, init_amount, dex_valid)
                self.maxhistory[cn] = coin_info["to_amount"] - gasapi.transaction_fee(coin_info["dex_used"]) * n18
                self.maxhistory_unit[cn] = self.maxhistory[cn] / n18
                self.current_rate[cn] = coinapi.best_dex(init_coin, cn, amount_small * n18, dex_valid)["to_amount"] / (amount_small * n18)

        
    def check(self, max_ratio=1.002, max_ratio_high=1.01, dex_valid=["Uniswap V2","Curve","Balancer","Swerve"], realmode=False):
        dex_used = {}
        amount_list = {}
        rate_list={}
        compare_list = {}
        ratio_list= {}
        max_ratio_list={} #交換を行うか否かの基準
        cheap_coin_num = 0
        
        rate_list[self.current_coin] = 1

        for cn in coinapi.coin_list:
            if cn != self.current_coin:
                coin_info = coinapi.best_dex(self.current_coin, cn, self.current_amount,dex_valid)
                amount_list[cn] = coin_info["to_amount"] - gasapi.transaction_fee(coin_info["dex_used"]) * n18
                rate_list[cn] = coinapi.best_dex(self.current_coin, cn, amount_small*n18,dex_valid)["to_amount"]/(amount_small*n18)
                dex_used[cn]=coin_info["dex_used"]
                compare_list[cn] = self.current_rate[cn] * self.current_amount
            
            if cn == "sUSD" or cn == "DAI":
                max_ratio_list[cn] = max_ratio_high
            else:
                max_ratio_list[cn] = max_ratio
                   
        max_cn = ""
        cheap_cn = ""

        for cn in amount_list:
            ratio_list[cn] = amount_list[cn] / compare_list[cn]
            if amount_list[cn] > max(max_ratio , max_ratio_list[cn]) * compare_list[cn] and amount_list[cn] > self.maxhistory[cn]:
                max_cn = cn
                max_ratio = ratio_list[cn]

            if ratio_list[cn] > 1.001:
                cheap_cn = cn
                cheap_coin_num += 1

        print("ValueRatio: "+ str(ratio_list))
        
        if cheap_coin_num >= 2:
            print(self.current_coin+" price incleased")
        elif cheap_coin_num == 1 :
            print(cheap_cn+" prise decreased")

        if max_cn == "": 
            return {"swap": False, "dex_used": "None"}

        else:
            self.previous_coin = self.current_coin
            self.current_coin = max_cn
            self.current_amount = amount_list[max_cn]

            for cn in amount_list:
                if amount_list[cn] > self.maxhistory[cn] : 
                    self.maxhistory[cn] = amount_list[cn]
                    self.maxhistory_unit[cn] = self.maxhistory[cn] / n18
           
            self.current_rate[self.current_coin] = 1
            for cn in coinapi.coin_list:
                if cn != self.current_coin:
                    self.current_rate[cn] = rate_list[cn]/rate_list[self.current_coin]                
        
            print("Swap in　"+ dex_used[self.current_coin] +" : "+ self.previous_coin + " -> " + self.current_coin)
            print("maxhistory:" + str(self.maxhistory_unit))

            if(realmode):
                time.sleep(transaction_time)

            return {"swap": True, "dex_used": dex_used[self.current_coin]}


    def print(self):  
        print("CC:" + self.current_coin + " , maxhistory:" + str(self.maxhistory_unit))
    
    
    


