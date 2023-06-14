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

################

import pandas as pd
# import pandas_datareader.data as web
# import matplotlib.pyplot as plt

# import yfinance as yf
# import altair as alt
import streamlit as st
import datetime

# # 月日計算用
# from dateutil import relativedelta

# # web上の金融情報収集
# import pandas_datareader.data as web

# 四捨五入などの計算式を計算するため
import math

# streamlit でHTMLのリンクを作ることができる
# https://docs.streamlit.io/library/components/components-api
#import streamlit.components.v1 as components

st.title("Start")
st.write("This is just Oki program")

# def bar_chart(df, x, y, color):
#     import plotly.express as px
#     from streamlit_plotly_events import plotly_events

#     clickedPoint = []
#     # クリックイベントのgithub
#     # https://github.com/yihui-he/streamlit-plotly-events/blob/master/src/streamlit_plotly_events/__init__.py
#     figbar = px.bar(df, x=x, y=y, color=color, title="テスト")
#     # figbar = px.bar(
#     #     df, x="Date", y="Dividends", color="profit_and_loss", text="type", title="テスト"
#     # )
#     # plot_name_holder = st.empty()

#     clickedPoint = plotly_events(figbar, key="line")
#     # plot_name_holder.write(f"Clicked Point: {clickedPoint}")
#     # st.plotly_chart(figbar, use_container_width=True)
#     # clickedPoint = clickedPoint[0]
#     # clickdPoint = clickedPoint[0]
#     try:
#         clickedmonth = clickedPoint[0]["x"]
#         st.write(clickedmonth)
#         st.write(df[df["month"] == clickedmonth])
#     except:
#         pass


# def common_data_df():
#     #######共通項目　マスター開始########
#     # ①googleの認証
#     # ②データ取得、整理、抽出

#     ##①googl スプレッドシートを読むための承認関係
#     ####################################################
#     # Google spread sheet 認証用&日付設定
#     # https://docs.gspread.org/en/v5.4.0/oauth2.html のコピペ
#     import gspread
#     from google.oauth2.service_account import Credentials

#     # スプレッドシート操作
#     from gspread_dataframe import set_with_dataframe

#     scopes = [
#         "https://www.googleapis.com/auth/spreadsheets",
#         "https://www.googleapis.com/auth/drive",
#     ]

#     credentials = Credentials.from_service_account_file(
#         "my-data-gathering-system-56fbd487872a.json", scopes=scopes
#     )
#     gc = gspread.authorize(credentials)

#     #####Google Spread sheet 指定（ワークシートは除く）######
#     ##https://docs.google.com/spreadsheets/d/1NigDhKCANgDLMPqnBuXw2DaPKh0c3GwN8cgd_QKWfzI/edit#gid=0
#     ##真ん中部
#     SP_SHEET_KEY = "1NigDhKCANgDLMPqnBuXw2DaPKh0c3GwN8cgd_QKWfzI"
#     sh = gc.open_by_key(SP_SHEET_KEY)
#     ########################
#     ##認証終わり#####
#     ############################################
#     ####②データ抽出開始（本ファイルがマスター）####
#     # step1:データを読み込み
#     # step2:データの整理
#     # step3:sidebarで表示＆条件設定
#     # step4:3の条件からデータ抽出、ソート
#     # step5:表示&実行
#     ###########
#     # step1:全データをスプレッドシートから読み込み
#     ##########
#     import datetime

#     #####日時時間設定######
#     now = datetime.datetime.now()
#     # 年、月を　current_YMに入れる
#     current_YM = now.strftime("%Y%m")
#     today = datetime.date.today()
#     week = today.isocalendar()
#     # weekには[0]にyear:年、[1]にweek:週番号、[2]にweekday:曜日、日曜が7
#     weekNo = week[1]
#     current_YMW = current_YM + str(weekNo)
#     #########################3
#     # worksheet読み込みなければ一つ古いシートを作る
#     try:
#         worksheet = sh.worksheet(current_YMW)
#     except:
#         current_YMW = int(current_YMW) - 1
#         worksheet = sh.worksheet(current_YMW)

