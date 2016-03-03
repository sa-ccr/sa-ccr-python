from Trade import Trade


class Credit(Trade):
    def __init__(self, **kwargs):
        self.TradeGroup='Credit'
        super().__init__(**kwargs)


class CreditSingle(Credit):
    def __init__(self, **kwargs):
        self.TradeType = 'Single'
        super(CreditSingle, self).__init__(**kwargs)


class CreditIndex(Credit):
    def __init__(self, **kwargs):
        self.TradeType = 'Index'
        super(CreditIndex, self).__init__(**kwargs)
