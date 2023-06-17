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
import yfinance as yf
import streamlit as st
import datetime

# 月日計算用
from dateutil import relativedelta

# web上の金融情報収集
import pandas_datareader.data as web

# 四捨五入などの計算式を計算するため
import math

# streamlit でHTMLのリンクを作ることができる
# https://docs.streamlit.io/library/components/components-api
import streamlit.components.v1 as components

def ONeill_and_Minervini(dfdf,ticker):
    # import gspread
    # from google.oauth2.service_account import Credentials

    # # スプレッドシート操作
    # from gspread_dataframe import set_with_dataframe

    # scopes = [
    #     "https://www.googleapis.com/auth/spreadsheets",
    #     "https://www.googleapis.com/auth/drive",
    # ]

    # credentials = Credentials.from_service_account_file(
    #     "my-data-gathering-system-56fbd487872a.json", scopes=scopes
    # )
    # gc = gspread.authorize(credentials)

    # #####Google Spread sheet 指定（ワークシートは除く）######
    # ##https://docs.google.com/spreadsheets/d/1NigDhKCANgDLMPqnBuXw2DaPKh0c3GwN8cgd_QKWfzI/edit#gid=0
    # ##真ん中部
    # SP_SHEET_KEY = "1NkQY3vntwUF_ZhNk4lbam8gArFi2CnzSaHgXon-1OuE"
    # # SP_SHEET_KEY = "1NigDhKCANgDLMPqnBuXw2DaPKh0c3GwN8cgd_QKWfzI"
    # sh = gc.open_by_key(SP_SHEET_KEY)

    # worksheet = sh.worksheet("ONeill_and_Minervini")
    # data = worksheet.get_all_values()
    # df = pd.DataFrame(data[1:], columns=data[0])
    # # indexをweekNoに変更
    # #df = df.set_index("YMweekNo")
    # dfdf=df
    #st.write(dfdf)

    dfdf_fin=pd.DataFrame(index=[], columns=dfdf.columns)
    for i in dfdf.columns:
        #st.write(dfdf[i])
        for ii in range(len(dfdf.index)):
            #st.write(dfdf[i][ii])
            if ticker in dfdf[i][ii]:# or '7068.T' in dfdf[i][ii].keys():
                #st.write(i,ii)
                fullmatch,vcp_temp,vcp_base,temp_base,tt_vcpt2,tt_vcpt3more,df_tt,base_list = 0,0,0,0,0,0,0,0
                if i == "VCP+Tmp+Base":
                    fullmatch=1
                    #st.write("OK_full",fullmatch)
                if i == "VCP+Tmp":
                    vcp_temp=1
                if i == "VCP_Base":
                    vcp_base=1
                if i == "Tmp+Base":
                    temp_base=1
                if i =="Minervini_tt_vcpt2":
                    tt_vcpt2=1
                if i =="Minervini_tt_vcpt3more":
                    tt_vcpt3more=1
                if i =="Minervini_trend_template":
                    df_tt=1
                if i =="ONeill_base":
                    base_list=1
                record = pd.DataFrame([dfdf["YMweekNo"][ii],dfdf["Market"][ii],fullmatch,vcp_temp,vcp_base,temp_base,tt_vcpt2,tt_vcpt3more,df_tt,base_list], index=dfdf.columns)
                record = record.T

                dfdf_fin = pd.concat([dfdf_fin,record], ignore_index=True)       
        dfdf_fin = dfdf_fin.groupby(by=["YMweekNo","Market"]).sum().reset_index()
        #dfdf_fin=dfdf_fin.set_index(ticker)
    st.write(ticker," Screening Results ",dfdf_fin)

    return dfdf_fin



