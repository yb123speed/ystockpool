import tushare as ts
import pandas as pd
import datetime as dt

def downloaddata():
    #建立df0用来存储基本面信息df0 = pd.DataFrame()
    pro = ts.pro_api('84a39922917f0ecfee571126d5e27811bd50f5bf2c9590ebb246feaf')

    df0 = pro.stock_basic()
    #将code、name、pb、esp（每股收益）、timeToMarket（上市日期）保存到df0中
    df0 = df0.loc[:,['ts_code','name','list_date']]#, 'pb', 'esp', 'timeToMarket']]
    #将df0按code进行排序
    df0 = df0.sort_index(axis=0, ascending=True)
    df0.to_csv('./stock-pick/stock_basics.csv')

    #建立df1用来存储技术面信息
    df1 = ts.get_today_all()
    #将code、name、changepercent(涨跌幅)、turnoverratio（换手率)保存到df1中
    df1 = df1.loc[:,['code','name', 'changepercent', 'turnoverratio']]
    df1 = df1.set_index('code')
    #将df1按code进行排序
    df1 = df1.sort_index(axis=0, ascending=True)
    df1.to_csv('./stock-pick/today_all.csv')

def stock_picking():
    df0 = pd.read_csv('./stock-pick/stock_basics.csv')
    df1 = pd.read_csv('./stock-pick/today_all.csv')
    
    #将df0和df1横向拼接起来，赋给df
    df = pd.merge(df0,df1, how='inner')
    df.to_csv('./stock-pick/temp.csv');

    # 将每股收益（esp）>1，0<PB<1
    df = df[(df.esp > 1) & (0 < df.pb) & (df.pb < 1)]
    #将 涨跌幅（changepercent)<4% 和 0.8%<换手率(turnoverratio)<3% 的保留下来
    df = df[(df.changepercent<4) & (0.8<df.turnoverratio)&(df.turnoverratio<3)]
    if df.empty:
        print('无符合条件股票！')
    else:
        df = df.sort_values(by='pb', ascending=True)
        df = df.rename(columns={'code':'股票代码', 'name':'股票简称', 'pb':'平均净资产', 'esp':'每股收益', \
                  'timeToMarket':'上市日期', 'changepercent':'涨跌幅', 'turnoverratio':'换手率'})
        df = df.set_index('股票代码')
        #df.to_csv('C:/Users/admin/Desktop/选股.csv')
        date = dt.date.today()
        df.to_excel('./stock-pick/stock-pick-{0}.xlsx'.format(date))

if __name__ == '__main__':
    downloaddata()
    stock_picking()