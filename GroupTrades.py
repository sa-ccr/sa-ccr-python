def group_trades_func(group_trades, grouping_func, trade_classes_tree):
    results = HandleBasisVol(group_trades)
    hedging_super_set = ["normal_trades"]

    if results.get("hedging_sets"):
        hedging_super_set.extend(results["hedging_sets"])

    for h, hedging_set in enumerate(hedging_super_set):
        if hedging_set == "normal_trades":
            temp_trades = [x for x in group_trades if x['external_id'] not in results.get("trade_ids_all", [])]

            if not temp_trades:
                continue

            trade_classes_tree = grouping_func(temp_trades, trade_classes_tree)
        else:
            # Offset h by 1 as in R (results$trade_ids[[h-1]])
            trade_ids = results["trade_ids"][h - 1]
            temp_trades = [x for x in group_trades if x['external_id'] in trade_ids]

            trade_classes_tree = grouping_func(temp_trades, trade_classes_tree, hedging_set)

    return trade_classes_tree