def common_data_df():
    #######共通項目　マスター開始########
    # ①googleの認証
    # ②データ取得、整理、抽出

    ##①googl スプレッドシートを読むための承認関係
    ####################################################
    # Google spread sheet 認証用&日付設定
    # https://docs.gspread.org/en/v5.4.0/oauth2.html のコピペ
    import gspread
    from google.oauth2.service_account import Credentials

    # スプレッドシート操作
    from gspread_dataframe import set_with_dataframe

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    try:
        #google driveからの立ち上げの場合
        credentials = Credentials.from_service_account_file("/content/drive/MyDrive/streamlit_finance/my-data-gathering-system-56fbd487872a.json", scopes=scopes)
    except:
        try:
            #pcからリモートで立ち上げの場合
            credentials = Credentials.from_service_account_file("/Volumes/GoogleDrive/マイドライブ/streamlit_finance/my-data-gathering-system-56fbd487872a.json", scopes=scopes)
        except:
            #docker使ってgithub
            credentials = Credentials.from_service_account_file("https://drive.google.com/file/d/15NI523AwaFeCfGhNpxfiEXPJ-fLiULCq/view?usp=drive_link", scopes=scopes)
            
    gc = gspread.authorize(credentials)

    #####Google Spread sheet 指定（ワークシートは除く）######
    ##https://docs.google.com/spreadsheets/d/1NigDhKCANgDLMPqnBuXw2DaPKh0c3GwN8cgd_QKWfzI/edit#gid=0
    ##真ん中部
    SP_SHEET_KEY = "1NkQY3vntwUF_ZhNk4lbam8gArFi2CnzSaHgXon-1OuE"
    # SP_SHEET_KEY = "1NigDhKCANgDLMPqnBuXw2DaPKh0c3GwN8cgd_QKWfzI"
    sh = gc.open_by_key(SP_SHEET_KEY)

    




    ########################
    ##認証終わり#####
    ############################################
    ####②データ抽出開始（本ファイルがマスター）####
    # step1:データを読み込み
    # step2:データの整理
    # step3:sidebarで表示＆条件設定
    # step4:3の条件からデータ抽出、ソート
    # step5:表示&実行
    ###########
    # step1:全データをスプレッドシートから読み込み
    ##########
    import datetime

    #####日時時間設定######
    now = datetime.datetime.now()
    # 年、月を　current_YMに入れる
    current_YM = now.strftime("%Y%m")
    today = datetime.date.today()
    week = today.isocalendar()
    # weekには[0]にyear:年、[1]にweek:週番号、[2]にweekday:曜日、日曜が7
    weekNo = week[1]
    st.write("This week is" + str(weekNo))
    current_YMW = current_YM + str(weekNo)
    st.write(current_YMW)
    current_YMW_b = current_YMW
    #############
    # shに指定したファイルに全てワークシート名を取得
    ws_list = sh.worksheets()
    # 全て文字列化
    #test = map(str, ws_list)
    #st.write("ws_list",ws_list)
    test = map(str, ws_list)
    # # 要素合体
    test = "".join(test)
    while (True):
        if current_YMW in test:
            st.write("current_YMW",current_YMW)
            worksheet = sh.worksheet(current_YMW)
            break
        current_YMW = int(current_YMW) - 1
        current_YMW = str(current_YMW)
        #st.write("途中",current_YMW)




    # for i in range(len(ws_list)):
    #     if current_YMW in test:
    #         st.write("current_YMW",current_YMW)
    #         worksheet = sh.worksheet(current_YMW)
    #         break
    #     current_YMW = int(current_YMW) - 1
    #     current_YMW = str(current_YMW)
    #     st.write("途中",current_YMW)

    #########################3
    # worksheet読み込みなければ一つ古いシートを作る
    st.write("This week sheet is" + current_YMW)
    # try:
    #     worksheet = sh.worksheet(current_YMW)
    # except: #1週間前のデータ
    #     st.write("We cannnot find this week sheet")
    #     try:  # 通常
    #         current_YMW = int(current_YMW) - 1
    #         current_YMW = str(current_YMW)
    #         worksheet = sh.worksheet(current_YMW)
    #         st.write("weekNo", current_YMW)
    #     except:  
    #         try:#２週間前のデータ
    #             st.write("we cannot find last week data")
    #             current_YMW = int(current_YMW) - 2
    #             current_YMW = str(current_YMW)
    #             worksheet = sh.worksheet(current_YMW)
    #             st.write("weekNo", current_YMW)
    #         except:# 年越しかつ新しい週にならない場合
    #             st.write("We cannnot find this year sheet")
    #             current_YMW_b = int(current_YMW_b) - 10000 + 1100
    #             current_YMW = str(current_YMW_b)
    #             st.write("weekNo", current_YMW)
    #             worksheet = sh.worksheet(current_YMW)

    data = worksheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])
    # indexをweekNoに変更
    df = df.set_index("YMweekNo")
    #####################
    # step2:データの整理
    # 数値をobjectからfloat（小数点の数値）へ変換,配当金支払いは文字列にする
    # googleスプレッドから読み込むと数値がオブジェクト化されているので文字の変換が必要
    #####################
    df["trailingAnnualDividendYield:税引前の配当利回り"] = df[
        "trailingAnnualDividendYield:税引前の配当利回り"
    ].astype(float, errors="raise")

    df["priceToBook:PBR:Price Book-value Ratio:株価純資産倍率"] = df[
        "priceToBook:PBR:Price Book-value Ratio:株価純資産倍率"
    ].astype(float, errors="raise")
    df["operatingMargins:営業利益率"] = df["operatingMargins:営業利益率"].astype(
        float, errors="raise"
    )
    df["currentRatio:流動比率"] = df["currentRatio:流動比率"].astype(float, errors="raise")
    ######データ整理おわり#######
    
    ##各スクリーニングシートを読み込み
    worksheet2 = sh.worksheet("ONeill_and_Minervini")
    data_O_M = worksheet2.get_all_values()
    df_O_M = pd.DataFrame(data_O_M[1:], columns=data_O_M[0])
    #st.write("df_O_M in",df_O_M)
    #########
    return df,df_O_M