#     data = worksheet.get_all_values()
#     df = pd.DataFrame(data[1:], columns=data[0])
#     # indexをweekNoに変更
#     df = df.set_index("YMweekNo")
#     #####################
#     # step2:データの整理
#     # 数値をobjectからfloat（小数点の数値）へ変換,配当金支払いは文字列にする
#     # googleスプレッドから読み込むと数値がオブジェクト化されているので文字の変換が必要
#     #####################
#     df["trailingAnnualDividendYield:税引前の配当利回り"] = df[
#         "trailingAnnualDividendYield:税引前の配当利回り"
#     ].astype(float, errors="raise")

#     df["priceToBook:PBR:Price Book-value Ratio:株価純資産倍率"] = df[
#         "priceToBook:PBR:Price Book-value Ratio:株価純資産倍率"
#     ].astype(float, errors="raise")
#     df["operatingMargins:営業利益率"] = df["operatingMargins:営業利益率"].astype(
#         float, errors="raise"
#     )
#     df["currentRatio:流動比率"] = df["currentRatio:流動比率"].astype(float, errors="raise")
#     ######データ整理おわり#######
#     st.write(df)
#     return df


# ######################
# ##step3:sidebarで表示＆条件設定企業を抽出開始
# # 抽出のためのsidebar表示及びTicker抽出条件入力
# #######################
# def common_streamlit(df):
#     ######################
#     ##step3:sidebarで表示＆条件設定企業を抽出開始
#     # 抽出のためのsidebar表示及びTicker抽出条件入力
#     #######################
#     current_YMW = df.index[0]
#     st.sidebar.write(current_YMW + "データを使用してます")
#     # 元データから国選択
#     country = st.sidebar.selectbox(
#         "select country", ("United States", "Japan", "All"), index=0
#     )
#     # 配当率 税引前の配当利回りが3.75％以上
#     Divi_ratio_low, Divi_ratio_high = st.sidebar.slider(
#         "配当利回り率の範囲", 0.00, 10.00, (3.75, 10.00)
#     )

#     Divi_low = Divi_ratio_low * 0.01
#     Divi_high = Divi_ratio_high * 0.01

#     # PBR PBRが高水準ではないこと(目安レンジ：0.5倍~1.5倍)
#     PBR_low, PBR_high = st.sidebar.slider("PBRの範囲", 0.0, 2.0, (0.5, 1.5))

#     # 売上高営業利益率 売上高営業利益率が10％以上　　売上高：amount of sale 営業利益：Operation incame　完了
#     opemarg_ratio_low, opemarg_ratio_high = st.sidebar.slider(
#         "営業利益率　以上", 0.00, 20.00, (10.00, 20.00)
#     )

#     opemarg_low = opemarg_ratio_low * 0.01
#     opemarg_high = opemarg_ratio_high * 0.01

#     # 流動率 流動比率が200％以上　完了
#     CurRa_ratio = st.sidebar.slider("流動率　以上", 0.00, 300.00, 200.00)
#     CurRa = CurRa_ratio * 0.01
#     ################################

#     ######step4:3の条件からデータ抽出、ソート
#     # sidebar設定からデータを計算させてに企業抽出する##################

#     if country != "All":
#         df = df[df["country:国"] == country]

#     if Divi_ratio_high != 10.0:
#         df = df[df["trailingAnnualDividendYield:税引前の配当利回り"] < Divi_high]
#     df = df[df["trailingAnnualDividendYield:税引前の配当利回り"] > Divi_low]

#     if opemarg_ratio_high != 20.0:
#         df = df[df["operatingMargins:営業利益率"] < opemarg_high]
#     df = df[df["operatingMargins:営業利益率"] > opemarg_low]

