##2022/8/21

# 基本、高配当株投資、考え方、一番重要
# 以下を抽出する日本、アメリカの株を抽出するアプリを作る
# https://kobito-kabu.com/about/jouken/

# 高配当株もいつ買うのか、株価から検討する、移動平均の考え方
# https://www.sevendata.co.jp/shihyou/technical/idouheikin02.html

# グランビルの法則
# 買いパターン・1	長い間、200日移動平均線が下降を続け横バイか少し上向きかけている局面で、株価が移動平均線を下から上に突き抜けた場合、大勢的な買いパターン（信号）です。
# 買いパターン・2	上昇中の200日移動平均線を上回っていた株価が、割り込んだ場合、押し目の買いパターン（信号）です。
# 買いパターン・3	株価が200日移動平均線の上にあり、目先の高値を付け下降に転じ、200日移動平均線の手前で再び上昇に転じた場合、押し目の買いパターン（信号）です。
# 買いパターン・4	下降中の200日移動平均線を株価が下回っていた状態で、さらに株価が売り込まれ下落を続け売りかれた場合、自律反発期待の短期的な買いパターン（信号）です。
# 売りパターン・1	長い間続いた上昇期の後、200日移動平均線が横バイになるか、少し下向きかけている局面で、株価が移動平均線から下放れした場合、基調が下降に転じる長期的な売りパターン（信号）です。
# 売りパターン・2	200日移動平均線が下降中であるのに、これを下回っていた株価が上回るまで急騰した場合、戻りいっぱいの売りパターン（信号）です。
# 売りパターン・3	株価が下降中の200日移動平均線の下にあり、同線に向かって上昇し上回る（上昇して同線を突破できない）も、再び下降に転じた場合、戻りの売りパターン（信号）です。
# 売りパターン・4	株価が上昇し200日移動平均線から、大きく乖離した場合、短期的に修正される売りパターン（信号）です。


# pythonで株計算方法,かなりテクニカルで参考になると思う
# https://myfrankblog.com/convert_daily_stock_data_to_weekly_monthly/
# https://neulab.co.jp/technical-indicator/%E7%A7%BB%E5%8B%95%E5%B9%B3%E5%9D%87%E4%B9%96%E9%9B%A2%E7%8E%87/
# https://optrip.xyz/?p=4318
# 一部、テクニカル計算する方法を検討（今後の検討）

# このアプリはgatherinfoapp .pyで集められたデータから,
# スクリーニングしてその結果を示す

# 以下を抽出する日本、アメリカの株を抽出するアプリを作る
# https://kobito-kabu.com/about/jouken/


# 自己資本比率が50％以上
# １株あたり純利益及び１株あたり純資産が長期的に上昇トレンド(上昇率は不問)
# 配当政策が分かりやすく、配当実績に納得できること

# 配当継続力が高いこと→指標①：調整後利益剰余金÷配当総額,指標②：修正ネットキャッシュ÷配当総額
# 売上高が長期的に上昇トレンド(上昇率は不問)
# １株あたり純利益及び１株あたり純資産が長期的に上昇トレンド(上昇率は不問)

# 総資産に占める現金等の割合が高く、長期的に上昇傾向
from pages import commonapp

# from pages import stockMLProphet

import pandas as pd
import streamlit as st
import datetime


import matplotlib.pyplot as plt

import yfinance as yf
import altair as alt


# 月日計算用
from dateutil import relativedelta

# web上の金融情報収集
import pandas_datareader.data as web

# 四捨五入などの計算式を計算するため
import math


def d_break(df):
    #####数値がない土日をリスト化
    df = df
    # start,endを見て全ての日付リストを作成
    start = pd.to_datetime(df.index[0])
    end = pd.to_datetime(df.index[-1])
    d_all = pd.date_range(start=start, end=end)
    # dfの株価データの日付リストを取得
    d_obs = [d.strftime("%Y-%m-%d") for d in df.index]
    # 株価データの日付データに含まれていない日付を抽出
    d_breaks = [d for d in d_all.strftime("%Y-%m-%d").tolist() if not d in d_obs]
    ################
    return d_breaks


def base_go_Scatter_Line(df, fig, dfy, row):
    import plotly.graph_objects as go

    # 基本的な線描画
    fig.add_trace(
        go.Scatter(x=df.index, y=df[dfy], name=dfy, mode="lines"),
        row=row,
        col=1,
    )
    return