######################
##step3:sidebarで表示＆条件設定企業を抽出開始
# 抽出のためのsidebar表示及びTicker抽出条件入力
#######################
def common_streamlit(df):
    ######################
    ##step3:sidebarで表示＆条件設定企業を抽出開始
    # 抽出のためのsidebar表示及びTicker抽出条件入力
    #######################
    current_YMW = df.index[0]
    st.sidebar.write(current_YMW + "データを使用してます")
    # 元データから国選択

    col1, col2, col3 = st.columns(3)

    with col1:
        countryc = st.selectbox("Country", ("United States", "Japan", "All"), index=2)
    # # 元データから国選択
    # countryc = st.sidebar.selectbox(
    #     "select country", ("United States", "Japan", "All"), index=0
    # )

    # 配当率 税引前の配当利回りが3.75％以上
    Divi_ratio_low, Divi_ratio_high = st.sidebar.slider(
        "配当利回り率の範囲", 0.00, 10.00, (3.75, 10.00)
    )

    Divi_low = Divi_ratio_low * 0.01
    Divi_high = Divi_ratio_high * 0.01

    # PBR PBRが高水準ではないこと(目安レンジ：0.5倍~1.5倍)
    PBR_low, PBR_high = st.sidebar.slider("PBRの範囲", 0.0, 2.0, (0.5, 1.5))

    # 売上高営業利益率 売上高営業利益率が10％以上　　売上高：amount of sale 営業利益：Operation incame　完了
    opemarg_ratio_low, opemarg_ratio_high = st.sidebar.slider(
        "営業利益率　以上", 0.00, 20.00, (10.00, 20.00)
    )

    opemarg_low = opemarg_ratio_low * 0.01
    opemarg_high = opemarg_ratio_high * 0.01

    # 流動率 流動比率が200％以上　完了
    CurRa_ratio = st.sidebar.slider("流動率　以上", 0.00, 300.00, 200.00)
    CurRa = CurRa_ratio * 0.01
    ################################

    ######step4:3の条件からデータ抽出、ソート
    # sidebar設定からデータを計算させてに企業抽出する##################

    if countryc != "All":
        df = df[df["country:国"] == countryc]

    if Divi_ratio_high != 10.0:
        df = df[df["trailingAnnualDividendYield:税引前の配当利回り"] < Divi_high]
    df = df[df["trailingAnnualDividendYield:税引前の配当利回り"] > Divi_low]

    if opemarg_ratio_high != 20.0:
        df = df[df["operatingMargins:営業利益率"] < opemarg_high]
    df = df[df["operatingMargins:営業利益率"] > opemarg_low]

    if PBR_high != 2.0:
        df = df[df["priceToBook:PBR:Price Book-value Ratio:株価純資産倍率"] < PBR_high]
    df = df[df["priceToBook:PBR:Price Book-value Ratio:株価純資産倍率"] > PBR_low]

    df = df[df["currentRatio:流動比率"] > CurRa]

    # 抽出されたものを配当利回り＆営業利益率が高い方からソートする
    df = df.sort_values(
        ["trailingAnnualDividendYield:税引前の配当利回り", "operatingMargins:営業利益率"],
        ascending=[False, False],
    )

    ######全数表示か個別表示か選ぶ
    ##############################
    # #input のためのリストを作成

    # スライダーに表示するtickerリスト作る

    l = []
    for c in df.ticker:
        l.append(c)

    l2 = []
    l2 = ["^DJI", "^GSPC", "^IXIC", "^N225"]
    if countryc == "United States":
        l2 = ["^DJI", "^GSPC", "^IXIC"]

    if countryc == "Japan":
        l2 = ["^N225"]

    l2 = l + l2

    #########################
    ######抽出された会社から表示する会社を選択する、初期は全部表示###########
    # lは前にdf.tickerのリストを設定
    # index_stock = st.sidebar.selectbox("This is screening ticker", l2)

    # l = l[0:5]
    # st.sidebar.write("個別銘柄選択")
    # index_stock = st.sidebar.multiselect("These are screening tickers: ", l2, l)
    # if not index_stock:
    #     st.sidebar.error("少なくとも一社は選んでください。")
    # else:
    #     df_ch = pd.DataFrame()
    #     df_base = pd.DataFrame()
    #     for c in index_stock:
    #         df_ch = df[df["ticker"] == c]
    #         df_base = pd.concat([df_base, df_ch])

    # # 配当利回りで高い順にソート
    # df = df_base.sort_values("trailingAnnualDividendYield:税引前の配当利回り", ascending=False)

    ##表面
    with col2:
        index_stock = st.selectbox("Ticker", l2)
        # st.write("'^GSPC:S&P500  ^DJI:Dow ^IXIC:NASDAQ ^N225:日経平均株価")

    with col3:
        investment_style = st.selectbox("Style", ("high-dividend stocks", "othes"))

    st.write(
        f"{Divi_ratio_low}<配当利回り<{Divi_ratio_high}以上、{PBR_low}<PBR<{PBR_high}、{opemarg_ratio_low}<営業利益率<{opemarg_ratio_high}%以上、流動率{CurRa_ratio}%"
    )
    #st.write(df)
    # st.write(l2)

    #####

    return df, index_stock


