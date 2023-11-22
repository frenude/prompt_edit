import os

from openpyxl.workbook import Workbook

from src.portrait.gen_data import get_data
from src.portrait.mark import mark
from src.portrait.portrait import get_user
import json

import pandas as pd


def append_to_excel(data, file_name, sheet_name='Sheet1'):
    # 将数据转换为DataFrame
    df = pd.DataFrame([data])

    # 如果文件不存在，直接写入数据
    if not os.path.exists(file_name):
        df.to_excel(file_name, sheet_name=sheet_name, index=False)
    else:
        # 读取原始文件
        try:
            old_df = pd.read_excel(file_name, sheet_name=sheet_name)
        except FileNotFoundError:
            # 如果指定的工作表不存在，则创建一个新的DataFrame
            old_df = pd.DataFrame()

        # 使用 concat 追加数据
        updated_df = pd.concat([old_df, df], ignore_index=True)

        # 写入更新后的数据
        updated_df.to_excel(file_name, sheet_name=sheet_name, index=False)

def pipline(file_name):
    ori = json.loads(get_data())
    content = ori.get('content')
    portrait = json.loads(get_user(content))
    data = mark(ori, portrait)
    print(data)
    append_to_excel(data, file_name)


from src.portrait.color import mark_rows_below_threshold

if __name__ == '__main__':
    file = '1122-1.xlsx'
    for i in range(200):
        pipline(file)
    mark_rows_below_threshold(file)
