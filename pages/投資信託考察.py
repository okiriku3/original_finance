# https://note.com/hideta_9907/n/na6389f19c0df
# 流浪の武士
import numpy as np
import pandas as pd
from datetime import datetime, timedelta  # CSVデータに年月日データあり
import streamlit as st
import plotly.graph_objects as go

########ETF list get
#import investpy

#df_etf = investpy.etfs.get_etfs_overview(country='united states', as_json = False, n_results = 100)

#st.write(df_etf)

#######
# 個別の投資信託ファンドのデータを取得する関数
def fund_data(isin, assoc):
    # CSVデータをダウンロードするURLを作成し読み込む
    headURL = "https://toushin-lib.fwg.ne.jp/FdsWeb/FDST030000/"

    isin_URL = "isinCd=" + isin
    assoc_URL = "associFundCd=" + assoc
    dl_URL = headURL + "csv-file-download?" + "&" + isin_URL + "&" + assoc_URL
    # st.write(dl_URL)

    # 年月日カラムを加工してデータ取得：年月日をパースする
    my_parser = lambda date: datetime.strptime(date, "%Y年%m月%d日")
    df = pd.read_csv(
        dl_URL,
        encoding="shift-jis",
        index_col="年月日",
        parse_dates=True,
        date_parser=my_parser,
    )
    #st.write("df", isin, assoc, df)
    return df

##データ収集エリア
# 野村外国株式インデックスファンド・ＭＳＣＩ－ＫＯＫＵＳＡＩ（確定拠出年金向け）401k
nomura_gaikokukabu = fund_data(isin="JP90C0002Z87", assoc="01312022")
# 三井住友DC外国債券()401k
mitsui_gaikokusaiken = fund_data(isin="JP90C0000KL7", assoc="79312024")  # done
# ニッセイ外国株
nissei_gaikokukabu = fund_data(isin="JP90C0009VE0", assoc="2931113C")  # done
# 楽天VTI
rakuten_zenbeikabu = fund_data(isin="JP90C000FHD2", assoc="9I312179")  # done
# emax is slim 先進国
emaxisslim_senshinkabu = fund_data(isin="JP90C0006LG2", assoc="0331509A")
# emax is slim 全米株S&P500
emaxisslim_zenbeikabu = fund_data(isin="JP90C000GKC6", assoc="03311187")  # done
# SBI新興国株式インデックス
sbi_shinkoukokukabu = fund_data(isin="JP90C000FQQ5", assoc="8931117C")  # done
#DC日本株式インデックスファンドL SMTAM 日株インデックスL
#https://toushin-lib.fwg.ne.jp/FdsWeb/FDST030000?isinCd=JP90C0000367
#"/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C0000367&associFundCd=64311024"
dc_SMTAM_nihonn= fund_data(isin="JP90C0000367",assoc="64311024")

# 野村外国債券インデックスファンド（確定拠出年金向け）
# https://toushin-lib.fwg.ne.jp/FdsWeb/FDST030000  ?isinCd=JP90C0002ZJ5
nomura_gaikokuseki = fund_data(isin="JP90C0002ZJ5", assoc="0131102B")
# フィデリティ・世界割安成長株投信（確定拠出年金向け）／愛称：テンバガー・ハンター
fidelity = fund_data(isin="JP90C000M6Q9", assoc="32314217")
# たわらノーロード先進国株式
# https://toushin-lib.fwg.ne.jp/FdsWeb/FDST030000?isinCd=JP90C000CMK4
# /FdsWeb/FDST030000/csv-file-download?isinCd=JP90C000CMK4&associFundCd=4731B15C
tawara_senshin = fund_data(isin="JP90C000CMK4", assoc="4731B15C")

# https://toushin-lib.fwg.ne.jp/FdsWeb/FDST030000?isinCd=JP90C00084Z7
# 三菱ＵＦＪ＜ＤＣ＞ＪーＲＥＩＴインデックスファンド
# /FdsWeb/FDST030000/csv-file-download?isinCd=JP90C00084Z7&associFundCd=03311121"
ufj_reit = fund_data(isin="JP90C00084Z7", assoc="03311121")

#  "ＧＳ・日本株ファンドＤＣ牛若丸ＤＣ"https://toushin-lib.fwg.ne.jp/FdsWeb/FDST030000?isinCd=JP90C000NQ14
# eb/FDST030000/csv-file-download?isinCd=JP90C000NQ14&associFundCd=35313229"
ushiwakamaru = fund_data(isin="JP90C000NQ14", assoc="35313229")
# href="/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C000M6Q9&associFundCd=32314217

# "ＤＣニッセイ国内株式インデックス": dc_nissei_kokunai,https://toushin-lib.fwg.ne.jp/FdsWeb/FDST030000?isinCd=JP90C000AY68
# href="/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C000AY68&associFundCd=29316149"
dc_nissei_kokunai = fund_data(isin="JP90C000AY68", assoc="29316149")

#"三菱ＵＦＪＤＣ国内債券インデックスファンド"
#https://toushin-lib.fwg.ne.jp/FdsWeb/FDST030000?isinCd=JP90C00011E5
#href="/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C00011E5&associFundCd=03311022"
mitsubishi_kokunaisaiken=fund_data(isin="JP90C00011E5", assoc="03311022")

#"インデックスコレクション（国内債券）": 
#https://toushin-lib.fwg.ne.jp/FdsWeb/FDST030000?isinCd=JP90C00079W4
#href="/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C00079W4&associFundCd=6431210A"
index_collection_kokusai=fund_data(isin="JP90C00079W4", assoc="6431210A")

#"マイターゲット２０３０（確定拠出年金向け）": 
#https://toushin-lib.fwg.ne.jp/FdsWeb/FDST030000?isinCd=JP90C000C2A4
#href="/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C000C2A4&associFundCd=01313156"
my_target_2030=fund_data(isin="JP90C000C2A4", assoc="01313156")

#"マイターゲット２０３５（確定拠出年金向け）":
#href="/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C000G540&associFundCd=01312183"
my_target_2035=fund_data(isin="JP90C000G540", assoc="01312183")

#"マイターゲット２０４０（確定拠出年金向け）": 
#href="/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C000C291&associFundCd=01314156"
my_target_2040=fund_data(isin="JP90C000C291", assoc="01314156")

#"マイターゲット２０４５（確定拠出年金向け）": 
#href="/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C000G532&associFundCd=01313183"
my_target_2045=fund_data(isin="JP90C000G532", assoc="01313183")

#"マイターゲット２０５０（確定拠出年金向け）": 
#href="/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C000BHX9&associFundCd=0131D152"
my_target_2050=fund_data(isin="JP90C000BHX9", assoc="0131D152")

#"マイターゲット２０５５（確定拠出年金向け）": 
#href="/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C000G524&associFundCd=01314183"
my_target_2055=fund_data(isin="JP90C000G524", assoc="01314183")