#####表示系
def bar_chart(df, x, y, color, title):
    import plotly.express as px
    from streamlit_plotly_events import plotly_events

    clickedPoint = []

    # クリックイベントのgithub
    # https://github.com/yihui-he/streamlit-plotly-events/blob/master/src/streamlit_plotly_events/__init__.py

    figbar = px.bar(df, x=x, y=y, color=color, title=title)
    clickedPoint = plotly_events(figbar, key="line")
    # plot_name_holder.write(f"Clicked Point: {clickedPoint}")
    # st.plotly_chart(figbar, use_container_width=True)

    try:
        clickedmonth = clickedPoint[0]["x"]
        st.write(clickedmonth, x)
        st.write(df[df[x] == clickedmonth])
    except:
        pass
    return


def treemap(df, path, values, color, title):
    import plotly.express as px

    # ライブラリの
    path = [px.Constant("All")] + path
    # path=[px.Constant("All"), pathpath],

    fig2 = px.treemap(
        df,
        path=path,
        values=values,
        color=color,
        # color_continuous_scale="PiYG",
        color_continuous_scale="RdBu",  # "balance",  # "RdBu",
        title=title,
        # width=800,
        height=600,
    )

    fig2.data[0].textinfo = "label+text+value+percent entry"
    # "label", "text", "value", "current path", "percent root", "percent entry", "percent parent"
    # 描画
    st.plotly_chart(fig2, use_container_width=True)


