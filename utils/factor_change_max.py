def factor_change_max(stock_data):
    
    '''
    Args :
    stock_data - dataframe containing day level closing price
    '''
    
    #sort dataframe by stock name and date
    st = stock_data.sort_values(['Name','Date'])
    
    #modify dataframe to extract closing price of first and last day from the input
    df1 = pd.DataFrame(st.groupby('Name')['Adj Close'].first()).reset_index().rename(columns = {'Adj Close' : 'Close1'})
    df2 = pd.DataFrame(st.groupby('Name')['Adj Close'].last()).reset_index().rename(columns = {'Adj Close' : 'Close2'})
    
    #merge the above dataframes
    df = df1.merge(df2,on='Name')
    
    #Factor change - current price / starting price 
    df['change_factor'] = df['Close2']/df['Close1']
    
    #sort values by factor change
    df = df.sort_values('chanTctor',ascending=False)
    
    return df