def golden_cross_graph_add(df, fig):
    import plotly.graph_objects as go

    # df = df.dropna(axis=0)

    df = df.dropna(subset=["Close"])

    st.write(
        "ゴールデンクロスとデットクロス",
        "移動線平均線で短期、中期、長期、次上移動平均線MACDでクロスの時" "perfect order:パーフェクトオーダーとは、",
        "複数（3つ以上）の移動平均線が順序よく並んでいる状態を指します。",
        "3つの移動平均線が使用される場合が多く、",
        "短期＞中期＞長期の順番にきれいに並んでいる状態をパーフェクトオーダーと言います。",
        "単純移動平均線（Simple Moving Average：SMA）指数平滑移動平均線（Exponential Moving Average：EMA）"
        "単純移動平均線（SMA）指数平滑移動平均（EMA）平滑移動平均線（SMMA）線形加重移動平均線（LWMA）GMMA（複合型移動平均線）",
    )

    ls_ave = st.multiselect(
        "What are your favorite SMA,EMA",
        ["EMA", "SMA"],
        ["EMA", "SMA"],
    )
    # 株式用　EMA描写
    ls_days = [5, 20, 25, 50, 75, 200]
    # ls_ave = ["EMA", "SMA"]
    # Fx用以下参照　https://fxinspect.com/archives/25825
    # ls
    for i in ls_days:
        for ii in ls_ave:
            if ii == "EMA":
                dash = "longdashdot"
            if ii == "SMA":
                dash = "solid"
            ave = ii + str(i)
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df[ave],
                    name=ave,
                    mode="lines",
                    line=dict(dash=dash, width=0.5),
                ),
                row=1,
                col=1,
            )

    # 移動平均線
    fig.add_trace(
        go.Scatter(
            x=df.index, y=df["MACD"], name="MACD", mode="lines", showlegend=True
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=df.index, y=df["Signal"], name="Signal", mode="lines", showlegend=True
        ),
        row=2,
        col=1,
    )

    fig.add_trace(
        go.Bar(x=df.index, y=df["MACD-Signal"], name="MACD-Signal"),
        row=2,
        col=1,
        secondary_y=True,
    )

    # MACDゴールデンクロス@MACD
    fig.add_trace(
        go.Scatter(
            x=df[df["cross-MACD"] == "GC"].index,
            y=df[df["cross-MACD"] == "GC"]["MACD"] * 0.98,
            name="GC-MACD",
            mode="markers",
            marker_symbol="triangle-up-dot",
            marker_line_color="midnightblue",
            marker_color="lightskyblue",
            marker_size=15,
            # marker_color="black",
        ),
        row=2,
        col=1,
    )

    # MACDゴールデンクロス@stock
    fig.add_trace(
        go.Scatter(
            x=df[df["cross-MACD"] == "GC"].index,
            y=df[df["cross-MACD"] == "GC"]["Low"] * 0.98,
            name="GC-MACD",
            mode="markers",
            marker_symbol="triangle-up-dot",
            marker_line_color="midnightblue",
            marker_color="lightskyblue",
            marker_size=15,
            # marker_color="black",
            showlegend=False,
        ),
        row=1,
        col=1,
    )
    # MACDデッドクロス
    fig.add_trace(
        go.Scatter(
            x=df[df["cross-MACD"] == "DC"].index,
            y=df[df["cross-MACD"] == "DC"]["High"] * 1.02,
            name="DC-MACD",
            mode="markers",
            marker_symbol="triangle-down",
            marker_size=15,
            marker_color="lightskyblue",
        ),
        row=1,
        col=1,
    )

    # MACDデッドクロス
    fig.add_trace(
        go.Scatter(
            x=df[df["cross-MACD"] == "DC"].index,
            y=df[df["cross-MACD"] == "DC"]["MACD"] * 1.02,
            name="DC-MACD",
            mode="markers",
            marker_symbol="triangle-down",
            marker_size=15,
            marker_color="lightskyblue",
        ),
        row=2,
        col=1,
    )

    # ゴールデンクロス-SMA
    fig.add_trace(
        go.Scatter(
            x=df[df["cross_short(5-25)"] == "GC"].index,
            y=df[df["cross_short(5-25)"] == "GC"]["SMA5"] * 0.98,
            name="GC-short(5-25)",
            mode="markers",
            marker_symbol="triangle-up",
            marker_size=15,
            marker_color="Green",
        ),
        row=1,
        col=1,
    )
    # middle
    fig.add_trace(
        go.Scatter(
            x=df[df["cross_middle(25-75)"] == "GC"].index,
            y=df[df["cross_middle(25-75)"] == "GC"]["SMA25"] * 0.98,
            name="GC-middle(25-75)",
            mode="markers",
            marker_symbol="triangle-up",
            marker_size=15,
            marker_color="Yellow",
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=df[df["cross_long(75-200)"] == "GC"].index,
            y=df[df["cross_long(75-200)"] == "GC"]["SMA75"] * 0.98,
            name="GC-long(75-200)",
            mode="markers",
            marker_symbol="triangle-up",
            marker_size=15,
            marker_color="Red",
        ),
        row=1,
        col=1,
    )

    # デッドクロス-SMA
    # short
    fig.add_trace(
        go.Scatter(
            x=df[df["cross_short(5-25)"] == "DC"].index,
            y=df[df["cross_short(5-25)"] == "DC"]["SMA5"] * 1.02,
            name="DC-short(5-25)",
            mode="markers",
            marker_symbol="triangle-down",
            marker_size=15,
            marker_color="Green",
        ),
        row=1,
        col=1,
    )
    # middle
    fig.add_trace(
        go.Scatter(
            x=df[df["cross_middle(25-75)"] == "DC"].index,
            y=df[df["cross_middle(25-75)"] == "DC"]["SMA25"] * 1.02,
            name="DC-middle(25-75)",
            mode="markers",
            marker_symbol="triangle-down",
            marker_size=15,
            marker_color="Yellow",
        ),
        row=1,
        col=1,
    )

    # long
    fig.add_trace(
        go.Scatter(
            x=df[df["cross_long(75-200)"] == "DC"].index,
            y=df[df["cross_long(75-200)"] == "DC"]["SMA75"] * 1.02,
            name="DC-long(75-200)",
            mode="markers",
            marker_symbol="triangle-down",
            marker_size=15,
            marker_color="Red",
        ),
        row=1,
        col=1,
    )

    fig.update_yaxes(title_text="MACD", row=2, col=1, secondary_y=False)
    fig.update_yaxes(title_text="MACD-Signal", row=2, col=1, secondary_y=True)

    # perfect
    add_vrect(df, fig, "PerfectOrder_diff", "star", "blue", 1.02)

    return


def add_vrect(df, fig, judge, marker_symbol, fillcolor, up_or_down):
    # 0,1,-1判定の列の期間と始点終点に色つけする関数
    import plotly.graph_objects as go
    from datetime import datetime, timezone

    df = df.reset_index()
    # st.write("df", df)

    # 終了期間を算出
    # st.write("df[judge].isin([-1, 1]", df[judge].isin([-1, 1]))
    df_signal = df[df[judge].isin([-1, 1])]
    # st.write("df_signal 1", df_signal)
    df_signal["end_datetime"] = df_signal["Date"].shift(-1)
    # st.write("df_signal 2", df_signal)
    # end_dateが欠損であればtodayを入れる
    now = datetime.now().astimezone()

    # st.write("now", now)
    df_signal["end_datetime"] = df_signal["end_datetime"].fillna(now)
    # st.write("df_signal 3", df_signal)
    df_signal_st = df_signal[df_signal[judge] == 1]

    # st.write("df_signal 4", df_signal)

    # df_signal = df_signal.set_index("Date")
    # st.write("st", df_signal_st)

    for i in range(len(df_signal[df_signal[judge] == 1])):
        row = df_signal_st.iloc[i]
        fig.add_vrect(
            x0=row["Date"],
            x1=row["end_datetime"],
            line_width=0,
            fillcolor=fillcolor,
            opacity=0.1,
            row=1,
            col=1,
            name=judge,
        )

    # st.write("前半終わり")

    # 変化点始点を表示
    fig.add_trace(
        go.Scatter(
            x=df_signal_st["Date"],
            y=df_signal_st["Close"] * up_or_down,
            mode="markers",
            marker_symbol=marker_symbol,
            marker=dict(size=10, color=fillcolor),
            name=judge + "_st",
        ),
        row=1,
        col=1,
    )
    # st.write("後半終わり")
    # 終点end_pointを表示
    df_signal_end = df_signal[df_signal[judge] == -1]
    # st.write("end", df_signal_end)
    # st.write("プロット前")
    fig.add_trace(
        go.Scatter(
            x=df_signal_end["Date"],
            y=df_signal_end["Close"] * up_or_down,
            mode="markers",
            marker_symbol=marker_symbol + "-open-dot",
            marker=dict(size=10, color=fillcolor),
            name=judge + "_end",
        ),
        row=1,
        col=1,
    )
    # x軸レンジを決める（何故かエラー)
    # fig.update_xaxes(
    #     row=1,
    #     col=1,
    #     range=[df["Date"].min(), df["Date"].max()],
    # )

    return


