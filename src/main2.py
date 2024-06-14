"""
基于用户的协同过滤推荐算法
"""
import os
import random

# 自定义的数据分析功能
import analyse.analyse as ans
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix

# 引入自己 写的html工具
from src.html import htmlG
from src.util import chart_util

# 图表文件夹
chart_folder = 'chart/synergy/'

# 检查img文件夹是否存在，如果不存在则创建
if not os.path.exists(chart_folder):
    os.makedirs(chart_folder)

before_flog = input("是否需要可视化预处理  1 true \n")

before_flog = before_flog == '1'

if before_flog:
    print('开启数据预处理可视化')
else:
    print('跳过数据预处理可视化')

print("开始预处理")

# 读取数据集
movies_df = pd.read_csv('../DS/movies.csv', sep=',', names=['movieId', 'movieName', 'movieType'])
ratings_df = pd.read_csv('../DS/ratings.csv', sep='::', engine='python', header=None)

ratings_df.columns = ['userId', 'movieId', 'rating', 'ratingTime']

# 转换数据类型
ratings_df['userId'] = ratings_df['userId'].astype(int)
ratings_df['movieId'] = ratings_df['movieId'].astype(int)
ratings_df['rating'] = ratings_df['rating'].astype(float)
ratings_df['ratingTime'] = ratings_df['ratingTime'].astype(int)  # 假设时间戳是整数

# 转换评分时间为日期时间格式
ratings_df['ratingTime'] = pd.to_datetime(ratings_df['ratingTime'], unit='s')

# 检查数据缺失 真正的查看缺失值
miss_movie = ans.check_missing_values(movies_df).sum()
miss_rating = ans.check_missing_values(ratings_df).sum()

# 如果有数据缺失 将其删除或者填充
if miss_movie > 0:
    # 这是电影数据 采用填充策略
    movies_df = ans.handle_missing_values(movies_df, False)

if miss_rating > 0:
    # 这是评分数据 采用删除策略
    ratings_df = ans.handle_missing_values(ratings_df, True)

if before_flog:
    chart_util.preview(movies_df.shape[0], ratings_df.shape[0], chart_folder, miss_movie, miss_rating)

print("预处理结束")
"""
开始数据分析
"""

print("开始数据分析")
# 转换数据集，创建用户-电影矩阵
ratings_matrix = ratings_df.pivot_table(index='movieId', columns='userId', values='rating').fillna(0)
ratings_matrix = csr_matrix(ratings_matrix.values)

# 计算用户之间的相似度
user_similarity = cosine_similarity(ratings_matrix)
user_similarity_df = pd.DataFrame(user_similarity, index=ratings_df['movieId'].unique(),
                                  columns=ratings_df['movieId'].unique())

print("数据分析结束")

print("开始推荐")


# 推荐函数
def recommend_movies(user_id, user_similarity_df, movies_df, ratings_df, num_recommendations=5):
    # 获取用户已经评分的电影
    rated_movies = ratings_df[ratings_df['userId'] == user_id]['movieId']

    # 计算用户与其他用户的相似度
    similarities = user_similarity_df[user_id]

    # 排除用户自身
    similarities[user_id] = 0

    # 获取相似度最高的用户
    most_similar_users = similarities.sort_values(ascending=False).index[1:num_recommendations + 1]

    # 推荐电影
    recommended_movies = set()

    for other_user in most_similar_users:
        # 获取其他用户评分的电影
        other_user_ratings = ratings_df[ratings_df['userId'] == other_user]['movieId']
        # 排除用户已经评分的电影
        other_user_ratings = other_user_ratings[~other_user_ratings.isin(rated_movies)]
        # 获取评分最高的电影
        index = ratings_df[ratings_df['userId'] == other_user]['rating'].idxmax()
        # 这个index可能没有出现 判断是否存在
        if index in other_user_ratings.index:
            top_rated_movie = other_user_ratings[index]
            recommended_movies.add(top_rated_movie)

        # 初始化预测评分字典
    predictions = {}
    # 对于每个电影，计算当前用户可能的评分
    for movie_id in movies_df['movieId']:
        # 获取与当前用户相似的用户对这部电影的评分
        similar_users_ratings = ratings_df[(ratings_df['movieId'] == movie_id) &
                                           (ratings_df['userId'].isin(most_similar_users))]
        if not similar_users_ratings.empty:
            # 计算加权和
            weighted_sum = (similar_users_ratings['rating'] * similarities.loc[user_id, most_similar_users]).sum()
            # 计算归一化因子，即相似度之和
            normalization_factor = similarities.loc[user_id, most_similar_users].abs().sum()
            # 计算预测评分
            predictions[movie_id] = weighted_sum / normalization_factor
        else:
            # 如果没有相似用户评分，预测用户评分为高分
            predictions[movie_id] = random.uniform(4.0, 5.0)

    # 将预测评分转换为DataFrame
    predictions_df = pd.DataFrame(list(predictions.items()), columns=['movieId', 'predicted_rating'])
    predictions_df = predictions_df.merge(movies_df, on='movieId')
    # 获取推荐电影的详细信息
    # 假设 movies_df['movieId'] 是字符串类型 类型不同解决
    # 将 recommended_movies 中的元素转换为字符串类型
    recommended_movie_ids = set(str(movie_id) for movie_id in recommended_movies)
    # 使用转换后的集合来筛选电影
    recommended_movies_df = movies_df[movies_df['movieId'].isin(recommended_movie_ids)]
    # 合并数据
    recommended_movies_df = pd.merge(predictions_df, recommended_movies_df)

    return recommended_movies_df


# 输入用户id
recommend_user_id = input("输入推荐用户id")

# 转型
recommend_user_id = int(recommend_user_id)
# 测试推荐系统
recommended_movies_r = recommend_movies(recommend_user_id, user_similarity_df, movies_df, ratings_df)

# 对推荐数据进行html生成
htmlG.generate(recommended_movies_r, before_flog, False)

print("数据推荐结束")
