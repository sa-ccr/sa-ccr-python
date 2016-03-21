from Commodity import *
from CalcAddon import *
from runExampleCalcs import *

#Tested to match R version
def dummyPrint():
	print("This is a test\n")
	
def ExampleComm():
    tr1 = Commodity(Notional=10000,MtM= -50,Si=0,Ei=0.75,BuySell='Buy',SubClass='Energy',commodity_type='Oil/Gas')
    tr2 = Commodity(Notional=20000,MtM= -30,Si=0,Ei=2,BuySell='Sell',SubClass='Energy',commodity_type='Oil/Gas')
    tr3 = Commodity(Notional=10000,MtM= 100,Si=0,Ei=5,BuySell='Buy',SubClass='Metals',commodity_type='Silver')

    trades= [tr1,tr2,tr3]
    dummyPrint()
    return runExampleCalcs(trades)

print(ExampleComm())