from Credit import *
from CalcAddon import *
from runExampleCalcs import *

#Tested to match R version
def ExampleCredit():
    tr1 = CreditSingle(Notional=10000,MtM=20,Currency="USD",Si=0,Ei=3,BuySell='Buy',SubClass='AA',RefEntity='FirmA')
    tr2 = CreditSingle(Notional=10000,MtM=-40,Currency="EUR",Si=0,Ei=6,BuySell='Sell',SubClass='BBB',RefEntity='FirmB')
    tr3 = CreditIndex(Notional=10000,MtM=0,Currency="USD",Si=0,Ei=5,BuySell='Buy',SubClass='IG',RefEntity='CDX.IG')

    trades= [tr1,tr2,tr3]
    return runExampleCalcs(trades)

print(ExampleCredit())
