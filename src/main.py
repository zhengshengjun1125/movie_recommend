"""
随机森林模型
"""
# 引入系统库
import os

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

# 引入图形工具
from src.util import chart_util

# 引入自己 写的html工具
from src.html import htmlG

# 用户数量封顶
user_count = 6040

# 图表文件夹
chart_folder = 'chart/forest/'

# 检查img文件夹是否存在，如果不存在则创建
if not os.path.exists(chart_folder):
    os.makedirs(chart_folder)

before_flog = input("是否需要可视化预处理  1 true \n")
after_flag = input("是否需要可视化数据分析  1 true")

before_flog = before_flog == '1'
after_flag = after_flag == '1'

if before_flog:
    print('开启数据预处理可视化')
else:
    print('跳过数据预处理可视化')

if after_flag:
    print('开启数据分析可视化')
else:
    print('跳过数据分析可视化')

print("开始数据预处理")
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
ratings['ratingTime'] = ratings['ratingTime'].astype(int)  # 时间戳是整数

# 转换评分时间为日期时间格式
ratings['ratingTime'] = pd.to_datetime(ratings['ratingTime'], unit='s')
ratings['ratingTime'] = str(ratings['ratingTime'])

# 检查数据缺失 真正的查看缺失值
miss_movie = ans.check_missing_values(movie).sum()
miss_rating = ans.check_missing_values(ratings).sum()

# 需要预处理图表
if before_flog:
    chart_util.preview(movie.shape[0], ratings.shape[0], chart_folder, miss_movie, miss_rating)

# 如果有数据缺失 将其删除或者填充
if miss_movie > 0:
    # 这是电影数据 采用填充策略
    movie = ans.handle_missing_values(movie, False)

if miss_rating > 0:
    # 这是评分数据 采用删除策略
    rating = ans.handle_missing_values(ratings, True)

# 将数据合并
data = pd.merge(ratings, movie, on="movieId")

# 过滤重复项
data = ans.remove_duplicates(data)

# 到这里数据预处理完毕
print("数据预处理完毕")
"""
作者: 郑声军
日期: 2024-06-06
功能: 数据分析
"""
print("开始数据分析")
# 数据分析 - 使用随机森林回归模型预测电影评分
X = data[['userId', 'movieId']]  # 特征
y = data['rating']  # 目标变量

# 拆分数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 创建随机森林回归模型 构建决策树50 最大深度10 平方差算法  随机状态设置42
rf = RandomForestRegressor(n_estimators=50, max_depth=10, max_features='sqrt', n_jobs=-1, random_state=42)

# 开始训练  如果决策树数量过多 会导致程序运行过慢
rf.fit(X_train, y_train)

# 预测测试集
y_pre = rf.predict(X_test)

# 评估模型
mse = mean_squared_error(y_test, y_pre)

print("数据分析完毕")
print("开始生成推荐数据")
"""
作者: 郑声军
日期: 2024-06-06
功能: 推荐电影
"""
# 因为我们的评分在1-5之内 如果能在2以内的误差 都是能接受的
if mse <= 2:
    if after_flag:
        chart_util.after_view(data, chart_folder)

    uId = input("输入一个用户id 我们将根据此用户id对它进行电影推荐")
    # 把这个uId 转换为数字
    try:
        uId = int(uId)
    except:
        print('输入必须为数字')
        exit()

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

        # 步骤7: 对电影数据进行去重 如果不去重 将会推荐重复数据
        recommended_movies.drop_duplicates(inplace=True)

        # 步骤8: 选择评分最高的几部电影作为推荐
        top_recommendations = recommended_movies.head(5)

        """
        作者: 郑声军
        日期: 2024-06-06
        功能: 数据可视化
        """
        # 将这个数据写成html
        htmlG.generate(top_recommendations, before_flog, after_flag)
else:
    print('mse误差过大 请调整数据')
print("生成推荐数据结束")