#"マイターゲット２０６０（確定拠出年金向け）": 
#href="/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C000G516&associFundCd=01315183"
my_target_2060=fund_data(isin="JP90C000G516", assoc="01315183")

#"マイターゲット２０６５（確定拠出年金向け）": 
#href="/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C000LH25&associFundCd=01313213"
my_target_2065=fund_data(isin="JP90C000LH25", assoc="01313213")

#"インデックスコレクション（バランス株式３０）": 
#href="/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C00079T0&associFundCd=6431510A"
index_collection_blance30=fund_data(isin="JP90C00079T0", assoc="6431510A")

#"インデックスコレクション（バランス株式５０）": index_collection_blance50,
#href="/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C00079V6&associFundCd=6431610A"
index_collection_blance50=fund_data(isin="JP90C00079V6", assoc="6431610A")

#"インデックスコレクション（バランス株式７０）": 
#href="/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C00079X2&associFundCd=6431710A"
index_collection_blance70=fund_data(isin="JP90C00079X2", assoc="6431710A")


# df_bal_safe = fund_data(
#     isin="JP90C000FN25", assoc="4731317B"
# )  # たわらノーロード　バランス（堅実型）:バランス型
# df_bal_std = fund_data(
#     isin="JP90C000FN33", assoc="4731417B"
# )  # たわらノーロード　バランス（標準型）:バランス型
# df_bal_act = fund_data(
#     isin="JP90C000FN41", assoc="4731517B"
# )  # たわらノーロード　バランス（積極型）:バランス型
# df_jp_stk = fund_data(isin="JP90C00035B0", assoc="32311984")  # フィデリティ・日本成長株・ファンド：国内株式
# df_os_stk = fund_data(isin="JP90C0000SW7", assoc="03319008")  # 三菱ＵＦＪ 海外株式オープン：海外株式

# df_jp_bnd = fund_data(
#     isin="JP90C00078F1", assoc="03316109"
# )  # 三菱ＵＦＪ 日本国債ファンド（毎月決算型）：国内債券
# df_os_bnd = fund_data(
#     isin="JP90C000END3", assoc="0331A172"
# )  # ｅＭＡＸＩＳ Ｓｌｉｍ 先進国債券インデックス：海外債券

# df_jp_reit = fund_data(isin="JP90C0009145", assoc="01314133")  # 野村Jリートファンド：国内リート
# df_os_reit = fund_data(
#     isin="JP90C0003PX5", assoc="04312056"
# )  # ダイワ・グローバルＲＥＩＴ・オープン（毎月分配型）：海外リート

#######データ収集終わり

dict_assets = {
    # "バランス堅実型": df_bal_safe,
    # "バランス標準型": df_bal_std,
    # "バランス積極型": df_bal_act,
    # "国内株式": df_jp_stk,
    # "国内債券": df_jp_bnd,
    # "海外株式": df_os_stk,
    # "海外債券": df_os_bnd,
    # "国内リート": df_jp_reit,
    # "海外リート": df_os_reit,
    #401K(バランス)
    "マイターゲット２０３０（確定拠出年金向け）": my_target_2030,
    "マイターゲット２０３５（確定拠出年金向け）": my_target_2035,
    "マイターゲット２０４０（確定拠出年金向け）": my_target_2040,
    "マイターゲット２０４５（確定拠出年金向け）": my_target_2045,
    "マイターゲット２０５０（確定拠出年金向け）": my_target_2050,
    "マイターゲット２０５５（確定拠出年金向け）": my_target_2055,
    "マイターゲット２０６０（確定拠出年金向け）": my_target_2060,
    "マイターゲット２０６５（確定拠出年金向け）": my_target_2065,
    "インデックスコレクション（バランス株式３０）": index_collection_blance30,
    "インデックスコレクション（バランス株式５０）": index_collection_blance50,
    "インデックスコレクション（バランス株式７０）": index_collection_blance70,


    #401K(国内債券２つ)
    "三菱ＵＦＪＤＣ国内債券インデックスファンド": mitsubishi_kokunaisaiken,
    "インデックスコレクション（国内債券）": index_collection_kokusai,
    #401K(外国債券２つ)
    "三井住友・ＤＣ外国債券インデックスファンド": mitsui_gaikokusaiken,
    "野村外国債券インデックスファンド（確定拠出年金向け）": nomura_gaikokuseki,
    #401K(国内株式３つ)
    "ＤＣ日本株式インデックスファンドＬ":dc_SMTAM_nihonn,
    "ＤＣニッセイ国内株式インデックス": dc_nissei_kokunai,
    "ＧＳ・日本株ファンドＤＣ牛若丸ＤＣ": ushiwakamaru,
    #401K(海外株式３つ)
    "野村外国株式インデックスファンド・ＭＳＣＩ－ＫＯＫＵＳＡＩ（確定拠出年金向け）": nomura_gaikokukabu,
    "たわらノーロード先進国株式": tawara_senshin,
    "フィデリティ・世界割安成長株投信（確定拠出年金向け）": fidelity,
    #401k(国内REIT1つ)
    "三菱ＵＦＪ＜ＤＣ＞ＪーＲＥＩＴインデックスファンド": ufj_reit,
}

dict_assets2 = {
    "ニッセイ外国株": nissei_gaikokukabu,
    "楽天VTI": rakuten_zenbeikabu,
    "ｅＭＡＸＩＳ先進国株": emaxisslim_senshinkabu,
    "ｅＭＡＸＩＳ全米株S&P500": emaxisslim_zenbeikabu,
    "SBI新興国株式インデックス": sbi_shinkoukokukabu,}





# # 個別の投資信託ファンドのデータを取得する関数
# def fund_data(isin, assoc):
#     # CSVデータをダウンロードするURLを作成し読み込む
#     headURL = "https://toushin-lib.fwg.ne.jp/FdsWeb/FDST030000/"

#     isin_URL = "isinCd=" + isin
#     assoc_URL = "associFundCd=" + assoc
#     dl_URL = headURL + "csv-file-download?" + "&" + isin_URL + "&" + assoc_URL
#     # st.write(dl_URL)

#     # 年月日カラムを加工してデータ取得：年月日をパースする
#     my_parser = lambda date: datetime.strptime(date, "%Y年%m月%d日")
#     df = pd.read_csv(
#         dl_URL,
#         encoding="shift-jis",
#         index_col="年月日",
#         parse_dates=True,
#         date_parser=my_parser,
#     )
#     #st.write("df", isin, assoc, df)
#     return df




# for fund_name, df_fund in dict_assets.items():
#     # st.write(fund_name, df_fund)
#     df_fund_sum ,assets_list= fund_sel_data(
#         df_fund, df_fund_sum, fund_name, days ,assets_list
#     )  # open_date, close_date)


