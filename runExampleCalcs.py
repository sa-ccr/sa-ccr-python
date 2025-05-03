from CalcAddon import *


def run_example_calcs(trades, csas, colls, simplified=False, OEM=False, ignore_margin=False):
    if len(trades) == len([x['TradeType'] for x in trades]):
        if all(x['TradeType'] == 'Option' and x['BuySell'].upper() == 'SELL' for x in trades):
            print('All trades are sold options, EAD is zero')
            return 0

    cpties = list(set(x['Counterparty'] for x in trades))

    if len(cpties) > 1:
        trade_trees_all = []

        for cpty in cpties:
            trades_cpty = [x for x in trades if x['Counterparty'] == cpty]
            ext_trade_ids_temp = set()
            trade_trees = []
            trades_temp = []

            if csas:
                for i in range(len(csas) + 1):
                    if i < len(csas):
                        if cpty in [x['Counterparty'] for x in csas]:
                            csa = csas[i]
                            csa_tradegroup = [g.replace("'", "") for g in csa['TradeGroups']]
                            csa_currency = [c.replace("'", "") for c in csa['Currency']]

                            trades_i = [x for x in trades_cpty if x['TradeGroup'] in csa_tradegroup and x['Currency'] in csa_currency and x['Counterparty'] == csa['Counterparty'] and x['external_id'] not in ext_trade_ids_temp]
                            if not trades_i:
                                continue

                            trades_tree = CreateTradeGraph(trades_i)
                            trade_ids = [x['external_id'] for x in trades_i]
                            MF = 1 if ignore_margin else csa['CalcMF'](simplified=simplified)
                            ext_trade_ids_temp.update(trade_ids)

                            tree = CalcAddon(trades_tree, MF, simplified=simplified, OEM=OEM)
                            tree['maturity_factor'] = MF
                            trade_trees.append(tree)
                            trades_temp.append(trades_i)
                    else:
                        trades_unmargined = [x for x in trades_cpty if x['external_id'] not in ext_trade_ids_temp]
                        if not trades_unmargined:
                            continue
                        trades_tree = CreateTradeGraph(trades_unmargined)
                        tree = CalcAddon(trades_tree, simplified=simplified, OEM=OEM)
                        trade_trees.append(tree)
                        trades_temp.append(trades_unmargined)
            else:
                trades_tree = CreateTradeGraph(trades_cpty)
                trade_trees.append(CalcAddon(trades_tree, simplified=simplified, OEM=OEM))
                trades_temp.append(trades_cpty)

            for i, tree in enumerate(trade_trees):
                trades_i = trades_temp[i]
                if i >= len(csas):
                    tree['Replacement Cost'] = CalcRC(trades_i, simplified=simplified, ignore_margin=ignore_margin)
                else:
                    tree['Replacement Cost'] = CalcRC(trades_i, csas[i], colls, simplified=simplified, ignore_margin=ignore_margin)

                rc = tree['Replacement Cost']
                tree['PFE'] = CalcPFE(rc['V_C'], rc['V'], tree['addon'], simplified=simplified)
                tree['EAD'] = CalcEAD(rc['RC'], tree['PFE'])

                trades_tree_unmargined = CreateTradeGraph(trades_i)
                trades_tree_unmargined = CalcAddon(trades_tree_unmargined, simplified=simplified, OEM=OEM)
                trades_tree_unmargined['Replacement Cost'] = CalcRC(trades_i, simplified=simplified, ignore_margin=ignore_margin)
                trades_tree_unmargined['PFE'] = CalcPFE(
                    trades_tree_unmargined['Replacement Cost']['V_C'],
                    trades_tree_unmargined['Replacement Cost']['V'],
                    trades_tree_unmargined['addon'],
                    simplified=simplified
                )
                trades_tree_unmargined['EAD'] = CalcEAD(trades_tree_unmargined['Replacement Cost']['RC'], trades_tree_unmargined['PFE'])

                tree['EAD'] = min(tree['EAD'], trades_tree_unmargined['EAD'])

            trade_trees_all.append(trade_trees)
        return trade_trees_all

    else:
        ext_trade_ids_temp = set()
        trade_trees = []
        trades_temp = []

        if csas:
            for i in range(len(csas) + 1):
                if i < len(csas):
                    csa = csas[i]
                    csa_tradegroup = [g.replace("'", "") for g in csa['TradeGroups']]
                    csa_currency = [c.replace("'", "") for c in csa['Currency']]

                    trades_i = [x for x in trades if x['TradeGroup'] in csa_tradegroup and x['Currency'] in csa_currency and x['Counterparty'] == csa['Counterparty'] and x['external_id'] not in ext_trade_ids_temp]
                    if not trades_i:
                        continue

                    trades_tree = CreateTradeGraph(trades_i)
                    trade_ids = [x['external_id'] for x in trades_i]
                    MF = csa['CalcMF'](simplified=simplified)
                    ext_trade_ids_temp.update(trade_ids)

                    tree = CalcAddon(trades_tree, MF, simplified=simplified, OEM=OEM)
                    tree['maturity_factor'] = MF
                    trade_trees.append(tree)
                    trades_temp.append(trades_i)
                else:
                    trades_unmargined = [x for x in trades if x['external_id'] not in ext_trade_ids_temp]
                    if not trades_unmargined:
                        continue
                    trades_tree = CreateTradeGraph(trades_unmargined)
                    tree = CalcAddon(trades_tree, simplified=simplified, OEM=OEM)
                    trade_trees.append(tree)
                    trades_temp.append(trades_unmargined)
        else:
            trades_tree = CreateTradeGraph(trades)
            trade_trees.append(CalcAddon(trades_tree, simplified=simplified, OEM=OEM))
            trades_temp.append(trades)

        for i, tree in enumerate(trade_trees):
            trades_i = trades_temp[i]
            if i >= len(csas):
                tree['Replacement Cost'] = CalcRC(trades_i, simplified=simplified, ignore_margin=ignore_margin)
            else:
                tree['Replacement Cost'] = CalcRC(trades_i, csas[i], colls, simplified=simplified, ignore_margin=ignore_margin)

            rc = tree['Replacement Cost']
            tree['PFE'] = CalcPFE(rc['V_C'], rc['V'], tree['addon'], simplified=simplified)
            tree['EAD'] = CalcEAD(rc['RC'], tree['PFE'])

            trades_tree_unmargined = CreateTradeGraph(trades_i)
            trades_tree_unmargined = CalcAddon(trades_tree_unmargined, simplified=simplified, OEM=OEM)
            trades_tree_unmargined['Replacement Cost'] = CalcRC(trades_i, simplified=simplified, ignore_margin=ignore_margin)
            trades_tree_unmargined['PFE'] = CalcPFE(
                trades_tree_unmargined['Replacement Cost']['V_C'],
                trades_tree_unmargined['Replacement Cost']['V'],
                trades_tree_unmargined['addon'],
                simplified=simplified
            )
            trades_tree_unmargined['EAD'] = CalcEAD(trades_tree_unmargined['Replacement Cost']['RC'], trades_tree_unmargined['PFE'])

            tree['EAD'] = min(tree['EAD'], trades_tree_unmargined['EAD'])

        return trade_trees