def ichimoku_graph_add(df, fig):
    # https://myfrankblog.com/judge_signals_for_ichimoku_cloud_with_python/#i-3
    # 一目均衡表
    import plotly.graph_objects as go

    st.write("一目均衡表(Ichimoku Cloud) technical analysis")
    st.write(
        "基準線: (当日を含めた過去26日間の最高値 + 最安値) ÷ 2",
        "転換線: (当日を含めた過去9日間の最高値 + 最安値) ÷ 2" "先行スパン1: ((転換値+基準値) ÷ 2)を26日先行させたもの",
        "先行スパン2: ((当日を含めた過去52日間の最高値 + 最安値)÷2) を26日先行させたもの",
        "遅行スパン: 当日の終値を26日遅行させてたもの",
        "先行スパン1と先行スパン2で囲われた部分は雲と呼ばれ、相場の動向を見る",
        "base_line:基準線,conversion_line:転換線,leading_span1:先行スパン1,leading_span2:先行スパン1,lagging_span:遅延スパン",
    )

    date = [
        "base_line",
        "conversion_line",
        "leading_span1",
        "leading_span2",
        "lagging_span",
    ]

    for n in date:
        # st.write("date", n)
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df[n],
                name=n,
                mode="lines",
                line=dict(width=1),
            ),
            row=1,
            col=1,
        )
    # st.write("塗りつぶし前")

    # 塗りつぶし 雲
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["leading_span1"],
            name="先行スパン1",
            mode="lines",
            fill=None,
            line=dict(width=0, color="gray"),
            showlegend=False,
        ),
        row=1,
        col=1,
    )
    # st.write("塗りつぶし中")

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["leading_span2"],
            name="先行スパン2",
            mode="lines",
            fill="tonexty",
            line=dict(width=0, color="gray"),
            showlegend=False,
        ),
        row=1,
        col=1,
    )
    # st.write("塗りつぶし後")

    # 期間及び始点終点のプロットadd_vrect
    judge = "三役好転_diff"
    fillcolor = "Yellow"
    marker_symbol = "circle"
    add_vrect(df, fig, judge, marker_symbol, fillcolor, 1)
    # add_vrect(df, fig, "三役好転_diff", "circle", "Yellow", 1.02)
    # st.write("好転後")

    judge = "三役逆転_diff"
    fillcolor = "Purple"
    add_vrect(df, fig, judge, marker_symbol, fillcolor, 1)

    return


def toobuysell(df, fig):
    import plotly.graph_objects as go

    df = df.dropna(subset=["Close"])

    st.write("移動平均乖離率（25日） ave+2σ：買われすぎ、ave-2σ:売られすぎ")
    st.write("RSI Relative Strength Index 相対力指数: 70%以上：買われすぎ、30%以下：売られすぎ")
    st.write(
        "Bollinger bands:移動平均線と、その上下に移動平均線と標準偏差から計算した値動きの幅を示す線を加えて、",
        "統計学に基づいて「ほとんどの確率で株価がこの上下の線の内部に収まる」ということを示します。",
        "短期：25日、中期：50,75,長期：100,200",
    )

    # 乖離率
    fig.add_trace(
        go.Scatter(x=df.index, y=df["SMA25_乖離率"], name="SMA25_乖離率"), row=2, col=1
    )
    fig.add_trace(
        go.Scatter(x=df.index, y=df["SMA50_乖離率"], name="SMA50_乖離率"), row=2, col=1
    )
    fig.add_trace(
        go.Scatter(x=df.index, y=df["SMA200_乖離率"], name="SMA200_乖離率"),
        row=2,
        col=1,
    )

    # 乖離率グラフのy軸
    fig.update_yaxes(title_text="乖離率", row=2, col=1)

    # ##統計計算
    # m, s = df["SMA25_乖離率"].mean(), df["SMA25_乖離率"].std()

    # 買われすぎ row=1
    add_vrect(df, fig, "SMA25_乖離率+buy_diff", "triangle-down", "midnightblue", 1.02)
    add_vrect(df, fig, "RSI_too_buy_diff", "triangle-down", "Green", 1.02)
    # 売られすぎ row=1
    add_vrect(df, fig, "SMA25_乖離率-sell_diff", "triangle-up", "Red", 0.98)
    add_vrect(df, fig, "RSI_too_sell_diff", "triangle-up", "Pink", 0.98)

    ######RSIの表示
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["RSI"],
            mode="lines",
            name="RSI",
            line_color="Green",
            # line_width=2,
        ),
        row=2,
        col=1,
        secondary_y=True,
    )
    # y軸をRSIに合わせる
    fig.update_yaxes(
        title_text="RSI",
        row=2,
        col=1,
        range=[0, 100],
        secondary_y=True,
    )

    ###########

    return