def fund_sel_data(dict_assets,days): 
    assets_list = []
    df_fund_sum = pd.DataFrame()
    # 投資信託ファンド分類の全データを結合
    for fund_name, df_fund in dict_assets.items():
        # st.write(fund_name, df_fund)
        # # open_date, close_date)
        if days > len(df_fund.index):
            st.write(fund_name," lack of data=>delete")
        else:
            df_fund_sel = df_fund #[days:]
            # st.write("df_fund_sel", df_fund_sel)
            # 列名の変更
            df_fund_sel = df_fund_sel.rename(columns={"基準価額(円)": fund_name})[[fund_name]]
            #st.write( fund_name , df_fund_sel)

            # 投資信託ファンド分類の結合
            # df_fund_sum = (
            #     pd.merge(
            #         df_fund_sum, df_fund_sel, left_index=True, right_index=True, how="inner"
            #     )
            df_fund_sum =( pd.concat([df_fund_sum,df_fund_sel], axis=1))
            assets_list.append(fund_name)
            #st.write(fund_name, df_fund_sum)
    return df_fund_sum,assets_list



# 時系列データの抽出期間を設定する関数
# fund_df:投資信託ファンド分類, fund_sum_df:結合した投資信託ファンド分類, fund_name:投資信託ファンド分類名
# open_date:投資信託ファンドの抽出開始日, close_date:投資信託ファンドの抽出終了日
# def fund_sel_data(df_fund, df_fund_sum, fund_name, days,assets_list):  # open_date, close_date):

#     # 投資信託ファンド分類の抽出データ期間
#     # df_fund_sel = df_fund.loc[
#     #     (df_fund.index >= open_date) & (df_fund.index <= close_date), :
#     # ]
#     #st.write(days,len(df_fund.index))
#     if days > len(df_fund.index):
#         st.write(fund_name," lack of data=>delete")
#     else:
#         df_fund_sel = df_fund #[days:]
#         # st.write("df_fund_sel", df_fund_sel)
#         # 列名の変更
#         df_fund_sel = df_fund_sel.rename(columns={"基準価額(円)": fund_name})[[fund_name]]
#         #st.write( fund_name , df_fund_sel)

#         # 投資信託ファンド分類の結合
#         # df_fund_sum = (
#         #     pd.merge(
#         #         df_fund_sum, df_fund_sel, left_index=True, right_index=True, how="inner"
#         #     )
#         df_fund_sum =( pd.concat([df_fund_sum,df_fund_sel], axis=1))
#         assets_list.append(fund_name)
#     #st.write(fund_name, df_fund_sum)
#     return df_fund_sum,assets_list


# df_bal_safe:バランス堅実型, df_bal_std:バランス標準型, df_bal_act:バランス積極型
# df_jp_stk:国内株式, df_os_stk:海外株式, df_jp_bnd:国内債券, df_os_bnd:海外債券
# df_jp_reit:国内リート, df_os_reit:海外リート

# # 野村外国株式インデックスファンド・ＭＳＣＩ－ＫＯＫＵＳＡＩ（確定拠出年金向け）401k
# nomura_gaikokukabu = fund_data(isin="JP90C0002Z87", assoc="01312022")
# # 三井住友DC外国債券()401k
# mitsui_gaikokusaiken = fund_data(isin="JP90C0000KL7", assoc="79312024")  # done
# # ニッセイ外国株
# nissei_gaikokukabu = fund_data(isin="JP90C0009VE0", assoc="2931113C")  # done
# # 楽天VTI
# rakuten_zenbeikabu = fund_data(isin="JP90C000FHD2", assoc="9I312179")  # done
# # emax is slim 先進国
# emaxisslim_senshinkabu = fund_data(isin="JP90C0006LG2", assoc="0331509A")
# # emax is slim 全米株S&P500
# emaxisslim_zenbeikabu = fund_data(isin="JP90C000GKC6", assoc="03311187")  # done
# # SBI新興国株式インデックス
# sbi_shinkoukokukabu = fund_data(isin="JP90C000FQQ5", assoc="8931117C")  # done
# #DC日本株式インデックスファンドL SMTAM 日株インデックスL
# #https://toushin-lib.fwg.ne.jp/FdsWeb/FDST030000?isinCd=JP90C0000367
# #"/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C0000367&associFundCd=64311024"
# dc_SMTAM_nihonn= fund_data(isin="JP90C0000367",assoc="64311024")

# # 野村外国債券インデックスファンド（確定拠出年金向け）
# # https://toushin-lib.fwg.ne.jp/FdsWeb/FDST030000  ?isinCd=JP90C0002ZJ5
# nomura_gaikokuseki = fund_data(isin="JP90C0002ZJ5", assoc="0131102B")
# # フィデリティ・世界割安成長株投信（確定拠出年金向け）／愛称：テンバガー・ハンター
# fidelity = fund_data(isin="JP90C000M6Q9", assoc="32314217")
# # たわらノーロード先進国株式
# # https://toushin-lib.fwg.ne.jp/FdsWeb/FDST030000?isinCd=JP90C000CMK4
# # /FdsWeb/FDST030000/csv-file-download?isinCd=JP90C000CMK4&associFundCd=4731B15C
# tawara_senshin = fund_data(isin="JP90C000CMK4", assoc="4731B15C")

# # https://toushin-lib.fwg.ne.jp/FdsWeb/FDST030000?isinCd=JP90C00084Z7
# # 三菱ＵＦＪ＜ＤＣ＞ＪーＲＥＩＴインデックスファンド
# # /FdsWeb/FDST030000/csv-file-download?isinCd=JP90C00084Z7&associFundCd=03311121"
# ufj_reit = fund_data(isin="JP90C00084Z7", assoc="03311121")

# #  "ＧＳ・日本株ファンドＤＣ牛若丸ＤＣ"https://toushin-lib.fwg.ne.jp/FdsWeb/FDST030000?isinCd=JP90C000NQ14
# # eb/FDST030000/csv-file-download?isinCd=JP90C000NQ14&associFundCd=35313229"
# ushiwakamaru = fund_data(isin="JP90C000NQ14", assoc="35313229")
# # href="/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C000M6Q9&associFundCd=32314217

# # "ＤＣニッセイ国内株式インデックス": dc_nissei_kokunai,https://toushin-lib.fwg.ne.jp/FdsWeb/FDST030000?isinCd=JP90C000AY68
# # href="/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C000AY68&associFundCd=29316149"
# dc_nissei_kokunai = fund_data(isin="JP90C000AY68", assoc="29316149")

# #"三菱ＵＦＪＤＣ国内債券インデックスファンド"
# #https://toushin-lib.fwg.ne.jp/FdsWeb/FDST030000?isinCd=JP90C00011E5
# #href="/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C00011E5&associFundCd=03311022"
# mitsubishi_kokunaisaiken=fund_data(isin="JP90C00011E5", assoc="03311022")

# #"インデックスコレクション（国内債券）": 
# #https://toushin-lib.fwg.ne.jp/FdsWeb/FDST030000?isinCd=JP90C00079W4
# #href="/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C00079W4&associFundCd=6431210A"
# index_collection_kokusai=fund_data(isin="JP90C00079W4", assoc="6431210A")

