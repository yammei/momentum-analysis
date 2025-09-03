from collections import deque
import mplfinance as mpf
import pandas as pd
import copy
import os
from matplotlib.lines import Line2D

def graph_ema(ema_data: dict, display: bool = False, save: bool = True, overlay_og_data=None) -> None:
    if not display and not save:
        return

    os.makedirs("graphs", exist_ok=True)

    x = pd.to_datetime(copy.deepcopy(ema_data['dates']))
    del ema_data['dates']

    colors_pool = [
        'deepskyblue', 'darkslateblue', 'crimson', 'darkred', 'black',
        'darkgreen', 'goldenrod', 'slategray', 'purple', 'teal'
    ]

    for k1 in ema_data.keys():
        ema_spans = sorted(ema_data[k1].keys(), key=int)

        addplots, labels, colors = [], [], []
        color_rotation = deque(colors_pool[:len(ema_spans)])
        for span in ema_spans:
            c = color_rotation.popleft()
            y = pd.Series(ema_data[k1][span], index=x)
            addplots.append(mpf.make_addplot(y, color=c, width=1.2))
            labels.append(f'EMA{span}')
            colors.append(c)

        if overlay_og_data is not None:
            df = overlay_og_data[k1].copy()
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'])
                df.set_index('Date', inplace=True)

            fig, axes = mpf.plot(
                df,
                type='candle',
                style='yahoo',
                addplot=addplots,
                xrotation=30,
                returnfig=True
            )

            ax = axes[0]
            proxies = [Line2D([0], [0], color=c, lw=1.5) for c in colors]
            ax.legend(proxies, labels, loc="best", fontsize=9, frameon=False)
            fig.suptitle(f"{k1} EMA{'-'.join(map(str, ema_spans))} + Candles")

            if save:
                fig.savefig(f"graphs/{k1}_EMA{'-'.join(map(str, ema_spans))}_overlaid.png", bbox_inches='tight', dpi=150)
            if display:
                mpf.show()
            continue

        base_close = pd.Series(ema_data[k1][ema_spans[-1]], index=x, name='Close')
        df_base = pd.DataFrame({'Close': base_close})

        fig, axes = mpf.plot(
            df_base,
            type='line',
            style='yahoo',
            addplot=addplots,
            xrotation=30,
            returnfig=True
        )

        ax = axes[0]
        proxies = [Line2D([0], [0], color=c, lw=1.5) for c in colors]
        ax.legend(proxies, labels, loc="best", fontsize=9, frameon=False)
        fig.suptitle(f"{k1} EMA values")

        if save:
            fig.savefig(f"graphs/{k1}_EMA{'-'.join(map(str, ema_spans))}.png", bbox_inches='tight', dpi=150)
        if display:
            mpf.show()
