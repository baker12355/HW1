
# You can write code above the if-main block.

if __name__ == '__main__':
    # You should not modify this part.
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--training',
                       default='training_data.csv',
                       help='input training data file name')
    parser.add_argument('--testing',
                        default='testing_data.csv',
                        help='input testing data file name')
    parser.add_argument('--output',
                        default='output.csv',
                        help='output file name')
    args = parser.parse_args()
    
    
    
    import pandas as pd
    
    traning_data = pd.read_csv(args.training, delim_whitespace=False, header=None)
    columns=['open','high','low','close']
    traning_data.columns = columns       #setting columns
    
    close = traning_data['close']
    period=30                          #Average daily line of 30days
    sma= close.rolling(period).mean()
    close.plot(linewidth=1)
    sma.plot()
    
    rising=close>=sma                                   #close > sma ,then market is tending to rising
    falling=close<sma                                   #close < sma ,then market is tending to falling
    
    trend=pd.Series([0]*len(rising),index=rising.index)       
    trend[rising]=1
    trend[falling]=-1                                      
    trend=trend[trend!=0].reindex(trend.index).ffill()  #Trend representing the trend of the market
    
    act=pd.Series([0]*len(trend),index=trend.index)     #act is the action we take next day.

    temp=0
    for i in range(period,len(trend)):
        
        if (temp+trend[i]<=1)&(temp+trend[i]>=-1):
            if (trend[i]==-1):
                act[i]=-1
            else:
                act[i]=1
            temp+=trend[i]
    act.drop([0],inplace=True)
    act.to_csv(args.output, sep=',', encoding='utf-8',index=False)

    
    