# #"マイターゲット２０３０（確定拠出年金向け）": 
# #https://toushin-lib.fwg.ne.jp/FdsWeb/FDST030000?isinCd=JP90C000C2A4
# #href="/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C000C2A4&associFundCd=01313156"
# my_target_2030=fund_data(isin="JP90C000C2A4", assoc="01313156")

# #"マイターゲット２０３５（確定拠出年金向け）":
# #href="/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C000G540&associFundCd=01312183"
# my_target_2035=fund_data(isin="JP90C000G540", assoc="01312183")

# #"マイターゲット２０４０（確定拠出年金向け）": 
# #href="/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C000C291&associFundCd=01314156"
# my_target_2040=fund_data(isin="JP90C000C291", assoc="01314156")

# #"マイターゲット２０４５（確定拠出年金向け）": 
# #href="/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C000G532&associFundCd=01313183"
# my_target_2045=fund_data(isin="JP90C000G532", assoc="01313183")

# #"マイターゲット２０５０（確定拠出年金向け）": 
# #href="/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C000BHX9&associFundCd=0131D152"
# my_target_2050=fund_data(isin="JP90C000BHX9", assoc="0131D152")

# #"マイターゲット２０５５（確定拠出年金向け）": 
# #href="/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C000G524&associFundCd=01314183"
# my_target_2055=fund_data(isin="JP90C000G524", assoc="01314183")

# #"マイターゲット２０６０（確定拠出年金向け）": 
# #href="/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C000G516&associFundCd=01315183"
# my_target_2060=fund_data(isin="JP90C000G516", assoc="01315183")

# #"マイターゲット２０６５（確定拠出年金向け）": 
# #href="/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C000LH25&associFundCd=01313213"
# my_target_2065=fund_data(isin="JP90C000LH25", assoc="01313213")

# #"インデックスコレクション（バランス株式３０）": 
# #href="/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C00079T0&associFundCd=6431510A"
# index_collection_blance30=fund_data(isin="JP90C00079T0", assoc="6431510A")

# #"インデックスコレクション（バランス株式５０）": index_collection_blance50,
# #href="/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C00079V6&associFundCd=6431610A"
# index_collection_blance50=fund_data(isin="JP90C00079V6", assoc="6431610A")

# #"インデックスコレクション（バランス株式７０）": 
# #href="/FdsWeb/FDST030000/csv-file-download?isinCd=JP90C00079X2&associFundCd=6431710A"
# index_collection_blance70=fund_data(isin="JP90C00079X2", assoc="6431710A")


# # df_bal_safe = fund_data(
# #     isin="JP90C000FN25", assoc="4731317B"
# # )  # たわらノーロード　バランス（堅実型）:バランス型
# # df_bal_std = fund_data(
# #     isin="JP90C000FN33", assoc="4731417B"
# # )  # たわらノーロード　バランス（標準型）:バランス型
# # df_bal_act = fund_data(
# #     isin="JP90C000FN41", assoc="4731517B"
# # )  # たわらノーロード　バランス（積極型）:バランス型
# # df_jp_stk = fund_data(isin="JP90C00035B0", assoc="32311984")  # フィデリティ・日本成長株・ファンド：国内株式
# # df_os_stk = fund_data(isin="JP90C0000SW7", assoc="03319008")  # 三菱ＵＦＪ 海外株式オープン：海外株式

# # df_jp_bnd = fund_data(
# #     isin="JP90C00078F1", assoc="03316109"
# # )  # 三菱ＵＦＪ 日本国債ファンド（毎月決算型）：国内債券
# # df_os_bnd = fund_data(
# #     isin="JP90C000END3", assoc="0331A172"
# # )  # ｅＭＡＸＩＳ Ｓｌｉｍ 先進国債券インデックス：海外債券

# # df_jp_reit = fund_data(isin="JP90C0009145", assoc="01314133")  # 野村Jリートファンド：国内リート
# # df_os_reit = fund_data(
# #     isin="JP90C0003PX5", assoc="04312056"
# # )  # ダイワ・グローバルＲＥＩＴ・オープン（毎月分配型）：海外リート

# 投資信託ファンド分類に対応する変数を設定
dict_assets = {
    # "バランス堅実型": df_bal_safe,
    # "バランス標準型": df_bal_std,
    # "バランス積極型": df_bal_act,
    # "国内株式": df_jp_stk,
    # "国内債券": df_jp_bnd,
    # "海外株式": df_os_stk,
    # "海外債券": df_os_bnd,
    # "国内リート": df_jp_reit,
    # "海外リート": df_os_reit,
    #401K(バランス)
    "マイターゲット２０３０（確定拠出年金向け）": my_target_2030,
    "マイターゲット２０３５（確定拠出年金向け）": my_target_2035,
    "マイターゲット２０４０（確定拠出年金向け）": my_target_2040,
    "マイターゲット２０４５（確定拠出年金向け）": my_target_2045,
    "マイターゲット２０５０（確定拠出年金向け）": my_target_2050,
    "マイターゲット２０５５（確定拠出年金向け）": my_target_2055,
    "マイターゲット２０６０（確定拠出年金向け）": my_target_2060,
    "マイターゲット２０６５（確定拠出年金向け）": my_target_2065,
    "インデックスコレクション（バランス株式３０）": index_collection_blance30,
    "インデックスコレクション（バランス株式５０）": index_collection_blance50,
    "インデックスコレクション（バランス株式７０）": index_collection_blance70,


    #401K(国内債券２つ)
    "三菱ＵＦＪＤＣ国内債券インデックスファンド": mitsubishi_kokunaisaiken,
    "インデックスコレクション（国内債券）": index_collection_kokusai,
    #401K(外国債券２つ)
    "三井住友・ＤＣ外国債券インデックスファンド": mitsui_gaikokusaiken,
    "野村外国債券インデックスファンド（確定拠出年金向け）": nomura_gaikokuseki,
    #401K(国内株式３つ)
    "ＤＣ日本株式インデックスファンドＬ":dc_SMTAM_nihonn,
    "ＤＣニッセイ国内株式インデックス": dc_nissei_kokunai,
    "ＧＳ・日本株ファンドＤＣ牛若丸ＤＣ": ushiwakamaru,
    #401K(海外株式３つ)
    "野村外国株式インデックスファンド・ＭＳＣＩ－ＫＯＫＵＳＡＩ（確定拠出年金向け）": nomura_gaikokukabu,
    "たわらノーロード先進国株式": tawara_senshin,
    "フィデリティ・世界割安成長株投信（確定拠出年金向け）": fidelity,
    #401k(国内REIT1つ)
    "三菱ＵＦＪ＜ＤＣ＞ＪーＲＥＩＴインデックスファンド": ufj_reit,
}

