# 数据分析类库
import pandas as pd

#  将数据集拆分为训练集和测试集
from sklearn.model_selection import train_test_split

# 用于回归任务的随机森林模型
from sklearn.ensemble import RandomForestRegressor

# 计算均方误差，用于评估回归模型的性能
from sklearn.metrics import mean_squared_error

# 自定义的数据分析功能
import analyse.analyse as ans

# 数据可视化库
import seaborn as sns
import matplotlib.pyplot as plt

# 引入自己 写的html工具
from src.html import htmlG

# 用户数量封顶
user_count = 6040

"""
作者: 郑声军
日期: 2024-06-05
功能: 数据预处理
"""
# 读取各种数据集
movie = ans.load_data('../DS/movies.csv')
ratings = pd.read_csv('../DS/ratings.csv', sep='::', engine='python', header=None)

ratings.columns = ['userId', 'movieId', 'rating', 'ratingTime']

# 转换数据类型
ratings['userId'] = ratings['userId'].astype(int)
ratings['movieId'] = ratings['movieId'].astype(int)
ratings['rating'] = ratings['rating'].astype(float)
ratings['ratingTime'] = ratings['ratingTime'].astype(int)  # 假设时间戳是整数

# 转换评分时间为日期时间格式
ratings['ratingTime'] = pd.to_datetime(ratings['ratingTime'], unit='s')

# 可视化 - 箱线图观察电影数据特征是否有异常值
sns.boxplot(data=movie)
plt.title('电影箱线图')
plt.show()

# 可视化 - 箱线图观察评分数据特征是否有异常值
for column in ['rating']:
    sns.boxplot(x=ratings[column])
    plt.title(f'评分箱线图')
    plt.show()

# 可视化 - 柱状图了解用户ID和电影ID的分布情况
sns.countplot(x='userId', data=ratings)
plt.title('用户ID 柱状图')
plt.show()

sns.countplot(x='movieId', data=ratings)
plt.title('电影ID 柱状图')
plt.show()

# 可视化 - 直方图了解评分的分布情况
sns.histplot(ratings['rating'], bins=20, kde=True)
plt.title('评分 直方图')
plt.show()

# 检查数据缺失 真正的查看缺失值
miss_movie = ans.check_missing_values(movie).sum()
miss_rating = ans.check_missing_values(ratings).sum()

# 如果有数据缺失 将其删除或者填充
if miss_movie > 0:
    # 这是电影数据 采用填充策略
    movie = ans.handle_missing_values(movie, False)

if miss_rating > 0:
    # 这是评分数据 采用删除策略
    rating = ans.handle_missing_values(ratings, True)

# 到这里数据预处理完毕

"""
作者: 郑声军
日期: 2024-06-06
功能: 数据分析
"""
# 开始进行数据分析 我们根据电影相关分数和和评分平均值作为度量关键 为用户推荐电影
data = pd.merge(ratings, movie, on="movieId")
# 数据分析 - 使用随机森林回归模型预测电影评分
X = data[['userId', 'movieId']]  # 特征
y = data['rating']  # 目标变量

# 拆分数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 创建随机森林回归模型 构建决策树100 随机状态设置42
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# 预测测试集
y_pre = rf.predict(X_test)

# 评估模型
mse = mean_squared_error(y_test, y_pre)

# 因为我们的评分在1-5之内 如果能在2以内的误差 都是能接受的
if mse <= 2:
    # 可视化评分分布
    sns.histplot(data['rating'], kde=True)
    plt.title('评级分布')
    plt.show()

    # 可视化评分与时间的关系
    sns.scatterplot(data=data, x='ratingTime', y='rating')
    plt.title('评分与时间变化')
    plt.show()

    # 可视化用户评分数量
    user_ratings = data.groupby('userId').size()
    sns.barplot(x=user_ratings.index, y=user_ratings.values)
    plt.title('每个用户的评级数')
    plt.show()

    # 可视化电影评分平均值
    movie_ratings_avg = data.groupby('movieId')['rating'].mean()
    sns.barplot(x=movie_ratings_avg.index, y=movie_ratings_avg.values)
    plt.title('平均评分')
    plt.show()

    # 可视化电影评分次数
    movie_ratings_count = data.groupby('movieId')['rating'].count()
    sns.barplot(x=movie_ratings_count.index, y=movie_ratings_count.values)
    plt.title('电影的评分次数')
    plt.show()

    uId = input("输入一个用户id 我们将根据此用户id对它进行电影推荐")
    # 把这个uId 转换为数字
    uId = int(uId)
    if uId < 0 or uId > user_count:
        print('用户id不合法')
    else:
        print(f"开始为用户{uId}推荐电影.....")
        # 步骤1: 找到该用户已经评分的电影
        user_ratings = data[data['userId'] == uId]

        # 步骤2: 使用模型预测该用户对未评分电影的评分
        # 假设 `movies_to_predict` 是用户尚未评分的所有电影的 `movieId` 列表
        movies_to_predict = data[~data['movieId'].isin(user_ratings['movieId'])]['movieId']

        # 创建预测所需的特征
        user_features = pd.DataFrame({'userId': [uId] * len(movies_to_predict), 'movieId': movies_to_predict})

        # 步骤3: 使用模型进行预测
        predicted_ratings = rf.predict(user_features)

        # 将预测结果添加到电影列表中
        movies_to_predict = pd.DataFrame({'movieId': movies_to_predict, 'predicted_rating': predicted_ratings})

        # 步骤4: 将预测结果与电影信息合并，以便获取电影名称和其他信息
        movie_info = pd.read_csv('../DS/movies.csv')
        recommended_movies = pd.merge(movies_to_predict, movie_info, on='movieId')

        # 步骤5: 根据预测的评分对推荐结果进行排序
        recommended_movies = recommended_movies.sort_values(by='predicted_rating', ascending=False)

        # 步骤6: 选择评分最高的几部电影作为推荐
        top_recommendations = recommended_movies.head(5)

        # 打印推荐的电影
        print("推荐的电影:")
        print(top_recommendations[['title', 'predicted_rating']])

        # 将这个数据写成html
        htmlG.generate(top_recommendations)
else:
    print('mse误差过大 请调整数据')
