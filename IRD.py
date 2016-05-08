from Trade import Trade
from scipy.stats import norm
from math import log

class IRD(Trade):
    def __init__(self, **kwargs):
        self.TradeGroup = "IRD"
        self.SubClass = " "
        super().__init__(**kwargs)

    @property
    def TimeBucket(self):
        if self.Ei < 1: return 1
        if 1 <= self.Ei <= 5: return 2
        if self.Ei >5: return 3


class IRDSwaption(IRD):
    def __init__(self,OptionType, UnderlyingPrice, StrikePrice, **kwargs):
        self.OptionType = OptionType
        self.UnderlyingPrice = UnderlyingPrice
        self.StrikePrice = StrikePrice
        self.TradeType = "Option"

        super().__init__(**kwargs)

    def CalcSupervDelta(self, Superv_Vol=None):
        if not Superv_Vol:
            return 1 if self.BuySell=="Buy" else -1
        
        if (self.UnderlyingPrice * self.StrikePrice < 0):
            num = self.UnderlyingPrice - self.StrikePrice
        else:
            num = (log(self.UnderlyingPrice/self.StrikePrice)+0.5*Superv_Vol**2*self.Si)
        
        den = Superv_Vol*self.Si**0.5
        temp = num/den
        flip = 1 if self.BuySell=="Buy" else -1
        return flip*norm.cdf(temp) if self.OptionType == 'Call' else flip*-norm.cdf(-temp)


class IRDSwap(IRD):
    def __init__(self, **kwargs):
        self.TradeType = "Swap"
        super().__init__(**kwargs)
