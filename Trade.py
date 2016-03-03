from math import exp, sqrt


class Trade(object):
    def __init__(self,**kwargs):
        for key,val in kwargs.items():
            setattr(self,key,val)



    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.__dict__)

    @property
    def isOption(self):
        return getattr(self,'TradeType',False)=='Option'


    @property
    def AdjNotional(self):
        if self.TradeGroup in ['IRD', 'Credit']:
            return self.Notional*self.SupervDuration
        else:
            return self.Notional

    @property
    def SupervDuration(self):
        if self.Ei < 1:
            return sqrt(self.Ei)
        else:
            return (exp(-0.05*self.Si)-exp(-0.05*self.Ei))/0.05

    @property
    def MaturityFactor(self):
        if self.Ei < 1:
            return sqrt(self.Ei)
        else:
            return 1

    def CalcSupervDelta(self, Superv_Vol=None):
        # Only the simpler calculation is relevant for Non-options
        if not Superv_Vol:
            return 1 if self.BuySell=="Buy" else -1
