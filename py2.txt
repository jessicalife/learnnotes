import pandas as pd

def run(user_input):
    # 读取 Excel 文件
    df = pd.read_excel('QC Part2.xlsx')
    
    # 分割并清理输入的 Audit ID
    input_ids = [str(i).strip() for i in str(user_input).split(',')]
    
    # 筛选数据
    result_df = df[df['ID'].astype(str).isin(input_ids)]
    
    # 如果你只想返回 System 列并去重，可以取消下面这行的注释：
    # result_df = result_df[['System']].drop_duplicates()
    
    return result_df