def Bollinger_bands(df, fig):
    import plotly.graph_objects as go

    df = df.dropna(subset=["Close"])

    st.write("ボリンジャーバンド:Bollinger bands")
    # ボリンジャーバンド

    options = st.multiselect(
        "What are your favorite SMA",
        [5, 20, 25, 50, 75, 200],
        [20, 75],
    )

    options = sorted(options)
    # st.write(options)
    line_color = ["pink", "Yellow", "Green"]

    for i in options:
        for ii in range(1, 4):
            sma = "SMA" + str(i)
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df[sma + "_" + str(ii) + "upper"],
                    name=sma + "_" + str(ii) + "σ",
                    line=dict(dash="dash", width=0.5, color=line_color[ii - 1]),
                ),
                row=1,
                col=1,
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df[sma + "_" + str(ii) + "lower"],
                    line=dict(dash="dash", width=0.5, color=line_color[ii - 1]),
                    showlegend=False,
                ),
                row=1,
                col=1,
            )

    return


def obv_graph(df, fig):
    import plotly.graph_objects as go

    df = df.dropna(subset=["Close"])

    st.write(
        "OBV:on-balance volume:トレンド系の出来高指標で、短期売買での株価トレンドや売買タイミングを計るための指標、出来高が株価に先行するという考え方"
    )
    fig.add_trace(
        go.Scatter(x=df.index, y=df["OBV"], name="OBV"),
        row=2,
        col=1,
        secondary_y=False,
    )
    fig.update_yaxes(title_text="On-Balance Volume", row=2, col=1, secondary_y=False)
    fig.update_xaxes(
        row=2,
        col=1,
        range=[df.index.min(), df.index.max()],
    )

    return


def line_chart(df, ticker, graph_style):  # Dateがindex
    # https://myfrankblog.com/stock_price_chart_with_python_plotly/
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    # d_breaks = d_break(df)  # おやすみ日を削除

    # figを定義,２つ目は２軸表示
    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_width=[0.2, 0.2, 1.0],
        x_title="Date",
        specs=[
            [{"secondary_y": True}],
            [{"secondary_y": True}],
            [{"secondary_y": False}],
        ],
    )

    # Candlestick
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name=ticker,
        ),
        row=1,
        col=1,
        secondary_y=False,
    )

    #############################################
    # # 上放れ
    # fig.add_trace(
    #     go.Scatter(
    #         x=df.index,
    #         y=df["Up"],
    #         showlegend=True,
    #         name="上放れ",
    #         mode="markers",
    #         marker=dict(
    #             color="yellow",
    #             size=10,
    #             symbol="triangle-down",
    #         ),
    #     )
    # )
    #############################################

    # Volume
    fig.add_trace(
        go.Bar(x=df.index, y=df["Volume"], name="Volume"),
        row=3,
        col=1,
        secondary_y=False,
    )

    # Layout
    # =0.5というのは横軸でちょうど真ん中という意味です。
    # y=0.9はチャートの縦軸でほぼ一番上を指します。（y=1だと文字がはみ出ます）
    # 細やかな設定は以下
    # https://data-analytics.fun/2021/07/02/plotly-layout/
    fig.update_layout(
        hovermode="x unified",
        width=None,
        height=None,
        autosize=True,
        # plot_bgcolor="white",
        # paper_bgcolor="LightSteelBlue",
        margin=dict(t=10, b=50, l=0, r=0),
    )
    # 非営業日を非表示設定,# 日付のフォーマット変更
    fig.update_xaxes(
        # rangebreaks=[dict(values=d_breaks)],
        tickformat="%Y/%m/%d",
        # title_standoff=500,
    )

    # ラベル名の設定とフォーマット変更（カンマ区切り）
    fig.update_yaxes(separatethousands=True, title_text="株価", row=1, col=1)
    fig.update_yaxes(title_text="出来高", row=3, col=1, secondary_y=False)

    fig.update(layout_xaxis_rangeslider_visible=False)  # 余分なのを消す

    if "一目均衡表(Ichimoku Clouds)" == graph_style or "ALL" == graph_style:
        ichimoku_graph_add(df, fig)
    if "買われすぎ/売られ過ぎ(剥離率/RSI)" == graph_style or "ALL" == graph_style:
        toobuysell(df, fig)
    if "ゴールデンクロス" == graph_style or "ALL" == graph_style:
        golden_cross_graph_add(df, fig)
    if "Bollinger bands" == graph_style or "ALL" == graph_style:
        st.write("test_Bollinger")
        Bollinger_bands(df, fig)
    if "グランビルの法則" == graph_style or "ALL" == graph_style:
        st.write("グランビルの法則")
    if "OBV" == graph_style or "ALL" == graph_style:
        obv_graph(df, fig)
    # if "ML_Prophet" == graph_style:
    #     stockMLProphet.ML_prophet(df, fig)

    # )

    st.plotly_chart(fig)
    return


def macd(df):

    ## https://myfrankblog.com/stock_price_chart_with_python_plotly
    # MACD Moving Average Convergence and Divergence（移動平均収束拡散）
    # https://www.oanda.jp/lab-education/beginners/technical_analysis/macd/
    FastEMA_period = 12  # 短期EMAの期間
    SlowEMA_period = 26  # 長期EMAの期間
    SignalSMA_period = 9  # SMAを取る期間
    df["MACD"] = (
        df["Close"].ewm(span=FastEMA_period).mean()
        - df["Close"].ewm(span=SlowEMA_period).mean()
    )
    df["Signal"] = df["MACD"].rolling(SignalSMA_period).mean()
    df["MACD-Signal"] = df["MACD"] - df["Signal"]
    df["cross-MACD"] = find_cross(short=df["MACD"], long=df["Signal"])
    return df


def check_up_gap(x):
    if x["d1"] == 0 and x["Position"] == 1:
        return x["High"]
    else:
        return None


def price_position(x):
    # https://myfrankblog.com/find_entry_point_with_moving_average_in_python/
    if x["Low"] > x["SMA25"]:
        return 1
    elif x["High"] < x["SMA25"]:
        return -1
    else:
        return 0