#     if PBR_high != 2.0:
#         df = df[df["priceToBook:PBR:Price Book-value Ratio:株価純資産倍率"] < PBR_high]
#     df = df[df["priceToBook:PBR:Price Book-value Ratio:株価純資産倍率"] > PBR_low]

#     df = df[df["currentRatio:流動比率"] > CurRa]

#     # 抽出されたものを配当利回り＆営業利益率が高い方からソートする
#     df = df.sort_values(
#         ["trailingAnnualDividendYield:税引前の配当利回り", "operatingMargins:営業利益率"],
#         ascending=[False, False],
#     )

#     ######全数表示か個別表示か選ぶ
#     ##############################
#     # #input のためのリストを作成
#     l = []
#     # t_l = []
#     for c in df.ticker:
#         l.append(c)

#     #########################
#     ######抽出された会社から表示する会社を選択する、初期は全部表示###########
#     # lは前にdf.tickerのリストを設定,最大１０社とする
#     l2 = l[0:10]
#     st.sidebar.write("個別銘柄選択")
#     index_stock = st.sidebar.multiselect("These are screening tickers: ", l, l2)
#     if not index_stock:
#         st.sidebar.error("少なくとも一社は選んでください。")
#     else:
#         df_ch = pd.DataFrame()
#         df_base = pd.DataFrame()
#         for c in index_stock:
#             df_ch = df[df["ticker"] == c]
#             df_base = pd.concat([df_base, df_ch])

#     df = df_base
#     ##表面
#     st.write(
#         f"{Divi_ratio_low}<配当利回り<{Divi_ratio_high}以上、{PBR_low}<PBR<{PBR_high}、{opemarg_ratio_low}<営業利益率<{opemarg_ratio_high}%以上、流動率{CurRa_ratio}%"
#     )
#     st.write(df)

#     return df, index_stock


# #########################抽出end（共通項目：マスター）###############


# ###抽出した会社の配当金傾向を見える化開始######
# # #prg複雑回避するため配当日と配当率だけ取得して描画するdivipraph を定義
# def divi_info(df):
#     # 配当率のデータ
#     df2 = pd.DataFrame()
#     count = -1

#     for c in df.ticker:
#         #########
#         ##配当率見える化###
#         #########
#         ticker = c
#         #######配当金データ取得
#         # データを改めて収集
#         tk2 = yf.Ticker(c)
#         # 10年分のデータ取得
#         view2 = tk2.dividends
#         #############################
#         #######配当金の数値整理(年ごとに数値計算)#######
#         # resampleで年ごとに合計を計算
#         view2 = view2.resample("Y").sum()
#         # Y-M-dTの表示をindex（縦方向）を年のみ表示にする
#         view2.index = view2.index.strftime("%Y").astype(int)
#         # 計算するためにview3を定義、インデックスを付け直し＝インデックスにある年をデータ化
#         view3 = view2.reset_index()
#         #####配当データを20年分のみに抽出する###############
#         # 今から20年前,今年を除くと21年前の時間を取得(relativedeltaをimport)2001年＠2022現在s
#         criteriaY = datetime.datetime.now() - relativedelta.relativedelta(years=22)
#         # index内にある20年前の年月日から年だけを抽出して、かつ数値化(int)
#         criteriaY = int(criteriaY.strftime("%Y"))
#         # データの年の列’Date'の計算した21年以降のデータのみを再設定
#         view3 = view3[view3["Date"] > criteriaY]
#         pd.to_datetime(view3["Date"], format="%Y")
#         # 計算完了のためview3の20年分のデータが整ったので元のview2にindexに年データに入れ直し、
#         # かつインデックスをDateにする
#         view2 = view3.set_index("Date")
#         # index（縦方向）を日、月、年の表示にする
#         # 転置Tで縦軸と横軸を変更して、インデックスはリセットして付け直し
#         view2 = pd.DataFrame(view2).T.reset_index()
#         view2["index"] = c
#         # 旧dfの下にview2のデータを追加する
#         df2 = pd.concat([df2, view2])

