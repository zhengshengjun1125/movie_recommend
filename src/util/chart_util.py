# 数据可视化库
import seaborn as sns
import matplotlib.pyplot as plt


def preview(movie, ratings, chart_folder):
    # 可视化 - 箱线图观察电影数据特征是否有异常值
    sns.boxplot(data=movie)
    plt.title('Box plot')
    plt.savefig(chart_folder + '电影数据特征异常_箱线图.png')

    # 可视化 - 箱线图观察评分数据特征是否有异常值
    for column in ['rating']:
        sns.boxplot(x=ratings[column])
        plt.title(f'Box plot')
        plt.savefig(chart_folder + '评分数据特征异常_箱线图.png')

    # 可视化 - 柱状图了解用户ID和电影ID的分布情况
    sns.countplot(x='userId', data=ratings)
    plt.title('User ID bar chart')
    plt.savefig(chart_folder + '用户ID的分布情况.png')

    sns.countplot(x='movieId', data=ratings)
    plt.title('movie ID bar chart')
    plt.savefig(chart_folder + '电影ID的分布情况.png')

    # 可视化 - 直方图了解评分的分布情况
    sns.histplot(ratings['rating'], bins=20, kde=True)
    plt.title('Score histogram')
    plt.savefig(chart_folder + '评分的分布情况.png')


def after_view(data, chart_folder):
    global user_ratings
    plt.ioff()  # 关闭图像交互
    # 可视化评分分布
    sns.histplot(data['rating'], kde=True)
    plt.title('Rating distribution')
    plt.savefig(chart_folder + '评分分布.png')
    # 可视化评分与时间的关系  类型异常  todo
    sns.scatterplot(data=data, x='ratingTime', y='rating')
    plt.title('Rating and time distribution')
    plt.savefig(chart_folder + '评分与时间的关系.png')
    # 可视化用户评分数量
    user_ratings = data.groupby('userId').size()
    sns.barplot(x=user_ratings.index, y=user_ratings.values)
    plt.title('The number of ratings per user')
    plt.savefig(chart_folder + '用户评分数量.png')
    # 可视化电影评分平均值
    movie_ratings_avg = data.groupby('movieId')['rating'].mean()
    sns.barplot(x=movie_ratings_avg.index, y=movie_ratings_avg.values)
    plt.title('Average rating')
    plt.savefig(chart_folder + '电影评分平均值.png')
    # 可视化电影评分次数
    movie_ratings_count = data.groupby('movieId')['rating'].count()
    sns.barplot(x=movie_ratings_count.index, y=movie_ratings_count.values)
    plt.title('The number of times the movie was rated')
    plt.savefig(chart_folder + '电影评分次数.png')
