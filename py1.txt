import pandas as pd

def run(user_input):
    # 读取 Excel 文件
    df = pd.read_excel('QC Part2.xlsx')
    
    # 将用户输入的字符串按逗号分割，并去除每个 ID 两边的空格
    # 例如: " 101, 102 " 会变成 ['101', '102']
    input_ids = [str(i).strip() for i in str(user_input).split(',')]
    
    # 确保 DataFrame 的 ID 列也是字符串，然后使用 isin() 筛选包含在列表中的行
    result_df = df[df['ID'].astype(str).isin(input_ids)]
    
    return result_df