dict_assets2 = {
    "ニッセイ外国株": nissei_gaikokukabu,
    "楽天VTI": rakuten_zenbeikabu,
    "ｅＭＡＸＩＳ先進国株": emaxisslim_senshinkabu,
    "ｅＭＡＸＩＳ全米株S&P500": emaxisslim_zenbeikabu,
    "SBI新興国株式インデックス": sbi_shinkoukokukabu,}


#######################
st.title("信託投資考察")
# 投資信託ファンド分類の抽出期間を設定

# now = datetime.today()
# now = now.tz_localize(None)
days = 365
# open_date = now - timedelta(days=days)  # .tz_localize(None)
# st.write("open_date", open_date.tzinfo, "now", now.tzinfo)
# open_date = "2017-11-08"  # 抽出開始日：たわらノーロード　バランスの開設日が2017-11-8
# close_date = now  # "2021-09-29"  # 抽出終了日：検証用CSVデータのダウンロード実行日が2021-09-29

df_fund_sum ,assets_list=fund_sel_data(dict_assets,days)

# assets_list = []
# df_fund_sum = pd.DataFrame()
# # 投資信託ファンド分類の全データを結合
# for fund_name, df_fund in dict_assets.items():
#     # st.write(fund_name, df_fund)
#     df_fund_sum ,assets_list= fund_sel_data(
#         df_fund, df_fund_sum, fund_name, days ,assets_list
#     )  # open_date, close_date)

df_fund_sum1=df_fund_sum
df_fund_sum=df_fund_sum.tail(250)
st.write("df_fund_sum.tail()", df_fund_sum)



# データの要約統計量を表示
# データ個数, 平均, 標準偏差, 最小値, 第一四分位数, 第二四分位数, 第三四分位数, 最大値
# st.write(df_fund_sum.describe())


# リターン(年率%) ：トータルリターンは基準価額の変動、年間営業日は260日
# 計算式：((トータルリターン（率）+1）^（年間営業日/運用期間）－1)) * 100
# st.write(len(df_fund_sum))  # 運用期間

fig_all_fund = go.Figure()
for i in df_fund_sum.columns.to_list():
    fig_all_fund.add_trace(go.Scatter(x=df_fund_sum.index, y=df_fund_sum[i], name=i))
fig_all_fund.update_xaxes(
    # rangebreaks=[dict(values=d_breaks)],
    tickformat="%Y/%m/%d",
    title="Date",
)
st.plotly_chart(fig_all_fund)

# リターン(年率%) ：トータルリターンは基準価額の変動、年間営業日は250日
# 計算式：((トータルリターン（率）+1）^（年間営業日/運用期間）－1)) * 100
df_return = (
    (pd.DataFrame((df_fund_sum.pct_change()[1:] + 1).prod()).T)
    ** (250 / (len(df_fund_sum)))#
    - 1
) * 100

st.write("リターン", df_return.T)


# リスク(年率%)
# 計算式：（リターンの標準偏差）×（260^（1/2））×100
# 日毎の標準偏差を算出
df_risk = pd.DataFrame((df_fund_sum.pct_change()[1:]).std()).T

# 250乗根してリスク(年率(%))を算出
df_risk = df_risk * (250 ** (1 / 2)) * 100
st.write("risk", df_risk.T)

# 投資信託ファンド分類の相関係数を算出
# corr()メソッド
#st.write("corr前", df_fund_sum)
df_corr = df_fund_sum.corr()
#st.write("相関", df_corr.head(9))
import plotly.graph_objects as go

fig_heat = go.Figure()
fig_heat.add_trace(
    go.Heatmap(
        x=df_corr.columns,
        y=df_corr.index,
        z=np.array(df_corr),
    )
)
st.plotly_chart(fig_heat)


# ######現比率計算はまだできていない
# # ポートフォリオのリターンとリスクを算出

# X = len(df_return.T)  # 投資信託ファンドの分類数
# # 投資ウェイト（合計=1.0)
# # 1(国内債券・海外債券)：3(バランス型・国内株式・海外株式・国内リート・海外リート)
# y1 = 0.132  # バランス堅実型
# y2 = 0.132  # バランス標準型
# y3 = 0.13  # バランス積極型
# y4 = 0.132  # 国内株式
# y5 = 0.041  # 国内債券
# y6 = 0.13  # 海外株式
# y7 = 0.041  # 海外債券
# y8 = 0.132  # 国内リート
# y9 = 0.13  # 海外リート
# y10 = 0.1
# y11 = 0.1
# y12 = 0.1
# y13 = 0.1
# y14=0.1
# y15=0.1
# y16=0.1
# y17=0.1
# y18=0.1
# y19=0.1
# y20=0.1
# y21=0.1
# y22=0.1

# y = np.array([y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13,y14,y15,y16,y17,y18,y19,y20,y21,y22,])


# # ポートフォリオのリターン(年率%)計算
# # (各投資信託ファンド分類のリターン(年率%) × 投資ウェイト)の合計
# Return = np.dot(y, df_return.T.to_numpy()).item()
# Return = "{:.2f}".format(Return)
# Return = float(Return)
# st.write("リターン(年率%) :", Return, type(Return), float(Return))

# # ポートフォリオのリスク(年率%)計算
# # (X × X)の投資ウェイトとリスクと相関係数を掛け合わせて計算
# # 掛け合わせた結果(分散)を乗根
# # 投資信託ファンド分類のウェイト用行列
# df_fund_weight = pd.DataFrame(
#     np.dot((y.reshape(X, 1)), (y.reshape(1, X))),
#     index=df_corr.index,
#     columns=df_corr.columns,
# )


# # 投資信託ファンド分類の標準偏差用行列
# df_fund_risk = pd.DataFrame(
#     np.dot((df_risk.to_numpy().reshape(X, 1)), (df_risk.to_numpy().reshape(1, X))),
#     index=df_corr.index,
#     columns=df_corr.columns,
# )

# # 投資ウェイトとリスクと相関係数を掛け合わせて計算
# #df_fund_val = df_fund_weight * df_fund_risk * df_corr
# #ウェイトがまだ計算できていないからウェイトをなしとする
# df_fund_val = df_fund_risk * df_corr

# # リスク(年率%)
# risk = (np.sum(df_fund_val.to_numpy().reshape(1, -1))) ** (1 / 2)
# risk = "{:.2f}".format(risk)
# risk_m = float(risk)
# st.write("リスク  (年率%) :", risk_m, type(risk_m), float(risk_m))

#############################################################
# st.write("効果的ポートフォリオ（pypfopt.efficient_frontier バージョン）")
# # 効率的なポートフォリをを見えるかする、必要なモジュールをインポートする
# import numpy as np
# from pypfopt.efficient_frontier import EfficientFrontier  # 効率的フロンティア分析用モジュール
# from pypfopt import risk_models  # リスクモデルにより共分散行列を計算
# from pypfopt import expected_returns  # リターンを算出
# import math  # 数学処理のモジュール
# import plotly.graph_objects as go  # plotlyでデータを可視化


