from Trade import Trade
class FX(Trade):
    def __init__(self, **kwargs):
        self.TradeGroup='FX'
        self.SubClass = " "
        super().__init__(**kwargs)

class FXSwap(FX):
    def __init__(self, **kwargs):
        self.TradeType='Swap'
        super().__init__(**kwargs)