def rsi(df):
    ## https://myfrankblog.com/stock_price_chart_with_python_plotly
    # 前日との差分を計算
    df_diff = df["Close"].diff(1)

    # 計算用のDataFrameを定義
    df_up, df_down = df_diff.copy(), df_diff.copy()

    # df_upはマイナス値を0に変換
    # df_downはプラス値を0に変換して正負反転
    df_up[df_up < 0] = 0
    df_down[df_down > 0] = 0
    df_down = df_down * -1

    # 期間14でそれぞれの平均を算出
    df_up_sma14 = df_up.rolling(window=14, center=False).mean()
    df_down_sma14 = df_down.rolling(window=14, center=False).mean()

    # RSIを算出
    df["RSI"] = 100.0 * (df_up_sma14 / (df_up_sma14 + df_down_sma14))

    # # RSI 買われすぎ
    df["RSI_too_buy"] = df["RSI"] > 70

    # RSI 売られすぎ
    df["RSI_too_sell"] = df["RSI"] < 30

    # 1日前のデータとの差分を計算:開始が１、終了が-1になる
    df["RSI_too_buy_diff"] = df["RSI_too_buy"] - df["RSI_too_buy"].shift()
    df["RSI_too_sell_diff"] = df["RSI_too_sell"] - df["RSI_too_sell"].shift()
    # 必要なくなった行を削除
    df = df.drop(["RSI_too_buy"], axis=1)
    df = df.drop(["RSI_too_sell"], axis=1)

    return df


def find_cross(short, long):
    # 差分を計算する
    import numpy as np

    diff = short - long
    # diffの各値を直前のデータで引く　2ならゴールデンクロス(GC), -2ならデッドクロス(DC)と判定する
    cross = np.where(
        np.sign(diff) - np.sign(diff.shift(1)) == 2,
        "GC",
        np.where(np.sign(diff) - np.sign(diff.shift(1)) == -2, "DC", np.nan),
    )
    return cross


def sma(df):
    ## https://myfrankblog.com/stock_price_chart_with_python_plotly
    # 移動平均線SMAを計算Simple Moving Average (SMA)
    # df["SMA5"] = df["Close"].rolling(window=5).mean()
    # df["SMA20"] = df["Close"].rolling(window=20).mean()
    # df["SMA25"] = df["Close"].rolling(window=25).mean()
    # df["SMA50"] = df["Close"].rolling(window=50).mean()
    # df["SMA75"] = df["Close"].rolling(window=75).mean()
    # df["SMA200"] = df["Close"].rolling(window=200).mean()
    ###ボリンジャー
    # ボリンジャーバンド戦略
    # https://www.iforex.jpn.co

    # 標準偏差
    SMAday = [5, 20, 25, 50, 75, 150, 200]
    for i in SMAday:
        sma = "SMA" + str(i)  # 移動平均線
        stdd = sma + "_std"
        sma_d = sma + "_乖離率"  # 移動平均乖離率　Moving average divergence rate
        df[sma] = df["Close"].rolling(window=i).mean()
        df[stdd] = df["Close"].rolling(window=i).std()
        df[sma_d] = (df["Close"] - df[sma]) / df[sma] * 100
        # 移動平均乖離率の平均、標準偏差
        m, s = df[sma_d].mean(), df[sma_d].std()
        # 買われすぎ　2σ 95%
        df[sma_d + "+buy"] = df[sma_d] > (m + (2 * s))
        # 売られすぎ　2σ　95%
        df[sma_d + "-sell"] = df[sma_d] < (m - (2 * s))
        #
        df[sma_d + "+buy_diff"] = df[sma_d + "+buy"] - df[sma_d + "+buy"].shift()
        df = df.drop([sma_d + "+buy"], axis=1)
        df[sma_d + "-sell_diff"] = df[sma_d + "-sell"] - df[sma_d + "-sell"].shift()
        df = df.drop([sma_d + "-sell"], axis=1)
        # ボリンジャーバンド用
        for ii in range(1, 4):
            df[sma + "_" + str(ii) + "upper"] = df[sma] + (ii * df[stdd])
            df[sma + "_" + str(ii) + "lower"] = df[sma] - (ii * df[stdd])
        # 指数平滑移動平均 EMA Exponential Moving Average
        ema = "EMA" + str(i)
        df[ema] = df["Close"].ewm(span=i, adjust=False).mean()

    # # ボリンジャーバンド戦略
    # # https://www.iforex.jpn.com/エデュケーションセンター/ボリンジャーバンド

    ####乖離率
    # df["SMA25_乖離率"] = (df["Close"] - df["SMA25"]) / df["SMA25"] * 100
    # df["SMA50_乖離率"] = (df["Close"] - df["SMA50"]) / df["SMA50"] * 100
    # df["SMA200_乖離率"] = (df["Close"] - df["SMA200"]) / df["SMA200"] * 100
    # # df["SMA5-SMA25"] = df["SMA5"] - df["SMA25"]
    # # df["SMA75-SMA200"] = df["SMA75"] - df["SMA200"]
    df["cross_short(5-25)"] = find_cross(df["SMA5"], df["SMA25"])
    df["cross_middle(25-75)"] = find_cross(df["SMA25"], df["SMA75"])
    df["cross_long(75-200)"] = find_cross(df["SMA75"], df["SMA200"])

    # https://myfrankblog.com/find_entry_point_with_moving_average_in_python/
    # 上振れ判定
    # df["Position"] = df.apply(price_position(df), axis=1)
    # df["d1"] = df["Position"].shift()
    # df["Up"] = df.apply(check_up_gap(df), axis=1)
    #########
    return df


def position(df):
    for i in df.index:
        df["Position"] = df.apply(price_position(df), axis=1)
        df["d1"] = df["Position"].shift()
        df["Up"] = df.apply(check_up_gap(df), axis=1)


def perfect_order(df):
    import numpy as np

    df = df.reset_index()
    df["PerfectOrder"] = np.where(
        (df["SMA20"] > df["SMA50"]) & (df["SMA50"] > df["SMA200"]), 1, 0
    )
    # 前日との差分を計算する --> -1, 0, 1のいずれかになる 1がスタート、-1がend,0が変わらない
    df["PerfectOrder_diff"] = df["PerfectOrder"].diff()

    return df