# # 　年間営業日は250日とする
# rturn = expected_returns.mean_historical_return(
#     df_fund_sum, frequency=250
# )  # リターンの計算,年間営業日:250
# cov = risk_models.sample_cov(df_fund_sum, frequency=250)  # 分散・共分散行列の計算
# risk = (df_fund_sum.pct_change().dropna(how="all")).std()  # 標準偏差の計算
# risk = ((risk * risk) * 250).apply(math.sqrt)  # 乗根によりリスクの計算

# # 投資信託ファンド分類のリスク・リターンのデータフレーム作成
# df_plot = pd.DataFrame()
# df_plot["ファンド分類"] = rturn.index
# df_plot["リスク"] = risk.values
# df_plot["リターン"] = rturn.values

# # 効率的フロンティアの計算
# ef = EfficientFrontier(rturn, cov)

# # 効率的なリターンのパターンの作成
# # arange(初期値(amin()),終了値(amax()),ステップサイズ)で生成
# t_rturn = np.arange(round(np.amin(rturn), 3), round(np.amax(rturn), 3), 0.001)

# # 効率的なリターン
# tvols = []
# res_rturn = []
# res_risk = []
#df_weight = pd.DataFrame(columns=list(df_fund_sum.columns), index=t_rturn)

# 効率的なリターンのウェイト算出

# for tr in t_rturn:
#     try:
#         wt = ef.efficient_return(target_return=tr)
#         wt = ef.clean_weights()
#         pref = ef.portfolio_performance()
#         res_rturn += [pref[0]]
#         res_risk += [pref[1]]
#         df_weight.loc[tr, :] = list(wt.values())
#     except:
#         # マイナス値は例外処理
#         st.write("例外処理:", tr)

# # 効率的フロンティアの描画・可視化
# flont_line = pd.DataFrame({"リスク": res_risk, "リターン": res_rturn})

# トレース図にレイアウト情報を付加

# st.write("Plot", df_plot)
# st.write("flont", flont_line)
# layout = go.Layout(
#     xaxis={"title": "リスク [%]"},
#     yaxis={"title": "リターン [%]"},
# )
# fig = go.Figure(layout=layout)

# # 散布図 (Scatter Plot)情報を追加
# fig.add_trace(
#     go.Scatter(
#         x=df_plot["リスク"] * 100,
#         y=df_plot["リターン"] * 100,
#         mode="markers+text",
#         text=df_plot["ファンド分類"],
#         textposition="top center",
#         name="Fund_Type",
#     )
# )
# fig.add_trace(
#     go.Scatter(
#         x=flont_line["リスク"] * 100,
#         y=flont_line["リターン"] * 100,
#         mode="lines",
#         name="EF:EfficientFrontier",
#     )
# )

#現在のポートフォリををグラフに表示（まだ実装していない）
# xx = [risk_m]
# yy = [Return]
# st.write(xx, yy)
# # 現在のポートフォリオの位置
# fig.add_trace(
#     go.Scatter(
#         x=[risk_m],
#         y=[Return],
#         mode="markers+text",
#         text="Current",
#         textposition="top center",
#         name="CurrentPortfolio",
#     )
# )

# # fig.show()
# st.plotly_chart(fig)
#st.write("df_weight", df_weight)

####################

#https://note.com/225_dow/n/ne55f38d595fa
#https://optrip.xyz/?p=1668
#https://worth2know.com/investment/
import matplotlib.pyplot as plt
st.write("効果的ポートフォリオ（ガチ計算）")

data=df_fund_sum
selected=assets_list

# calculate daily and annual returns of the stocks
#returns_daily = table.pct_change()
returns_daily = data.pct_change()
#returns_daily = returns_daily.fillna(0, inplace=True)  # Nanを0で埋める
returns_annual = returns_daily.mean() * 250

# get daily and covariance of returns of the stock
cov_daily = returns_daily.cov()
cov_annual = cov_daily * 250

st.write("returns_daily",returns_annual,"cov_annual",cov_annual)


# empty lists to store returns, volatility and weights of imiginary portfolios
port_returns = []
port_volatility = []
sharpe_ratio = []
stock_weights = []


# set the number of combinations for imaginary portfolios
num_assets = len(selected)
num_portfolios = 50000

#set random seed for reproduction's sake
np.random.seed(101)


# populate the empty lists with each portfolios returns,risk and weights
for single_portfolio in range(num_portfolios):
   weights = np.random.random(num_assets)
   weights /= np.sum(weights)
   returns = np.dot(weights, returns_annual)
   volatility = np.sqrt(np.dot(weights.T, np.dot(cov_annual, weights)))
   sharpe = returns / volatility
   sharpe_ratio.append(sharpe)
   port_returns.append(returns)
   port_volatility.append(volatility)
   stock_weights.append(weights)
   
# a dictionary for Returns and Risk values of each portfolio
portfolio = {'Returns': port_returns,
            'Volatility': port_volatility,
            'Sharpe Ratio': sharpe_ratio}
            
# extend original dictionary to accomodate each ticker and weight in the portfolio
for counter,symbol in enumerate(selected):
   portfolio[symbol+' Weight'] = [Weight[counter] for Weight in stock_weights]


# make a nice dataframe of the extended dictionary
df = pd.DataFrame(portfolio)

# get better labels for desired arrangement of columns
column_order = ['Returns', 'Volatility', 'Sharpe Ratio'] + [stock+' Weight' for stock in selected]

# reorder dataframe columns
df = df[column_order]



# find min Volatility & max sharpe values in the dataframe (df)
min_volatility = df['Volatility'].min()
max_sharpe = df['Sharpe Ratio'].max()

# use the min, max values to locate and create the two special portfolios
sharpe_portfolio = df.loc[df['Sharpe Ratio'] == max_sharpe]
min_variance_port = df.loc[df['Volatility'] == min_volatility]

# plot frontier, max sharpe & min Volatility values with a scatterplot
fig_pori=plt.style.use('seaborn-dark')
df.plot.scatter(x='Volatility', y='Returns', c='Sharpe Ratio',
               cmap='RdYlGn', edgecolors='black', figsize=(10, 8), grid=True)
plt.scatter(x=sharpe_portfolio['Volatility'], y=sharpe_portfolio['Returns'], c='red', marker='D', s=200,label='sharpe ratio max')
plt.scatter(x=min_variance_port['Volatility'], y=min_variance_port['Returns'], c='blue', marker='D', s=200,label='min_volatility' )
plt.xlabel('Volatility (Std. Deviation)')
plt.ylabel('Expected Returns')
plt.title('Efficient Frontier')
plt.show()



# # plot frontier, max sharpe & min Volatility values with a scatterplot
# fig_pori=plt.style.use('seaborn-dark')
# df.plot.scatter(x='Volatility', y='Returns', c='Sharpe Ratio',
#                cmap='RdYlGn', edgecolors='black', figsize=(10, 8), grid=True)
# plt.xlabel('Volatility (Std. Deviation)')
# plt.ylabel('Expected Returns')
# plt.title('Efficient Frontier')
# plt.show()
st.pyplot(fig_pori)