def df_ML_change(df, days, index_stock):
    import numpy as np

    c = index_stock
    st.title(c)
    tk2 = yf.Ticker(c)
    #######
    df = tk2.history(period=f"{days}d")
    ###############表示#########

    st.write("機械学習設定")
    col1, col2, col3, col4 ,col5 ,col6 = st.columns(6)
    with col1:
        prophetset = st.selectbox("log tranfer?", ("log", "normal"), index=1)
    with col2:
        changepoint_flag = st.selectbox("FOMC include?", ("No", "Yes"), index=1)
    with col3:
        tran_ratio = st.slider("train_days/All_days ratio", 0.00, 1.00, 0.75)
    with col4:
        ML = st.selectbox(
            "Which ML?",
            (
                "SGDRegressor",
                "RandamForestRegressor",
                "SVR(Support Vector Regression)",
                "NN(neural network) MultilayerPerceptronRegressor",
                "LightGBM",
            ),
            index=0,
        )
    with col5:
        futureday = st.selectbox("Which future day?",(1,2,3,4,5,15,30),index=2)
    with col6:
        target_var = st.selectbox("Which target variable?",("Value","Up"),index=0)

    # 値なしを消す
    df = df.dropna(how="any")
    if prophetset == "log":
        # 対数変換する場合
        df["Close"] = np.log(df["Close"])

    df["ds"] = df.index
    df = df.rename(columns={"Close": "y"})
    # # 余計なデータ削除
    df = df[["ds", "y"]]
    return df, prophetset, changepoint_flag, tran_ratio, ML,futureday, target_var


def stock_heatmap(df):
    st.write(df.corr())



