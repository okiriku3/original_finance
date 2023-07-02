"""st.write('
 米国株
 SPY：S＆P500連動ETF
 QQQ ： NASDAQ100指数連動ETF
 DIA ： ダウ指数連動ETF
 IWM ： 米国の小型株で構成される指数（ラッセル2000）連動ETF
 ARKK ： キャシー・ウッド氏率いるアーク・インベストメント・マネジメントのイノベーションに焦点を当てたETF

 債券
 SHY ： 米国国債 1-3年 ETF
 IEF ： 米国国債 7-10年 ETF
 TLT ： 米国国債 20年超 ETF

 コモディティ
 DBC ： インベスコ DB コモディティ インデックス トラッキング ファンド
 USO ： WTI原油連動ETF
 GLD ： 金地金との連動ETF
 SLV ： 銀ETF

 新興国
 BKF ： BRIC ETF

 通貨
 BTC-USD ： ビットコイン（BTC/USD）
 ETH-USD ： イーサリアム（ETH/USD）
 JPY=X ： 円ドル

 指数
 ^SOX ： SOX指数（フィラデルフィア半導体株指数）
 ^N225 ： 日経225')
 """

import plotly.express as px

import datetime
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
pd.options.display.float_format = '{:.4f}'.format

start_D="2021-12-30"
end_D = datetime.date.today()
codelist = [
    "SPY","QQQ","DIA","IWM","ARKK",
    "SHY","IEF","TLT",
    "DBC","USO","GLD","SLV",
    "BKF",
    "BTC-USD","ETH-USD","JPY=X",
    "^SOX","^N225"]


data2 = yf.download(codelist, start=start_D, end=end_D)["Adj Close"]
st.write(data2)


df_all=(1+data2.pct_change()).cumprod()
st.write(df_all)

import plotly.graph_objects as go
from plotly.subplots import make_subplots

# fig = make_subplots(
#         rows=1,
#         cols=1,)
#         # shared_xaxes=True,
#         # vertical_spacing=0.05,
#         # row_width=[0.2, 0.2, 1.0],
#         # x_title="Date",
#         # specs=[
#         #     [{"secondary_y": True}],
#         #     [{"secondary_y": True}],
#     #     #     [{"secondary_y": False}],
#     #     # ],
#     # )

fig = go.Figure()
for col in df_all.columns:
    # 基本的な線描画
    fig.add_trace(
        go.Scatter(x=df_all.index, y=df_all[col], name= col, mode="lines",
        # row=row,
        # col=1,
    ))


st.plotly_chart(fig)


# df_all.plot(figsize=(8,6),fontsize=18)
# plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=18)  

# plt.grid(True)
# plt.show()

#年
df_Y=data2.groupby([lambda x: x.year]).last()
df_Y_pct=100*df_Y.pct_change()


st.write(df_Y,df_Y_pct.dropna())

#月月

df_M=data2.resample("M").last()
df_M_pct=100*df_M.pct_change()

st.write(df_M,df_M_pct.dropna())


#年
#display(df_Y_pct.dropna().sort_values(by=[2020],ascending=False,axis=1).T)

df_Y_pct =df_Y_pct.dropna().T
st.write("test",df_Y_pct)

fig2 = go.Figure()
for col in df_Y_pct.columns:
    fig2.add_trace(go.Bar(x=df_Y_pct.index,
                        y=df_Y_pct[col],
                        #marker_color='#87cefa',
                        name=col)
    )

fig2.update_traces(width=0.5,
                  hovertemplate='%{x}: %{y:0.1f}%',
                  texttemplate='%{y:0.1f}%',
                  textposition='outside')

fig2.update_layout(title='202X年の月年ごとのリターンの平均',
                  yaxis={'title': 'リターン平均(%)'},
                  legend=dict(orientation='h',
                              xanchor='right',
                              x=1,
                              yanchor='bottom',
                              y=1.05))

st.plotly_chart(fig2)


fig3 = go.Figure()
for col in df_Y_pct.columns:
    fig3.add_trace(go.Bar(y=df_Y_pct.index,
                        x=df_Y_pct[col],
                        #marker_color='#87cefa',
                        name=col)
    )
fig3.update_traces(width=0.25,
                  hovertemplate='%{y}: %{x:0.1f}%',
                  texttemplate='%{x:0.1f}%',
                  textposition='outside',
                  orientation='h')
                
fig3.update_layout(title='202X年8月以降のリターンの平均',
                  xaxis={'title': 'リターン平均(%)'},
                  legend=dict(orientation='h',
                              xanchor='right',
                              x=1,
                              yanchor='bottom',
                              y=1.05),
                  width=800, 
                  height=800,
                  #plot_bgcolor='white'
                  )

st.plotly_chart(fig3)
#fig, ax = plt.subplots()
#ax.bar(df["公園"], df["年齢"])



df_Y_pct.dropna().T.plot.bar(figsize=(15,4),fontsize=18)
plt.legend(loc='center left',bbox_to_anchor=(1, 0.5), fontsize=18)
plt.grid(True)

plt.show()
#st.pyplot(fig)


#月月
df_M_pct=df_M_pct.dropna().T
st.write(df_M_pct)

#########
fig4 = go.Figure()
for col in df_M_pct.columns:
    namename = col.strftime("%Y-%m-%d")
    fig4.add_trace(go.Bar(x=df_M_pct.index,
                        y=df_M_pct[col],name=namename))
                        #marker_color='#87cefa',
    #                     name=col)
    # )

fig4.update_traces(width=0.5,
                  hovertemplate='%{x}: %{y:0.1f}%',
                  texttemplate='%{y:0.1f}%',
                  textposition='outside')

fig4.update_layout(title='202X年の月年ごとのリターンの平均',
                  yaxis={'title': 'リターン平均(%)'},
                  legend=dict(orientation='h',
                              xanchor='right',
                              x=1,
                              yanchor='bottom',
                              y=1.05))

st.plotly_chart(fig4)

############

df_M_pct.dropna().T.plot.bar(figsize=(15,4),fontsize=18)
plt.legend(loc='center left',bbox_to_anchor=(1, 0.5), fontsize=18)
plt.grid(True)

plt.show()



df_D=data2.pct_change()
df_Dex=data2.drop(["BTC-USD","ETH-USD"], axis=1).pct_change()

import seaborn as sns
plt.rc("legend", fontsize=18)
import warnings
warnings.filterwarnings('ignore')

def check(df_check):
    out_analyse=pd.DataFrame(index=df_check.columns)
    out_analyse["return"]=250*df_check.mean()
    out_analyse["volatility"]=16*df_check.std()
    out_analyse["sharpR"]=out_analyse["return"]/out_analyse["volatility"]

    # ボラティリティ、リターン、シャープレシオ　チェック
    plt.style.use('seaborn-dark')
    ax= out_analyse.plot.scatter(x='volatility', y='return', c='sharpR',
                    cmap='RdYlGn', edgecolors='black', figsize=(8, 4), grid=True,sharex=False,s=100)
    for i,(x,y) in enumerate(zip(out_analyse["volatility"],out_analyse["return"])):
        ax.annotate(str(out_analyse.index[i]),(x,y))
    plt.show()

check(df_D)
check(df_Dex)



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
#from pages import commonapp

# from pages import stockMLProphet