# print the details of the 2 special portfolios
st.write("ボラティリティが最小",min_variance_port.T)
st.write("シャープレシオが最大(最も効率的)",sharpe_portfolio.T)


#############################################################3
# 精度確認
# 必要なモジュールをインポートする
# import seaborn as sns  # seabornをインポート
# import matplotlib.pyplot as plt
# import numpy as np

# # 配列を作成
# # r_x : リターン, r_y ：リスク, t_z ：投資信託ファンド分類
# r_x = np.array(
#     [
#         3.247211,
#         6.694885,
#         9.090114,
#         8.666589,
#         -1.519071,
#         18.360784,
#         2.440561,
#         12.740682,
#         0.461850,
#     ]
# )
# r_y = np.array(
#     [
#         3.656905,
#         8.300171,
#         13.228247,
#         19.817743,
#         2.040158,
#         22.701214,
#         6.424558,
#         22.928642,
#         20.942769,
#     ]
# )
# t_z = np.array(
#     ["バランス堅実型", "バランス標準型", "バランス積極型", "国内株式", "国内債券", "海外株式", "海外債券", "国内リート", "海外リート"]
# )
# array1 = np.array([r_x, r_y, t_z])

# 散布図にレイアウト情報を付加
# plt.xlabel("RISK")
# plt.ylabel("RETURN")

# sns.regplot() : 線形回帰モデル
# fit_reg = True : 線形回帰モデルを出力
# x_ci = 95 : 回帰を行う際の信頼区間 (%),95%を指定
# figsns = sns.regplot(data=array1, x=r_y, y=r_x, fit_reg=True, x_ci=95)
# figsns = go.Figure()
# figsns.add_trace(
#     go.Satter(
#         array1, x=r_y, y=r_x, trendline="ols", trendline_color_override="darkblue"
#     )
# )
# st.plotly_chart(figsns)
###############################


# # おすすめの投資先比率
# layout = go.Layout(
#     xaxis={"title": "リターン[%]"},
#     yaxis={
#         "title": "比率[%]",
#     },
# )
# fig2 = go.Figure(layout=layout)

# for col in df_weight:
#     fig2.add_trace(
#         go.Scatter(
#             x=df_weight.index * 100,
#             y=df_weight[col] * 100,
#             hoverinfo="x+y",
#             mode="lines",
#             line=dict(
#                 width=0.5,
#             ),
#             name=col,
#             stackgroup="one",  # define stack group
#         )
#     )

# st.plotly_chart(fig2)

##################################
#実際のDCで計算
##########
import numpy as np
import pandas as pd
from datetime import datetime
import urllib.request


# JE:日本株、EE:新興国株、IE:先進国株、JB:日本債券、EB:新興国債券、IB:先進国債券、IR:先進国リート、JR:日本リート



# 全ファンドの累積基準価額をひとつにまとめたデータを作成
#DC向け＆投信総合検索ライブラリーを活用
#assets_list = []
df_all = pd.DataFrame()

for fund_name, df_fund in dict_assets.items():
 #for asset in assets:  # assets:
    # st.write("asset",asset)
    # st.write(url_list[asset])
    # df = pd.read_csv(
    #     url_list[asset],  # asset_file,
    #     skiprows=[0],
    #     names=["date", "nav", "div", "aum"],  
    #     # date,基準日、nav:基準価格,div:配当金、aum:純資産総額
    #     parse_dates=True,
    #     index_col=0,
    # )
    # st.write(df)
    #assets_list.append(fund_name)

    df=df_fund
    df=df.rename(columns={'基準価額(円)': 'nav', '分配金': 'div'})
    #st.write(fund_name,df)

    
    df["div"] = pd.to_numeric(df["div"], errors="coerce")
    #欠損に0を入れる
    df["div"] = df["div"].fillna(0)

    df["cum_nav"] = (df["nav"] + df["div"]) / df["nav"].shift(1)
    df[fund_name] = df["cum_nav"].cumprod()
    df_all[fund_name] = df[fund_name]
    #st.write("df_all",df_all)


# 日次データを月次データに変換してシグナル判定
dfm = df_all.resample("M").ffill()
st.write("dfm1",dfm)
dfm = dfm[dfm.index < datetime.now()]
#st.write("dfm2",dfm)

calc = pd.DataFrame(columns=assets_list)
calc.loc["asset class"] = assets_list

# （3ヶ月＋６ヶ月＋１２ヶ月）/３
calc.loc["3 months"] = (dfm.iloc[-1] / dfm.iloc[-4] - 1) * 100
calc.loc["6 months"] = (dfm.iloc[-1] / dfm.iloc[-7] - 1) * 100
calc.loc["12 months"] = (dfm.iloc[-1] / dfm.iloc[-13] - 1) * 100
calc.loc["mean"] = (
    calc.loc["3 months"] + calc.loc["6 months"] + calc.loc["12 months"]
) / 3
calc = calc.fillna(0)
#st.write("calc",calc)
calc.loc["rank"] = calc.loc["mean"].rank(ascending=False).astype(int)

calc.loc["latest nav"] = dfm.iloc[-1]
calc.loc["12ma NAV"] = dfm.iloc[-12:].mean()
calc.loc["Buy/Sell"] = np.where(
    calc.loc["latest nav"] > calc.loc["12ma NAV"], "Buy", "Sell"
)

st.write(calc.T)
# 月次シグナル判定結果を表示
date = dfm.index.max()
st.write(str(date.year) + "年" + str(date.month) + "月末のシグナルは以下の通りとなりました。")
st.write(calc.T.set_index("rank")[["asset class", "Buy/Sell"]].sort_index())


for n in range(len(df_all)-13):
    st.write("過去約5年のシミュレーション")
    #i月
    n=n+1

    # （3ヶ月＋６ヶ月＋１２ヶ月）/３
    calc.loc["3 months"] = (dfm.iloc[-n] / dfm.iloc[-n-3] - 1) * 100
    calc.loc["6 months"] = (dfm.iloc[-n] / dfm.iloc[-n-6] - 1) * 100
    calc.loc["12 months"] = (dfm.iloc[-n] / dfm.iloc[-n-12] - 1) * 100
    calc.loc["mean"] = (
        calc.loc["3 months"] + calc.loc["6 months"] + calc.loc["12 months"]
    ) / 3
    calc = calc.fillna(0)
    #st.write("calc",calc)
    calc.loc["rank"] = calc.loc["mean"].rank(ascending=False).astype(int)

    calc.loc["latest nav"] = dfm.iloc[-n]
    calc.loc["12ma NAV"] = dfm.iloc[-n-11:].mean()
    calc.loc["Buy/Sell"] = np.where(
        calc.loc["latest nav"] > calc.loc["12ma NAV"], "Buy", "Sell"
    )

    # st.write(calc)
    calc1=calc.T

    st.write(n,"ヶ月前",calc1[calc1["Buy/Sell"] == "Buy"].sort_values("rank").head(2)[["rank","latest nav", "Buy/Sell"]])
    # 月次シグナル判定結果を表示
    # date = dfm.index.max()
    # st.write(n,"ヶ月前",str(date.year) + "年" + str(date.month) + "月末のシグナルは以下の通りとなりました。")
    # st.write(calc.T.set_index("rank")[["asset class", "Buy/Sell"]].sort_index())





