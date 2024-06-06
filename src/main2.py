"""
基于用户的协同过滤推荐算法
"""
import os

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix

# 引入自己 写的html工具
from src.html import htmlG

# 图表文件夹
chart_folder = 'chart/synergy/'

# 检查img文件夹是否存在，如果不存在则创建
if not os.path.exists(chart_folder):
    os.makedirs(chart_folder)

# 读取数据集
movies_df = pd.read_csv('../DS/movies.csv', sep=',', names=['movieId', 'title', 'genres'])
ratings_df = pd.read_csv('../DS/ratings.csv', sep='::', engine='python', header=None)

ratings_df.columns = ['userId', 'movieId', 'rating', 'ratingTime']

# 转换数据类型
ratings_df['userId'] = ratings_df['userId'].astype(int)
ratings_df['movieId'] = ratings_df['movieId'].astype(int)
ratings_df['rating'] = ratings_df['rating'].astype(float)
ratings_df['ratingTime'] = ratings_df['ratingTime'].astype(int)  # 假设时间戳是整数

# 转换评分时间为日期时间格式
ratings_df['ratingTime'] = pd.to_datetime(ratings_df['ratingTime'], unit='s')

"""
开始数据分析
"""

# 转换数据集，创建用户-电影矩阵
ratings_matrix = ratings_df.pivot_table(index='userId', columns='movieId', values='rating').fillna(0)
ratings_matrix = csr_matrix(ratings_matrix.values)

# 计算用户之间的相似度
user_similarity = cosine_similarity(ratings_matrix)
user_similarity_df = pd.DataFrame(user_similarity, index=ratings_df['userId'].unique(),
                                  columns=ratings_df['userId'].unique())


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

    # 获取推荐电影的详细信息
    # 假设 movies_df['movieId'] 是字符串类型 类型不同解决
    # 将 recommended_movies 中的元素转换为字符串类型
    recommended_movie_ids = set(str(movie_id) for movie_id in recommended_movies)

    # 使用转换后的集合来筛选电影
    recommended_movies_df = movies_df[movies_df['movieId'].isin(recommended_movie_ids)]

    return recommended_movies_df


# 测试推荐系统
recommended_movies_r = recommend_movies(1, user_similarity_df, movies_df, ratings_df)

# 对推荐数据进行html生成
htmlG.generate(recommended_movies_r, False, False)
