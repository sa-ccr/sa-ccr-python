from Trade import Trade


class Commodity(Trade):
    def __init__(self, **kwargs):
        self.TradeGroup = 'Commodity'
        super().__init__(**kwargs)