def ichimoku(df):
    # 一目均衡表
    import datetime

    # 計算しやすいように
    df = df.reset_index()
    # 未来の日付データを定義
    try:
        startday = df["Date"].max() + datetime.timedelta(days=1)
        endday = df["Date"].max() + datetime.timedelta(days=25)
        # st.write(startday, endday)
        additional_dates = pd.date_range(
            start=startday,
            end=endday,
        )
    except:
        additional_dates = pd.date_range(
            start=datetime.datetime.now() + datetime.timedelta(days=1),
            end=datetime.datetime.now() + datetime.timedelta(days=25),
        )

    additional_dates = pd.date_range(
        start=datetime.datetime.now() + datetime.timedelta(days=1),
        end=datetime.datetime.now() + datetime.timedelta(days=25),
    )
    # 株価データと結合
    df = pd.concat(
        [
            df,
            pd.DataFrame(additional_dates, columns=["Date"]),
        ],
        ignore_index=True,
    )
    # st.write("未来時間追加", df)

    # 基準線 過去の26日間の最高、最安
    high26 = df["High"].rolling(window=26).max()
    low26 = df["Low"].rolling(window=26).min()
    df["base_line"] = (high26 + low26) / 2
    # st.write("ichimoku基準線追加", df)

    # 転換線　過去の９日間の最高、最安
    high9 = df["High"].rolling(window=9).max()
    low9 = df["Low"].rolling(window=9).min()
    df["conversion_line"] = (high9 + low9) / 2
    # st.write("ichimoku転換線追加", df)

    # 先行スパン1
    leading_span1 = (df["base_line"] + df["conversion_line"]) / 2
    df["leading_span1"] = leading_span1.shift(25)
    # st.write("ichimoku先行スパン１追加", df)

    # 先行スパン2
    high52 = df["High"].rolling(window=52).max()
    low52 = df["Low"].rolling(window=52).min()
    leading_span2 = (high52 + low52) / 2
    df["leading_span2"] = leading_span2.shift(25)

    # 遅行スパン
    df["lagging_span"] = df["Close"].shift(-25)
    # st.write("ichimoku遅延スパン追加", df)

    # 三役好転と三役逆転を判定
    # 三役好転
    buy_condition1 = df["conversion_line"] > df["base_line"]
    buy_condition2 = df["Low"] > df[["leading_span1", "leading_span2"]].max(axis=1)
    buy_condition3 = df["lagging_span"].shift(25) > df["High"].shift(25)
    df["三役好転"] = buy_condition1 & buy_condition2 & buy_condition3
    # st.write("ichimoku三役好転追加", df)

    # 三役逆転
    sell_condition1 = df["conversion_line"] < df["base_line"]
    sell_condition2 = df["High"] < df[["leading_span1", "leading_span2"]].min(axis=1)
    sell_condition3 = df["lagging_span"].shift(25) < df["Low"].shift(25)
    df["三役逆転"] = sell_condition1 & sell_condition2 & sell_condition3
    # 1日前のデータとの差分を計算:開始が１、終了が-1になる
    df["三役好転_diff"] = df["三役好転"] - df["三役好転"].shift()
    df["三役逆転_diff"] = df["三役逆転"] - df["三役逆転"].shift()
    # いらなくなった列を減らす
    df = df.drop(["三役好転"], axis=1)
    df = df.drop(["三役逆転"], axis=1)

    df = df.set_index("Date")
    return df


def obv(df):
    import numpy as np

    # OBV オンバランスボリューム on-balance volume
    # https://medium.com/wwblog/implement-the-on-balance-volume-obv-indicator-in-python-10ac889efe72
    copy = df.copy()
    # https://stackoverflow.com/a/66827219
    copy["OBV"] = (np.sign(copy["Close"].diff()) * copy["Volume"]).fillna(0).cumsum()
    return copy


####株価関係開始######
# 抽出された企業の株価をpandasに入れる
def stock_info(index_stock, days):
    import yfinance as yf
    import numpy as np

    df = pd.DataFrame()
    tk2 = yf.Ticker(index_stock)
    #######days日分のデータ,daysはcommonから
    hist = tk2.history(period=f"{days}d")  ##表示と取得データが同じ　平均線計算なしの場合
    df = hist

    # 各統計データを追加
    df = sma(df)
    df = macd(df)
    df = rsi(df)
    df = perfect_order(df)
    df = ichimoku(df)
    df = obv(df)

    # line_chart(df, index_stock, graph_style)

    # #########
    # # index（縦方向）を日、月、年の表示にする
    # hist.index = hist.index.strftime("%d %B %Y")
    # # 色々株価がある中の、終値＝closeの値を選んでhistへ入れる
    # hist = hist[["Close"]]
    # # 横方向はcompanyを入れなさい
    # hist.columns = [c]
    # # 転置、縦軸と横軸を変えなさい
    # hist = hist.T
    # hist.index.name = "Name"
    # # 元々あるdfデータにhistを追加
    # dfStock = pd.concat([dfStock, hist])

    return df  # dfStock


# ##株価を描写
# def stockgraph(dfStock):
#     data = dfStock

#     ############################
#     # 対象となる文字列,ゴールデンクロス情報以外を抽出
#     character = "cross"
#     # 対象文字列を含まない列名を取得
#     index_not_inc_specific_char = [
#         column for column in data.index if character not in column
#     ]
#     # 取得した列名の表示
#     # st.write("取得した列名：", index_not_inc_specific_char)
#     # 取得した列名のみのデータフレームの表示
#     data = data.loc[index_not_inc_specific_char]
#     # st.write(data)
#     ################################

#     # グラフの上下限決める
#     stock_max = float(math.ceil(data.max().max()))
#     stock_min = float(math.ceil(data.min().min()))
#     ymax = stock_max
#     # 下限は見やすいように微調整
#     ymin = stock_min - (stock_max - stock_min) * 0.1
#     #################################

#     # st.write("### 株価 (USD)", data.sort_index())
#     data.sort_index()
#     data = data.T.reset_index()
#     # data = data.T
#     # st.write(data)

#     data = pd.melt(data, id_vars=["Date"]).rename(
#         columns={"value": "Stock Prices(USD)"}
#     )
#     # st.write(data)

#     # 凡例選択するとそのグラフのみ表示参考
#     # https://zatsugaku-engineer.com/python/streamlit-altair/

#     selection = alt.selection_multi(fields=["Name"], bind="legend")

#     chart = (
#         alt.Chart(data)
#         .mark_line(opacity=0.8, clip=True)
#         .encode(
#             x="Date:T",
#             y=alt.Y(
#                 "Stock Prices(USD):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])
#             ),
#             color="Name:N",
#             opacity=alt.condition(selection, alt.value(1), alt.value(0.1)),
#         )
#         .add_selection(selection)
#     )

