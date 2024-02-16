import bittensor
from datetime import datetime

def init_subtensor():
    subtensor = bittensor.subtensor(network='finney', chain_endpoint='localhost:9944') 
    subtensor.get_current_block()
    return subtensor
class Register:
    def __init__(self, max_cost, wallet, netuid, password_):
        self.subtensor = init_subtensor()
        self.max_cost = max_cost
        self.wallet = wallet
        self.netuid= netuid
    #Getters
    def get_max_cost(self):
        return self.max_cost
    def get_netuid(self):
        return self.netuid
    def get_wallet(self):
        return self.wallet
    def wait_for_cost(self):
        while(True): #yes I know
            if self.get_subnet_price() < self.get_max_cost(): # I chose this approach so it's constantly calling the recycle cost and when that'the condition is met, we register
                print("registering")
                print(self.register())
            print(self.get_subnet_price(), time.time )
    def get_subnet_price(self):
        return float(str(self.subtensor.recycle(netuid=self.get_netuid())).split("τ")[1])
    def register(self): # you can actually get the error too many registrations per itnernal
        return self.subtensor._do_burned_register(wallet=self.get_wallet(),netuid=self.get_netuid(), wait_for_inclusion=True, wait_for_finalization=False)


r = Register(max_cost=1.2,wallet=bittensor.wallet(), netuid=4, password_='Coolguy12!')
r.wait_for_cost()