#     return df2


# def divigraph(df2):
#     df2 = pd.melt(df2, id_vars=df2.columns.values[:1]).rename(
#         columns={"value": "Dividends(USD/YEN)"}
#     )

#     # altairを使って　配当金傾向を描画
#     viewview = (
#         alt.Chart(df2)
#         .mark_line()
#         .encode(
#             x=alt.X("Date", title="Year"),
#             y=alt.Y("Dividends(USD/YEN):Q", title="Dividends(USD/YEN"),
#             color=alt.Color("index:N", title="Campany"),
#         )
#         .properties(width=400, height=300, title="配当金傾向確認")
#     )
#     st.altair_chart(viewview, use_container_width=True)
#     return


# #####
# st.title("米国・日本 高配当株スクリーニング可視化アプリ")
# df = common_data_df()  # 全てのdf抽出
# df, index_stock = common_streamlit(df)  # スクリーニングdf抽出


# ##配当関係の表示＆実行##
# st.title("配当傾向を可視化")

# df2 = divi_info(df)
# st.write(df2)

# divigraph(df2)
# # st.write(df2)


# summary = pd.DataFrame()
# ########################################################
# # ##連続配当及び配当傾向の検討,数値計算#########################
# # for c in index_stock:
# #     # 名前をdfから取得して表示
# #     na = df.loc[:, ["ticker", "name:名前"]].set_index("ticker")
# #     st.write(c, na.loc[c, "name:名前"])

# #     # df2_ch = df2[df2["index"] == c]

# #     ############################################
# #     # 今年を除いた過去20年間で何回配当金が①値上げ②維持②値下げをカウント
# #     # Calは増配回数　Cals連続増配回数、過去から計算する
# #     # cal, cals = 0, 0
# #     # for num in range(20):
# #     #     # スタートの21年前を取得
# #     #     n1 = int(now.strftime("%Y")) - 21 + int(num)
# #     #     # その1年後
# #     #     n2 = n1 + 1
# #     #     # 2022年の場合、n1=2002,n2=2003
# #     #     cal1 = df2_ch[n2] - df2_ch[n1]
# #     #     cal1 = cal1.iloc[0]
# #     #     # cal1で増配だった場合
# #     #     if cal1 > 0:
# #     #         cal1 = 1
# #     #         cal2 = 1
# #     #         cal = cal + cal1  # 増配回数を計算
# #     #         cals = cals + cal2  # 連続増配を計算
# #     #     else:
# #     #         cals = 0  # 増配をリセット
# #     # #########################################################
# #     # #########################################################
# #     # #######################################################
# #     # df2_ch = df2_ch.set_index("index").T  # データを置換してindexに"index"を入れる
# #     # # 移動平均は2年、3年、4年で計算
# #     # for month_move_ave in 2, 3, 4:
# #     #     move_ave = c + "_" + str(month_move_ave) + "month_move_ave"
# #     #     # st.write(move_ave)
# #     #     df2_ch[move_ave] = df2_ch[c].rolling(window=month_move_ave).mean()
# #     #     # st.write(move_ave, df2_ch)
# #     ########################
# #     ########################

# #     # df2loss = df2_ch.isnull().sum()  # 配当金自体に欠損値、０もない＝配当自体が開始してないor会社がない期間
# #     # df2loss = df2loss.iloc[0]  # pandasからデータを取り出す
# #     # cal_ratio = round(cal / (19 - df2loss) * 100, 1)  # 増配した確率＝今後も増配の予感？