#     # ホバー時にマーカーを表示する
#     hover = alt.selection_single(
#         fields=["Date"],
#         nearest=True,
#         on="mouseover",
#         empty="none",
#     )
#     chart_temp = alt.Chart(data).encode(
#         x="Date:T",
#         y=alt.Y(
#             "Stock Prices(USD):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])
#         ),
#         color="Name",
#     )

#     points = chart_temp.transform_filter(hover).mark_circle(size=50)

#     # ホバー時にツールチップを表示
#     tooltips = (
#         alt.Chart(data)
#         .mark_rule()
#         .encode(
#             x="Date:T",
#             y=alt.Y(
#                 "Stock Prices(USD):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])
#             ),
#             opacity=alt.condition(hover, alt.value(0.1), alt.value(0)),
#             tooltip=[
#                 alt.Tooltip("Date:T", title="Date"),
#                 alt.Tooltip("Stock Prices(USD):Q", title="price"),
#                 alt.Tooltip("Name", title="Name"),
#             ],
#         )
#         .add_selection(hover)
#     )

#     annotation_layer1 = (
#         alt.Chart(dfStock_buy)
#         .mark_text(size=20, text="⬇", align="left", color="red")
#         .encode(x="Date:T", y="Stock Prices(USD):Q")
#         .interactive()
#     )

#     annotation_layer2 = (
#         alt.Chart(dfStock_sell)
#         .mark_text(size=20, text="⬆︎", align="left", color="blue")
#         .encode(x="Date:T", y="Stock Prices(USD):Q")
#         .interactive()
#     )

#     try:
#         st.altair_chart(
#             chart + points + tooltips + annotation_layer1 + annotation_layer2,
#             use_container_width=True,
#         )
#     except:
#         ###データの行列が違う＝
#         data = dfStock
#         # 平均線剥離率をグラフ化 ###########################
#         cluset = ["peeling", "Date", "Density"]
#         # .stackを使って列行入れ替えhttps://smart-hint.com/python/stack/
#         data = data.stack().reset_index()
#         data.columns = cluset
#         # 簡単に描写
#         chart = (
#             alt.Chart(data)
#             .mark_line()
#             .encode(x="Date:T", y="Density", color="peeling:N")
#         )
#         st.altair_chart(chart, use_container_width=True)
#     return


#######################
st.title("米国・日本 高配当株スクリーニング可視化アプリ")

########sidebar株式表示2#######
# st.sidebar.write("""# 株価こちらは株価可視化ツールです。以下のオプションから表示日数を指定できます。""")
st.sidebar.write("Graph style")
graph_style = st.sidebar.selectbox(
    "Which is your favorite Graph style?",
    (
        "Normal",
        "一目均衡表(Ichimoku Clouds)",
        "買われすぎ/売られ過ぎ(剥離率/RSI)",
        "ゴールデンクロス",
        "Bollinger bands",
        "グランビルの法則",
        "OBV",
        # "ML_Prophet",
        "ALL",
    ),
)
# 一目均衡表(Ichimoku Clouds)

st.sidebar.write("表示日数選択*グランビルの法則より基本200日")
days = st.sidebar.slider("days", 1, 3000, 200)

df,df_O_M = commonapp.common_data_df()  # 全てのdf抽出,df_O_Mスクリーニングシート
df=commonapp.Screening(df_O_M,df)
df, index_stock = commonapp.common_streamlit(df)  # スクリーニングdf抽出
#df=commonapp.Screening(df_O_M,df)
st.write(df)
dfdf= commonapp.ONeill_and_Minervini(df_O_M,index_stock) #各指数の結果
#st.write(index_stock,dfdf)
#st.write(df)
df = stock_info(index_stock, days)
line_chart(df, index_stock, graph_style)
st.write(df)

############################
# 株価関係######################

# ########sidebar株式表示2#######
# st.sidebar.write("""# 株価こちらは株価可視化ツールです。以下のオプションから表示日数を指定できます。""")
# st.sidebar.write("""## 表示日数選択*グランビルの法則より基本200日""")
# days = st.sidebar.slider("日数", 1, 3000, 200)

##描画のためにもデータ取得実行#


# # dfStockが欲しい
# stock_max = float(math.ceil(dfStock.max().max()))
# stock_min = float(math.ceil(dfStock.min().min()))
# # 株価maxの２倍を最小値と
# # graph_max = float(stock_max * 1.5)
# st.sidebar.write("""## 株価の範囲指定""")
# # ymin, ymax = st.sidebar.slider(
# #     "範囲を指定してください。", 0.0, stock_max, (stock_min - 5, stock_max)
# )

# ############################
# ####株価表示と実行###
# st.title("株価を可視化")
# st.write(f"""### 過去 **{days}日間** の株価""")
# dfStockstock = dfStock.T.reset_index()
# # stockgraph(dfStock)
# st.write(dfStockstock)

# ####個別銘柄詳細分析#####
# st.title("個別銘柄詳細分析")

##移動平均線(rolling)を求める,移動平均線剥離率を求める
# df["SMA25_乖離率"] = (df["close"] - df["SMA25"]) / df["SMA25"] * 100

# dfStock_buy = pd.DataFrame()
# dfStock_sell = pd.DataFrame()

# for c in index_stock:
#     st.write(c)
#     dfStock_buy = pd.DataFrame()
#     dfStock_sell = pd.DataFrame()
#     # 最後にまとめるからのdfを作る
#     # chは株価＋移動平均線
#     # ch2は移動平均線剥離率
#     # ch3は買いすぎ
#     # ch4haは売りすぎ
#     dfStock_ch2 = pd.DataFrame()
#     # st.write(dfStock)

#     # データにインデックスがないため、一旦標準の元のデータをいじらずインデックスを作る
#     dfStock_ch = dfStock.reset_index()
#     # データをtickerを抽出
#     dfStock_ch = dfStock_ch[dfStock_ch["Name"] == c]
#     # st.write(dfStock_ch)
#     # 計算しやすいように、転置して、インデックスを元に戻した＝１品種だけのデータ形式完了
#     dfStock_ch = dfStock_ch.set_index("Name").T
#     # dfStock_ch = dfStock_ch.T
#     # st.write("剥離率計算前")
#     # st.write(dfStock_ch)
#     # 5,25,75,200日の移動平均線と剥離率を求める
#     for day_move_ave in 5, 25, 75, 200:
#         # 移動平均線を求める
#         move_ave = c + "_" + str(day_move_ave) + "DAY_MOVE_AVE"
#         dfStock_ch[move_ave] = dfStock_ch[c].rolling(window=day_move_ave).mean()

