

from collections import defaultdict
from math import sqrt,exp
import pandas




def p2f(s):
    return float(s.strip('%'))/100 if '%' in s else float(s)
def LoadSupervisoryData(filepath):
    return pandas.read_csv(filepath, converters={'Supervisory_factor':p2f,
                                                 'Correlation':p2f,
                                                 'Supervisory_option_volatility':p2f})

filepath= 'supervisory_factors.csv'
superv = LoadSupervisoryData(filepath)




def CalcAddon(trades, MF=None):
    calc_dict = {'FX': CalcFX, 'IRD':CalcIRD, 'Credit':CalcCredit, 'Commodity':CalcCommodity }
    sum_addon = 0
    grouped_trades = defaultdict(list)

    for t in trades:
        grouped_trades[t.TradeGroup].append(t)
    for trade_class, trades_list in grouped_trades.items():
        tc_addon = calc_dict[trade_class](trades_list,MF)
        sum_addon += tc_addon
    return sum_addon



def TradeSupervDelta(t):
    if t.isOption:
        volatility = float(superv[(superv.Asset_Class==t.TradeGroup)
                                  & (superv.SubClass==t.SubClass)].Supervisory_option_volatility)
        return t.CalcSupervDelta(volatility)
    else:
        return t.CalcSupervDelta()


def SingleTradeAddon(t,MF):
    maturity_factor = MF or t.MaturityFactor
    AdjNotional = t.AdjNotional
    superv_delta = TradeSupervDelta(t)
    return superv_delta*AdjNotional*maturity_factor


def CalcFX(FX_trades, MF=None):
    # Arrange FX trades into a [ccyPair -> list of trades] mapping.
    trades_by_ccypair = groupby(FX_trades, 'ccyPair')
    ccypairs_addon = defaultdict(float)
    for ccypair, ccypair_trades in trades_by_ccypair.items():
        for t in ccypair_trades:
            ccypairs_addon[ccypair] += SingleTradeAddon(t,MF)
    supervisory_factor = float(superv[(superv.Asset_Class==t.TradeGroup)
                                &(superv.SubClass==t.SubClass)].Supervisory_factor)
    # Accumulating the addon of the hedging set to the trade class
    return supervisory_factor*sum([abs(addon) for ccypair,addon in ccypairs_addon.items()])



def CalcIRD(IRD_trades, MF=None):

    trades_by_currency = groupby(IRD_trades, 'Currency')

    currencies_addon = defaultdict(float)
    for currency, currency_trades in trades_by_currency.items():
        trades_by_timebucket = groupby(currency_trades, 'TimeBucket')
        timebuckets_addon = defaultdict(float)
        for timebucket, timebucket_trades in trades_by_timebucket.items():
            for t in timebucket_trades:
                timebuckets_addon[timebucket]+=SingleTradeAddon(t,MF)
        currencies_addon[currency] = (timebuckets_addon[1]**2+timebuckets_addon[2]**2+timebuckets_addon[3]**2
                                      +1.4*timebuckets_addon[2]*timebuckets_addon[3]
                                      +1.4*timebuckets_addon[2]*timebuckets_addon[1]
                                      +0.6*timebuckets_addon[2]*timebuckets_addon[1])**0.5

    supervisory_factor = float(superv[(superv.Asset_Class==t.TradeGroup)
                                &(superv.SubClass==t.SubClass)].Supervisory_factor)
    return supervisory_factor*sum([addon for _,addon in currencies_addon.items()])


def CalcCredit(Credit_trades, MF=None):
    trades_by_refentities = groupby(Credit_trades,'RefEntity')
    refEntities_Addon = defaultdict(float)
    supervisory_corel = defaultdict(float)
    for re, re_trades in trades_by_refentities.items():
        for t in re_trades:
            refEntities_Addon[re] += SingleTradeAddon(t, MF)
        AssetClass = t.TradeGroup+t.TradeType
        supervisory_factor = float(superv[(superv.Asset_Class==AssetClass)
                                &(superv.SubClass==t.SubClass)].Supervisory_factor)
        refEntities_Addon[re] *= supervisory_factor
        supervisory_corel[re] = float(superv[(superv.Asset_Class==AssetClass)
                                &(superv.SubClass==t.SubClass)].Correlation)

    systematic_component = sum([supervisory_corel[re]*refEntities_Addon[re] for re in refEntities_Addon])**2
    idiosynchratic_component = sum([(1-supervisory_corel[re]**2)*refEntities_Addon[re]**2 for re in refEntities_Addon])
    return sqrt(idiosynchratic_component+systematic_component)


def CalcCommodity(Commodity_trades, MF=None):
    HedgingSets = groupby(Commodity_trades,'SubClass')


    HedgingSets_addon = defaultdict(float)
    supervisory_corel = defaultdict(float)

    for hset, hset_trades in HedgingSets.items():
        com_types_addon = defaultdict(float)
        hset_trades_by_type = groupby(hset_trades,'commodity_type')
        for hs_type, hs_type_trades in hset_trades_by_type.items():
            for t in hs_type_trades:
                com_types_addon[hs_type] += SingleTradeAddon(t, MF)
            supervisory_factor = float(superv[(superv.Asset_Class=='Commodity')
            &((superv.SubClass==t.SubClass) | (superv.SubClass==t.commodity_type))].Supervisory_factor)
            com_types_addon[hs_type] = com_types_addon[hs_type]*supervisory_factor
        supervisory_corel = float(superv[(superv.Asset_Class=='Commodity')
                                &((superv.SubClass==t.SubClass) | (superv.SubClass==t.commodity_type))].Correlation)
        HedgingSets_addon[hset] = sqrt( (sum(com_types_addon.values())*supervisory_corel)**2+
                                        (1-supervisory_corel**2)*sum([cta**2 for cta in com_types_addon.values()]))
    return  sum(HedgingSets_addon.values())

    systematic_component = sum([supervisory_corel[re]*refEntities_Addon[re] for re in refEntities_Addon])**2
    idiosynchratic_component = sum([(1-supervisory_corel[re]**2)*refEntities_Addon[re]**2 for re in refEntities_Addon])
    return sqrt(idiosynchratic_component+systematic_component)


def CalcRC(trades, coll_agreement=None, current_collateral=None):
    V = sum([t.MtM for t in trades])
    if not coll_agreement:
        V_C = V
        RC = max(V_C, 0)
    else:
        V_C = V - current_collateral
        RC = max(V_C, coll_agreement.thres_cpty+coll_agreement.MTA_cpty-coll_agreement.IM_cpty, 0)

    return {"V_C":V_C, "RC":RC}

def CalcPFE(V_C, Addon_Aggregate):
    if V_C < 0:
        multiplier = min(1, 0.05 + 0.95 * exp(V_C/(1.9*Addon_Aggregate)))
    else:
        multiplier = 1
    return multiplier*Addon_Aggregate

def CalcEAD(RC,PFE):
    return 1.4*(RC+PFE)

def groupby(trades, attribute_name):
    trades_by_attr = defaultdict(list)
    for t in trades:
        trades_by_attr[getattr(t,attribute_name)].append(t)
    return trades_by_attr