# #     ##配当性向を計算#######################
# #     #'trailingEps' 過去のEPS 過去12ヶ月のEPS
# #     # 計算式は以下
# #     # 配当性向（％） ＝ 1株当たりの配当 ÷ EPS × 100
# #     # 配当は今年度は未定＝昨年を計算
# #     y = n2  # 昨年を定義
# #     df22 = df2.set_index("index")  # 昨年の配当金
# #     yy = yf.Ticker(c)
# #     # yesstock = yy.history(c)
# #     # yesterday = datetime.datetime.now() - relativedelta.relativedelta(days=1)
# #     # yesterday = yesterday.strftime("%Y-%m-%d")
# #     # # st.write("yes", yesterday)
# #     # yesstock = yesstock.loc[yesterday, "Close"]

# #     eps = yy.info["trailingEps"]  # epsを取得
# #     per = yy.info["trailingPE"]  # PERの取得
# #     # 配当性向計算
# #     divi_tendency = round(df22.at[c, y] / eps * 100, 2)
# #     st.write("配当性向", divi_tendency, "EPS(1株当たりの純利益)", eps)

# #     elmstock = eps * per

# #     colu = ["name:名前", "配当性向", "EPS(1株当たりの純利益)", "増配率", "連続増配", "予想株価"]

# #     record = pd.Series([c, divi_tendency, eps, cal_ratio, cals, elmstock], index=colu)
# #     summary = summary.append(record, ignore_index=True)
# #     # ignore_index=True

# #     ######################

# #     # st.write(
# #     #     f"昨年{n2}年まで過去19年間で,{n2-(19-df2loss)}から配当を開始し、増配した回数{cal}回/{20-df2loss}回({cal_ratio}%)、連続増配は{cals}年連続"
# #     # )
# #     # st.write(f"EPSは{eps},配当性向は{divi_tendency}%,予想株価は{eps*per}USDoryen")

# #     # st.write(df2_ch)
# #     # st.line_chart(df2_ch)

# # st.write(summary)


# ##############
# ###移動平均と剥離率を計算する######
# #


# # ##########抽出した銘柄のセクター比率を取得する
# # df_sector = df["sector:セクター"].value_counts().sort_values(ascending=False)
# # st.write(df_sector)
# # st.line_chart(df_sector)
# # ########################

# ####################
# # import yahoo_fin.stock_info as si

# # start_tmp = "2006-1-01"
# # end_tmp = datetime.date.today().strftime("%Y-%m-%d")
# # st.write(end_tmp)

# # # 銘柄の指定
# # codelist = ["MSFT"]

# # # EPS情報の取得
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

# # st.write(df2)

# # ##配当性向を計算#######################
# # #'trailingEps' 過去のEPS 過去12ヶ月のEPS
# # # 計算式は以下
# # # 配当性向（％） ＝ 1株当たりの配当 ÷ EPS × 100
# # # 配当は今年度は未定＝昨年を計算
# # y = int(now.strftime("%Y")) - 1
# # # 昨年の配当金
# # df2 = df2.set_index("index")
# # # 昨年の配当金
# # st.write(df2[y])
# # ##################

# # for c in index_stock:
# #     st.write(c)
# #     yy = yf.Ticker(c)
# #     eps = yy.info["trailingEps"]
# #     # １株配当金 昨年の配当金
# #     divi_tendency = df2.at[c, y] / eps * 100
# #     st.write("配当性向", divi_tendency, "EPS(1株当たりの純利益", eps)


# ######################
# # EPSのデータ収集

# for c in index_stock:
#     ###df2_ch計算###########
#     # 名前をdfから取得して表示
#     na = df.loc[:, ["ticker", "name:名前"]].set_index("ticker")
#     # st.write("df", df)
#     # st.write("cの属性", type(c))

#     df2_ch = df2[df2["index"] == c]
#     # st.write("df2", df2, "df2_ch", df2_ch)

#     # ############################################
#     # # 今年を除いた過去20年間で何回配当金が①値上げ②維持②値下げをカウント
#     # # Calは増配回数　Cals連続増配回数、過去から計算する
#     cal, cals = 0, 0
#     for num in range(20):
#         # スタートの21年前を取得
#         import datetime

