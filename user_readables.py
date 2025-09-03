

def translate_metrics(metrics: dict = None) -> dict:
    if not metrics:
        return

    translations = {}

    # in case diction needs to change
    diction = {
        'ema': 'short-term trends',
        'ohlc': 'prices',
        'ema_band': 'trend base',
        'ohlc_band': 'price range',

        'bullish': 'upward',
        'bearish': 'downward',
        'neutral': 'neutral',
        'hesitation': 'indecision',

        'within': 'in line with',

        'dominance': 'dominance',
        'acceptance': 'acceptance',
        'rejection': 'extended'
    }

    for k1 in metrics.keys():
        # print(f"metrics[{k1}]")

        # extract info for cleaner code look
        ema_spread_score    = metrics[k1]['ema_spread_score']
        distance            = metrics[k1]['distance']
        above_share         = metrics[k1]['above_share']
        inside_share        = metrics[k1]['inside_share']
        below_share         = metrics[k1]['below_share']

        # initialize dict for ticker translations
        translations[k1] = {}

        # translate ema spread score
        if ema_spread_score >= 0.01:
            translations[k1]['ema_analysis'] = f"{_capitalize(diction['bullish'])} velocity of {abs(ema_spread_score * 100):.2f}%."
        elif ema_spread_score < 0.01 and ema_spread_score >= 0:
            translations[k1]['ema_analysis'] = f"Mild {diction['bullish']} velocity of {abs(ema_spread_score * 100):.2f}%."
        elif ema_spread_score > -0.01 and ema_spread_score < 0:
            translations[k1]['ema_analysis'] = f"Mild {diction['bearish']} velocity of {abs(ema_spread_score * 100):.2f}%."
        else:
            translations[k1]['ema_analysis'] = f"{_capitalize(diction['bearish'])} velocity of {abs(ema_spread_score * 100):.2f}%."

        # translate candle cluster distance
        if distance >= 0.01:
            translations[k1]['distance_analysis'] = f"{_capitalize(diction['ohlc'])} trading above {diction['ema']} by {abs(distance * 100):.2f}%."
        elif distance < 0.01 and distance >= 0:
            translations[k1]['distance_analysis'] = f"{_capitalize(diction['ohlc'])} trading slightly above {diction['ema']} by {abs(distance * 100):.2f}%."
        elif distance > -0.01 and distance > 0:
            translations[k1]['distance_analysis'] = f"{_capitalize(diction['ohlc'])} trading slightly below {diction['ema']} by {abs(distance * 100):.2f}%."
        else:
            translations[k1]['distance_analysis'] = f"{_capitalize(diction['ohlc'])} trading below {diction['ema']} by {abs(distance * 100):.2f}%."

        # translate share (how much of the ema's range is in and out the candle)
        # future feature: add logic to reject if inside most of ema band is within either wick
        if above_share > inside_share and above_share > below_share:
            translations[k1]['share_analysis'] = f"Seller {diction['dominance']}. {_capitalize(diction['ema_band'])} above {diction['ohlc']} ({(above_share * 100):.2f}% of EMA band below {diction['ohlc']})."
        elif inside_share >= above_share and inside_share >= below_share:
            translations[k1]['share_analysis'] = f"Market {diction['hesitation']}. {_capitalize(diction['ema_band'])} {diction['within']} {diction['ohlc']} ({(above_share * 100):.2f}% overlap)."
        else:
            translations[k1]['share_analysis'] = f"Buyer {diction['dominance']}. {_capitalize(diction['ema_band'])} below {diction['ohlc']} ({(below_share * 100):.2f}% of EMA band above {diction['ohlc']})."

    for k1 in translations.keys():
        print(f"['{k1}']")
        for k, v in translations[k1].items():
            print(f"['{k}']: {v}")
        print()
    return

def _capitalize(s: str) -> str:
    return s[0].upper() + s[1:]