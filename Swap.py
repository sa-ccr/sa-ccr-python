######################################################################
# Create the base Swap class
#
# This is used to represent the swap product and it will contained to all the swap-like classes

class Swap(object):
    
    def __init__(self,**kwargs):
        for key,val in kwargs.items():
            setattr(self,key,val)

    @property
    def isBasisSwap(self):
        if len(self.pay_leg_type) != 0 and len(self.rec_leg_type) != 0:
            if self.pay_leg_type == self.rec_leg_type:
                if self.pay_leg_type == "Float" or self.pay_leg_type == "Commodity" or self.pay_leg_type == "Equity":
                    return True
        else:
            return False
            
"""
Implemented member variables:
pay_leg_type = "character"
rec_leg_type = "character"

Pending member variables:
pay_leg_ref  = "character"
pay_leg_tenor= "character"
pay_leg_rate = "numeric"
rec_leg_tenor= "character"
rec_leg_ref  = "character"
rec_leg_rate = "numeric"
"""              