import pandas as pd


"""
作者: 郑声军
日期: 2024-06-05
功能: 基础功能封装
"""


# 加载数据
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df


# 合并数据集 参数为数据数组
def merge_data(data_list):
    df = pd.concat(data_list, ignore_index=True)
    return df


# 检查是否含有缺失值 返回缺失数量
def check_missing_values(df):
    missing_values = df.isnull().sum()
    return missing_values


# 缺失值处理 参数为布尔值 true为删除 false为填补
def handle_missing_values(df, drop=False):
    if drop:
        df.dropna(inplace=True)
    else:
        df.fillna(0, inplace=True)
    return df


# 数据统计
def data_statistics(df):
    statistics = df.describe()
    return statistics


# 剔除重复项
def remove_duplicates(df):
    df.drop_duplicates(inplace=True)
    return df