#         # 移動平均線剥離率を求める
#         move_ave2 = move_ave + "_PEELING"
#         dfStock_ch2[move_ave2] = (
#             (dfStock_ch[c] - dfStock_ch[move_ave]) / dfStock_ch[move_ave] * 100
#         )

#         # st.write(dfStock_ch, dfStock_ch2)
#         #

#         # #剥離率の統計値、平均mと標準偏差シグマsを求める
#         m, s = dfStock_ch2[move_ave2].mean(), dfStock_ch2[move_ave2].std()
#         dfStock_chtt = dfStock_ch2.reset_index()
#         dfStock_chch = dfStock_ch.reset_index()
#         dfStock_ch3 = dfStock_chtt
#         dfStock_ch4 = dfStock_chtt
#         # # ch3は2シグマ以上を異常値（買われすぎ）として検出
#         dfStock_ch3 = dfStock_chch[dfStock_chtt[move_ave2] > (m + (2 * s))]
#         # dfStock_ch3["buy"] = "▼ too buy"
#         dfStock_ch3 = dfStock_ch3.loc[:, ["Date", c]]
#         # # 2シグマ以上を異常値（売られすぎ）として検出
#         dfStock_ch4 = dfStock_chch[dfStock_chtt[move_ave2] < (m - (2 * s))]
#         # dfStock_ch4["sell"] = "▲ too sell"
#         dfStock_ch4 = dfStock_ch4.loc[:, ["Date", c]]
#         # st.write("too sell", dfStock_ch4)
#         # # # # y=df[df[move_ave2]>(m+(2*s))][c]*1.02, name="買われすぎ", mode="markers", marker_symbol="triangle-down", marker_size=5, marker_color="black"), row=1, col=1)
#         # # st.write(move_ave2 + "ch3を記載")
#         # # dfStock_ch3.append(dfStock_ch4)
#         # st.write("ch3", dfStock_ch3)
#         dfStock_buy = pd.concat([dfStock_buy, dfStock_ch3]).drop_duplicates()
#         dfStock_sell = pd.concat([dfStock_sell, dfStock_ch4]).drop_duplicates()
#         # st.write("buy", dfStock_buy, "sell", dfStock_sell)

#############################
# ゴールデンクロス、デットクロスを計算する、３ヶ月単位の中長期の指標
# ①5日と25日②25日と75日③75日と200日の３種類で計算する
#     import numpy as np

#     # def find_cross(short, long):
#     # 差分を計算する
#     # 初期値は5日

#     move_ave = c + "_5DAY_MOVE_AVE"
#     short = dfStock_ch[move_ave]
#     for day_move_ave in 25, 75, 200:
#         # 移動平均線を
#         move_ave = c + "_" + str(day_move_ave) + "DAY_MOVE_AVE"
#         long = dfStock_ch[move_ave]
#         diff = short - long
#         # diffの各値を直前のデータで引く　2ならゴールデンクロス(GC), -2ならデッドクロス(DC)と判定する
#         cross = np.where(
#             np.sign(diff) - np.sign(diff.shift(1)) == 2,
#             "GC",
#             np.where(np.sign(diff) - np.sign(diff.shift(1)) == -2, "DC", np.nan),
#         )
#         short = long
#         cross_move_ave = "cross" + move_ave
#         dfStock_ch[cross_move_ave] = cross
#         # dfStock_ch
#         # st.write(dfStock_ch)
#     # return cross

#     # st.write(dfStock_ch)
#     # x=dfStock_ch[]
#     ##########################
#     ####################

#     # st.write(dfStock_ch2)
#     # st.write(dfStock_ch)
#     dfStock_buy = dfStock_buy.rename(columns={c: "Stock Prices(USD)"})
#     dfStock_sell = dfStock_sell.rename(columns={c: "Stock Prices(USD)"})
#     # st.write("buy", dfStock_buy, "sell", dfStock_sell)

#     # # ch2は移動平均線剥離率
#     # dfStock_ch2 = dfStock_ch2.T
#     # # st.write(dfStock_ch2)

#     # dfStock_ch = dfStock_ch.T

#     # chは株価＋移動平均線
#     dfStock_ch = dfStock_ch.T
#     stockgraph(dfStock_ch)
#     # ch2は移動平均線剥離率]
#     dfStock_ch2 = dfStock_ch2.T
#     stockgraph(dfStock_ch2)

# # ############
# # # EPS
# # import yahoo_fin.stock_info as si

# # start_tmp = "2006-1-01"
# # end_tmp = datetime.date.today().strftime("%Y-%m-%d")

# # # 銘柄の指定
# # codelist = ["BEN"]

# # # EPS情報の取得#####################
# # ticker = codelist[0]
# # ticker_earnings_hist = si.get_earnings_history(ticker)

# # # EPSグラフ作成のためのデータ調整
# # df = pd.DataFrame.from_dict(ticker_earnings_hist).loc[
# #     :, ["startdatetime", "epsestimate", "epsactual"]
# # ]
# # df.rename(
# #     columns={
# #         "epsestimate": "EPS_Estimate",
# #         "epsactual": "EPS_Actual",
# #         "startdatetime": "Date",
# #     },
# #     inplace=True,
# # )
# # df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
# # df = df.sort_index(axis="index", ascending=False)[
# #     ["Date", "EPS_Estimate", "EPS_Actual"]
# # ]
# # # 期間調整
# # df2 = df[(df["Date"] > start_tmp) & (df["Date"] < end_tmp)]
# # st.write(df)

# # # EPS成長率の計算
# # growth_01 = round(df2.EPS_Actual.pct_change(4).iloc[-1] * 100, 1)
# # growth_03 = round(df2.EPS_Actual.pct_change(12).iloc[-1] * 100, 1)
# # growth_05 = round(df2.EPS_Actual.pct_change(20).iloc[-1] * 100, 1)

# st.write("1y", growth_01, "3y", growth_03, "5y", growth_05)


#######株関係終了###