###########
############
# 移動平均＋レラティブストレングス投資法
# https://qiita.com/hiroshi_ichihara/items/caaff4ddf09c2784473c
# http://etftrendfollow.seesaa.net/article/152055593.html
# 「12ヶ月移動平均＋3-6-12ヶ月レラティブ・ストレングス投資」とは







#########################################################

"""
「12ヶ月移動平均＋3-6-12ヶ月レラティブ・ストレングス投資」とは、次のような投資法です。
１．月末に、複数の資産クラスの、「3ヶ月リターン、6ヶ月リターン、12ヶ月リターンの平均値」（以下、3-6-12ヶ月リターン）を計算する。
２．3-6-12ヶ月リターンが高い上位3資産を抽出する。
３．この3資産の中で、市場価格が12ヶ月移動平均を上回っている資産を抽出し、均等配分に投資する。
４．以上を毎月繰り返す。
要するに、直近のリターンが相対的に高い、つまり価格の勢いが相対的（＝レラティブ）に強い（ストロング）銘柄に投資する手法です。
今回は、日本株式、先進国株式、新興国株式、日本債券、先進国債券、新興国債券、日本REIT、外国REIT、コモディティ、9つの資産を対象に検証しました。
"""

# import numpy as np
# import pandas as pd
# from datetime import datetime
# import urllib.request

# # SMTAMウェブサイトから投信データcsvを取得して保存。
# # スクレイピングを最小限に抑えるため、一度スクレイピングしたらcsvファイルとして保存。

# # JE:日本株、EE:新興国株、IE:先進国株、JB:日本債券、EB:新興国債券、IB:先進国債券、IR:先進国リート、JR:日本リート
# url_list = {
#     "JE": "https://www.smtam.jp/chart_data/140833/140833.csv",
#     "EE": "https://www.smtam.jp/chart_data/140841/140841.csv",
#     "IE": "https://www.smtam.jp/chart_data/140834/140834.csv",
#     "JB": "https://www.smtam.jp/chart_data/140835/140835.csv",
#     "EB": "https://www.smtam.jp/chart_data/140842/140842.csv",
#     "IB": "https://www.smtam.jp/chart_data/140836/140836.csv",
#     "IR": "https://www.smtam.jp/chart_data/140838/140838.csv",
#     "JR": "https://www.smtam.jp/chart_data/140837/140837.csv",
# }


# # for key in url_list:
# #     url = url_list[key]
# #     title = "{0}.csv".format(key)
# # urllib.request.urlretrieve(url,title)


# # 全ファンドの累積基準価額をひとつにまとめたデータを作成
# assets = ["JE", "EE", "IE", "JB", "EB", "IB", "JR", "IR"]
# df_all = pd.DataFrame()

# for asset in assets:  # assets:
#     # asset_file = "{0}.csv".format(asset)
#     st.write(url_list[asset])
#     df = pd.read_csv(
#         url_list[asset],  # asset_file,
#         skiprows=[0],
#         names=["date", "nav", "div", "aum"],  # date,基準日、nav:基準価格,div:配当金、aum:純資産総額
#         parse_dates=True,
#         index_col=0,
#     )
#     st.write(df)
#     # https://note.com/startworkout/n/n831375b7e0d3
#     # RS
#     st.write("df[nav][-1]", df["nav"][-1])
#     RS = (
#         ((df["nav"][-1] - df["nav"][-63]) / df["nav"][-63] * 0.4)
#         + (((df["nav"][-1] - df["nav"][-126]) / df["nav"][-126]) * 0.2)
#         + (((df["nav"][-1] - df["nav"][-189]) / df["nav"][-189]) * 0.2)
#         + (((df["nav"][-1] - df["nav"][-252]) / df["nav"][-252]) * 0.2)
#     ) * 99

#     st.write(RS)

#     df["div"] = pd.to_numeric(df["div"], errors="coerce")
#     df["div"] = df["div"].fillna(0)

#     df["cum_nav"] = (df["nav"] + df["div"]) / df["nav"].shift(1)
#     df[asset] = df["cum_nav"].cumprod()
#     df_all[asset] = df[asset]


# # 日次データを月次データに変換してシグナル判定
# dfm = df_all.resample("M").ffill()
# dfm = dfm[dfm.index < datetime.now()]

# calc = pd.DataFrame(columns=["JE", "EE", "IE", "JB", "EB", "IB", "JR", "IR"])
# calc.loc["asset class"] = [
#     "日本株",
#     "新興国株",
#     "先進国株",
#     "日本債券",
#     "新興国債券",
#     "先進国債券",
#     "日本リート",
#     "先進国リート",
# ]
# # （3ヶ月＋６ヶ月＋１２ヶ月）/３
# calc.loc["3 months"] = (dfm.iloc[-1] / dfm.iloc[-4] - 1) * 100
# calc.loc["6 months"] = (dfm.iloc[-1] / dfm.iloc[-7] - 1) * 100
# calc.loc["12 months"] = (dfm.iloc[-1] / dfm.iloc[-13] - 1) * 100
# calc.loc["mean"] = (
#     calc.loc["3 months"] + calc.loc["6 months"] + calc.loc["12 months"]
# ) / 3

# calc.loc["rank"] = calc.loc["mean"].rank(ascending=False).astype(int)
# calc.loc["latest nav"] = dfm.iloc[-1]
# calc.loc["12ma NAV"] = dfm.iloc[-12:].mean()
# calc.loc["Buy/Sell"] = np.where(
#     calc.loc["latest nav"] > calc.loc["12ma NAV"], "Buy", "Sell"
# )

# レラティブストレングス
# ((((C - C63) / C63) * .4) + (((C - C126) / C126) * .2)
# + (((C - C189) / C189) * .2) + (((C - C252) / C252) * .2)) * 100
# https://myfrankblog.com/calculating_relative_strength/

# RS = (
#     ((df[asset][-1] - df[asset][-63]) / df[asset][-63] * 0.4)
#     + (((df[asset][-1] - df[asset][-126]) / df[asset][-126]) * 0.2)
#     + (((df[asset][-1] - df[asset][-189]) / df[asset][-189]) * 0.2)
#     + (((df[asset][-1] - df[asset][-252]) / df[asset][-252]) * 0.2)
# )


# st.write(calc)

# # 月次シグナル判定結果を表示
# date = dfm.index.max()
# st.write(str(date.year) + "年" + str(date.month) + "月末のシグナルは以下の通りとなりました。")
# st.write(calc.T.set_index("rank")[["asset class", "Buy/Sell"]].sort_index())