def Screening(df_O_M,df):
    ym=df_O_M["YMweekNo"].to_list()
    ym=list(set(ym))

    st.write("中長期傾向分析")

    col_sc1, col_sc2 = st.columns(2)

    with col_sc1:
        op=st.selectbox("YMweekNo select",ym)
        df_O_M=df_O_M[df_O_M["YMweekNo"]==op]
    #st.write(op,df_O_M)



    VCP_Tmp_Base_list = []
    VCP_Tmp_list = []
    VCP_Base_list = []
    Tmp_Base_list = []
    VCP_list= []
    # VCP_Tmp_Base_list=[]
    all_list=[]

    for tic in range(len(df.index)):
        tictic=df["ticker"][tic]
        #st.write("tictic",tictic)
        for  TTT  in df_O_M.columns:
            #スクリーニング項目
            fufu_list=df_O_M[TTT].to_list()
            #st.write(TTT)
            #縦軸をリスト化、usa,jp_premiam,jp_standard_jp_groth,jp_etf
            for iiii in range(len(fufu_list)):
                #st.write(fufu_list)
                if tictic in fufu_list[iiii]:
                    # st.write(iiii,"ari")
                    all_list.append(tictic)
                    if TTT == "VCP+Tmp":
                        VCP_Tmp_list.append(tictic)
                        #st.write("VCP_TMP",VCP_Tmp_list)
                    if TTT == "VCP+Tmp+Base":
                        VCP_Tmp_Base_list.append(tictic)
                        #st.write("VCP_TEMP_BASE",VCP_Tmp_Base_list)
                    if TTT == "VCP_Base":
                        VCP_Base_list.append(tictic)
                    if TTT == "Tmp+Base":
                        Tmp_Base_list.append(tictic)
                    if TTT == "Minervini_tt_vcpt2" or TTT == "Minervini_tt_vcpt3more":
                        VCP_list.append(tictic)
    

                # else:
                #     st.write(iiii,"なし")

    VCP_Tmp_Base_list = list(set(VCP_Tmp_Base_list))
    VCP_Tmp_list = list(set(VCP_Tmp_list))
    all_list = list(set(all_list))
    VCP_Base_list = list(set(VCP_Base_list))
    Tmp_Base_list = list(set(Tmp_Base_list))
    VCP_list = list(set(VCP_list))


    with col_sc2:
        option = st.selectbox(
            'How would you like to be contacted?',
            ('all', 'VCP+Tmp+Base',"VCP+Tmp","VCP_Base","Tmp+Base","VCP"))

    if option=='all':
        #st.write(all_list)
        df = df.query('ticker in @all_list')
    
    if option=='VCP+Tmp+Base':
        #st.write(VCP_Tmp_Base_list)
        df = df.query('ticker in @VCP_Tmp_Base_list')
    
    if option=='VCP+Tmp':
        #st.write(VCP_Tmp_list)
        df = df.query('ticker in @VCP_Tmp_list')
    if option=="VCP_Base":
        #st.write(VCP_Base_list)
        df = df.query('ticker in @VCP_Base_list')
    if option=="Tmp+Base":
        #st.write(Tmp_Base_list)
        df = df.query('ticker in @Tmp_Base_list')
    if option=="VCP":
        #st.write(VCP_list)
        df = df.query('ticker in @VCP_list')


    #st.write(op,option,df)
    return df


#########################抽出end（共通項目：マスター）###############

df,df_O_M = common_data_df()
#st.write(df_O_M )
df=Screening(df_O_M,df)

#st.write("df_O_M",df_O_M)
df, index_stock = common_streamlit(df)
st.write(df)



#st.write(dfdf)



dfdf=ONeill_and_Minervini(df_O_M,index_stock)
#st.write(dfdf)
st.write("bar_chart(df, x, y, color, title),treemap(df, path, values, color, title)")


# def Screening(df_O_M,df):
#     ym=df_O_M["YMweekNo"].to_list()
#     ym=list(set(ym))

#     col_sc1, col_sc2 = st.columns(2)

#     with col_sc1:
#         op=st.selectbox("YMweekNo select",ym)
#         df_O_M=df_O_M[df_O_M["YMweekNo"]==op]
#     #st.write(op,df_O_M)



#     VCP_Tmp_Base_list=[]
#     VCP_Tmp_list=[]
#     for tic in range(len(df.index)):
#         tictic=df["ticker"][tic]
#         for  TTT  in df_O_M.columns:
#             #st.write(TTT)
#             fufu_list=df_O_M[TTT].to_list()
#             #st.write(fufu_list)
#             for iiii in range(len(fufu_list)):
#                 if tictic in fufu_list[iiii]:
#                     # st.write(iiii,"ari")
#                     VCP_Tmp_Base_list.append(tictic)
                
#                     # if TTT == "VCP+Tmp":
#                     #     VCP_Tmp_list.append(tictic)
                    

#                 # else:
#                 #     st.write(iiii,"なし")

#     VCP_Tmp_Base_list=list(set(VCP_Tmp_Base_list))
#     #VCP_Tmp_list=list(set(VCP_Tmp_list))
#     #st.write(VCP_Tmp_Base_list,VCP_Tmp_list)
#     with col_sc2:
#         option = st.selectbox(
#             'How would you like to be contacted?',
#             ('all', 'VCP+Tmp+Base'))

#     if option=='VCP+Tmp+Base':
#         df = df.query('ticker in @VCP_Tmp_Base_list')

#     st.write(option,df)
# return df


