from runExampleCalcs import *
from FX import *

#Tested to match R version

def ExampleFX():
    tr1 = FXSwap(Notional=10000,MtM=30,ccyPair="EUR/USD",Si=0,Ei=10,BuySell='Buy')
    tr2 = FXSwap(Notional=10000,MtM=-20,ccyPair="EUR/USD",Si=0,Ei=4,BuySell='Sell')
    tr3 = FXSwap(Notional=5000,MtM=50,ccyPair="GBP/USD",Si=1,Ei=11,BuySell='Sell')
    trades = [tr1, tr2, tr3]
    return runExampleCalcs(trades)

print(ExampleFX())