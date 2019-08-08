class PoeTradeUrl:
    def __init__(self, league, have, want):
        self.base = "http://currency.poe.trade/search?league="
        self.league = league
        self.have = have
        self.want = want

    def __repr__(self):
        return f'This builds a URL from {self.league} league. The user is buying ' \
            f'currency_ID: {self.want} and is selling currency_ID: {self.have}'

    @property
    def url(self) -> str:
        return f'{self.base}{self.league}&online=x&stock=&want={self.want}&have={self.have}'