#         now = datetime.datetime.now()
#         n1 = int(now.strftime("%Y")) - 21 + int(num)
#         # その1年後
#         n2 = n1 + 1
#         # 2022年の場合、n1=2002,n2=2003
#         cal1 = df2_ch[n2] - df2_ch[n1]
#         # st.write("cal1", cal1)
#         cal1 = cal1.iloc[0]
#         # cal1で増配だった場合
#         if cal1 > 0:
#             cal1 = 1
#             cal2 = 1
#             cal = cal + cal1  # 増配回数を計算
#             cals = cals + cal2  # 連続増配を計算
#             # st.write("cals", cals)
#         else:
#             cals = 0  # 増配をリセット
#     # #########################################################
#     # #########################################################
#     # #######################################################
#     # st.write(df2_ch)
#     df2_ch = df2_ch.set_index("index").T  # データを置換してindexに"index"を入れる
#     # 移動平均は2年、3年、4年で計算
#     for month_move_ave in 2, 3, 4:
#         move_ave = c + "_" + str(month_move_ave) + "month_move_ave"
#         # st.write(move_ave)
#         df2_ch[move_ave] = df2_ch[c].rolling(window=month_move_ave).mean()
#         # st.write(df2_ch)

#     ##df_ch:diviのデータまとめのデータ整える
#     df2_ch = df2_ch.reset_index()
#     df2_ch = pd.melt(df2_ch, id_vars=df2_ch.columns.values[:1]).rename(
#         columns={"value": "Dividends(USD/YEN)"}
#     )
#     ###############
#     ##配当の分析#####
#     ##############
#     df2loss = df2_ch.isnull().sum()  # 配当金自体に欠損値、０もない＝配当自体が開始してないor会社がない期間
#     df2loss = df2loss.iloc[0]  # pandasからデータを取り出す
#     cal_ratio = round(cal / (19 - df2loss) * 100, 1)  # 増配した確率＝今後も増配の予感？

#     ##配当性向を計算#######################

#     #'trailingEps' 過去のEPS 過去12ヶ月のEPS
#     # 計算式は以下
#     # 配当性向（％） ＝ 1株当たりの配当 ÷ EPS × 100
#     # 配当は今年度は未定＝昨年を計算
#     # # y = n2  # 昨年を定義

#     ##s以下
#     # y = n1 = int(now.strftime("%Y")) - 1
#     # st.write("昨年", y)
#     # df22 = df2.set_index("index")  # 昨年の配当金
#     # st.write("昨年の配当金", df22)

#     # try:
#     #     yy = yf.Ticker(c)
#     #     st.write("ticker", c, yy.info)
#     #     # yesstock = yy.history(c)
#     #     # yesterday = datetime.datetime.now() - relativedelta.relativedelta(days=1)
#     #     # yesterday = yesterday.strftime("%Y-%m-%d")
#     #     # # st.write("yes", yesterday)
#     #     # yesstock = yesstock.loc[yesterday, "Close"]
#     #     eps = yy.info["trailingEps"]  # epsを取得
#     #     per = yy.info["trailingPE"]  # PERの取得
#     #     # 配当性向計算
#     #     divi_tendency = round(df22.at[c, y] / eps * 100, 2)
#     #     st.write("配当性向", divi_tendency, "EPS(1株当たりの純利益)", eps)
#     #     elmstock = eps * per
#     # except:

#     #     eps = "No"
#     #     per = "no"
#     #     elmstock = "no"
#     #     divi_tendency = "no"

#     # colu = ["Ticker", "name", "配当性向", "EPS(1株当たりの純利益)", "増配率", "連続増配", "予想株価"]

#     # record = pd.Series(
#     #     [c, na.loc[c, "name:名前"], divi_tendency, eps, cal_ratio, cals, elmstock],
#     #     index=colu,
#     # )
#     # summary = summary.append(record, ignore_index=True)
#     # st.write(record)

#     # ######################

