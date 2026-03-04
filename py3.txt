import pandas as pd

def run(user_input):
    # 读取 Network Table
    df = pd.read_excel('Network Table.xlsx')
    
    # 分割并清理输入的 AE
    input_aes = [str(a).strip() for a in str(user_input).split(',')]
    
    # 筛选包含在输入列表中的 AE
    result_df = df[df['AE'].astype(str).isin(input_aes)]
    
    return result_df
