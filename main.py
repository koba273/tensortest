import bittensor
import datetime
"""
Insert the values into the variables below
Ensure that your system is secure and review scripts before running them.

TODO:
Once the 'Too many reg's this inverval error' comes, find out when the interval opens and start registering in preperation for that
"""
max_cost = 1
netuid = 4
subtensor_ip = "ws://127.0.0.1:9944"
def init_subtensor():
    subtensor = bittensor.subtensor(network=subtensor_ip)
    subtensor.get_current_block()
    return subtensor
class Register:
    _maxcost = None
    _netuid = None
    _wallet = None
    def __init__(self, max_cost, wallet, netuid):
        self.subtensor = init_subtensor()
        self._maxcost = max_cost
        self._wallet = wallet
        self._netuid= netuid
   
    def wait_for_cost(self):
        while(True): #yes I know
            if self.get_subnet_price() < self._maxcost: # I chose this approach so it's constantly calling the recycle cost and when that'the condition is met, we register
                print("registering")
                reg_msg = self.register()
                
                if('False' in str(reg_msg)):
                    print(reg_msg)
                    #break # Keeping until i've collected different error codes, the docs don't have all of them
                else:
                    print(f'Key Successfully Purchased @ {self.get_subnet_price}. \nRegistration Message: {reg_msg}')
                    #break

    def get_subnet_price(self):
        return float(str(self.subtensor.recycle(netuid=self._netuid)).split("τ")[1])
    def register(self): # you can actually get the error too many registrations per itnernal
        return self.subtensor._do_burned_register(wallet=self._wallet,netuid=self._netuid, wait_for_inclusion=True, wait_for_finalization=False)

r = Register(max_cost=max_cost,wallet=bittensor.wallet(), netuid=netuid)
r.wait_for_cost()