#     st.write(
#         f"昨年{n2}年まで過去19年間で,{n2-(19-df2loss)}から配当を開始し、増配した回数{cal}回/{20-df2loss}回({cal_ratio}%)、連続増配は{cals}年連続"
#     )
#     # st.write(f"EPSは{eps},配当性向は{divi_tendency}%,予想株価は{elmstock}USDoryen")

#     # #################################
#     # # EPSの銘柄の指定################
#     # # EPS情報の取得##################
#     # ##############################
#     # import yahoo_fin.stock_info as si

#     # ticker = c
#     # ticker_earnings_hist = pd.DataFrame()
#     # ticker_earnings_hist = si.get_earnings_history(ticker)
#     # st.write(ticker_earnings_hist)
#     # # EPSグラフ作成のためのデータ調整
#     # try:  # 日本株用
#     #     dfEPS = pd.DataFrame.from_dict(ticker_earnings_hist).loc[
#     #         :, ["startdatetime", "epsestimate", "epsactual"]
#     #     ]
#     #     dfEPS.rename(
#     #         columns={
#     #             "epsestimate": "EPS_Estimate",
#     #             "epsactual": "EPS_Actual",
#     #             "startdatetime": "Date",
#     #         },
#     #         inplace=True,
#     #     )
#     #     # st.write("日付変換まえ", dfEPS)
#     #     dfEPS["Date"] = pd.to_datetime(dfEPS["Date"], format="%Y-%m")
#     #     dfEPS = dfEPS.sort_index(axis="index", ascending=False)[
#     #         ["Date", "EPS_Estimate", "EPS_Actual"]
#     #     ]
#     #     # EPSの期間調整
#     #     # 21年前を計算
#     #     start_tmp = datetime.date.today() - relativedelta.relativedelta(years=21)
#     #     start_tmp = start_tmp.strftime("%Y-%m-%d")
#     #     end_tmp = datetime.date.today().strftime("%Y-%m-%d")
#     #     dfEPS2 = dfEPS[
#     #         (dfEPS["Date"] > start_tmp) & (dfEPS["Date"] < end_tmp)
#     #     ]  # データを絞る
#     #     # EPS成長率の計算
#     #     growth_01 = round(dfEPS2.EPS_Actual.pct_change(4).iloc[-1] * 100, 1)
#     #     growth_03 = round(dfEPS2.EPS_Actual.pct_change(12).iloc[-1] * 100, 1)
#     #     growth_05 = round(dfEPS2.EPS_Actual.pct_change(20).iloc[-1] * 100, 1)

#     #     st.write("EPS成長率　1y", growth_01, "3y", growth_03, "5y", growth_05)

#     #     # データをDate,種類としてEPS,数値としてEPS(USD/YEN)
#     #     dfEPS2 = pd.melt(dfEPS2, id_vars=dfEPS2.columns.values[:1]).rename(
#     #         columns={"value": "EPS(USD/YEN)", "variable": "EPS"}
#     #     )
#     # except:
#     #     st.write("EPS取れない")

#     lines = (
#         alt.Chart(df2_ch)
#         .mark_line()
#         .encode(x="Date", y="Dividends(USD/YEN)", color="index")
#     )
#     try:  # 日本株用
#         # ２軸グラフのための基本のAltar設定
#         base1 = alt.Chart(dfEPS2).encode(x="Date:T").properties()
#         # base2 = alt.Chart(df2).encode(x="Date").properties()

#         # EPSのbarを設定、y軸の積み重ねしないのはstack=Noneが必要
#         bars = (
#             base1.transform_fold(["EPS_Actual", "EPC_Estimate"])
#             .mark_bar(opacity=0.3)
#             .encode(alt.Y("EPS(USD/YEN):Q", stack=None), alt.Color("EPS:N"))
#         )
#         zz = alt.layer(bars, lines).resolve_scale(y="independent")
#         st.altair_chart(zz, use_container_width=True)
#     except:
#         st.altair_chart(lines, use_container_width=True)

# # st.write(summary)
