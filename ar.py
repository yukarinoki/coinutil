import coinapi
import time
transaction_time = 180
transaction_fee=6 #単位は$

n18=1000000000000000000

class Arbitrage:
    def __init__(self, init_coin, init_amount):
        if(not coinapi.CoinNameIsValid(init_coin)):
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
                maxamount = 0
                print(cn)
                uniswapv2_amount = coinapi.Uniswapv2(init_coin, cn, init_amount)-transaction_fee * n18
                uniswapv2_rate = coinapi.Uniswapv2(init_coin, cn, n18)/n18
                curve_amount = coinapi.Curve(init_coin, cn, init_amount)-transaction_fee * n18
                curve_rate = coinapi.Curve(init_coin, cn, n18)/n18
                self.maxhistory[cn] = max(uniswapv2_amount, curve_amount)
                self.maxhistory_unit[cn]= max(uniswapv2_amount, curve_amount)/n18
                self.current_rate[cn] = max(uniswapv2_rate, curve_rate)
        
    def check(self, max_ratio=1.002, max_ratio_sUSD = 1.01, realmode=False):
        dex_list = {}
        compare_list = {}
        amount_list = {}
        ratio_list= {}
        max_ratio_list={}
        cheap_coin_num = 0
        

        for cn in coinapi.coin_list:
            if cn != self.current_coin:
                uniswapv2_amount = coinapi.Uniswapv2(self.current_coin, cn, self.current_amount)-transaction_fee * n18
                curve_amount = coinapi.Curve(self.current_coin, cn, self.current_amount)-transaction_fee * n18
                maxamount =  max(uniswapv2_amount, curve_amount)
                if uniswapv2_amount > curve_amount:
                    dex_list[cn] = "Uniswap V2"
                else:
                    dex_list[cn] = "Curve"
                compare_list[cn] = self.current_rate[cn] * self.current_amount
                amount_list[cn] = maxamount 
            
            if cn == "sUSD":
                max_ratio_list[cn] = max_ratio_sUSD
            else:
                max_ratio_list[cn] = max_ratio
           
        max_cn = ""

        for cn in amount_list:
            if amount_list[cn] > max(max_ratio , max_ratio_list[cn]) * compare_list[cn]:
                max_cn = cn
                max_ratio = amount_list[cn]/compare_list[cn]
                # print(cn)
            
            ratio_list[cn]=amount_list[cn]/compare_list[cn]
            if ratio_list[cn] > 1.001:
                cheap_coin_num += 1
        
        if cheap_coin_num >= 3:
            print(str(self.current_coin)+" price incleased")
        elif cheap_coin_num == 2 or cheap_coin_num == 1 :
            print(str(max_cn)+" prise decreased")

        print("ValueRatio: "+ str(ratio_list))

        if max_cn == "":
            return ""
        else :
            self.previous_coin = self.current_coin
            self.current_coin = max_cn
            self.current_amount = amount_list[max_cn]
            for cn in amount_list:
                if amount_list[cn] > self.maxhistory[cn] : 
                    self.maxhistory[cn] = amount_list[cn]
                    self.maxhistory_unit[cn] = self.maxhistory[cn] / n18

            self.current_rate[self.current_coin]=1
            for cn in coinapi.coin_list:
                if cn != self.current_coin:
                    uniswapv2_rate = coinapi.Uniswapv2(self.current_coin, cn, n18)/n18
                    curve_rate = coinapi.Curve(self.current_coin, cn, n18)/n18
                    self.current_rate[cn]= max(uniswapv2_rate, curve_rate)
        
            print("Swap in　"+ dex_list[self.current_coin]+":"+self.previous_coin + "->" + self.current_coin)
            print("maxhistory:" + str(self.maxhistory_unit))
            if(realmode):
                time.sleep(transaction_time)
            return self.previous_coin + "::" + self.current_coin
            

    def print(self):       
        print("CC:" + self.current_coin + " , maxhistory:" + str(self.maxhistory_unit))
    

