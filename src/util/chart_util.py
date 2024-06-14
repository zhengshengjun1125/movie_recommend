# 数据可视化库
import seaborn as sns
import matplotlib.pyplot as plt

# 设置matplotlib的字体，以支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

plt.figure(figsize=(10, 8))  # 宽度为10英寸，高度为8英寸


def preview(movie_total, ratings_total, chart_folder, movie_lose, ratings_lose):
    # 对plt进行状态清空
    plt.clf()
    # 电影数据缺失扇形图
    labels = ['正常的数据量', '丢失的数据量']
    sizes = [movie_total - movie_lose, movie_lose]
    colors = ['lightgreen', 'red']  # 红色代表缺失量  绿色代表正常的
    explode = (0.1, 0)  # 突出显示缺失数据部分
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    # 确保饼图是圆形的
    plt.axis('equal')
    plt.title('电影数据缺失扇形图')
    plt.savefig(chart_folder + '电影数据缺失扇形图.png')

    # 评分数据缺失扇形图 红色代表缺失量  绿色代表正常的
    sizes = [ratings_total - ratings_lose, ratings_lose]
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    # 确保饼图是圆形的
    plt.axis('equal')
    plt.title('评分数据缺失扇形图')
    plt.savefig(chart_folder + '评分数据缺失扇形图.png')


def after_view(data, chart_folder):
    # 对plt进行状态清空
    plt.clf()
    # 假设df是你的DataFrame
    movie_avg_ratings = data.groupby('movieName')['rating'].mean().sort_values(ascending=False)
    top_movies = movie_avg_ratings.head(20)
    # 绘制条形图
    top_movies.plot(kind='barh', color='skyblue')
    plt.title('电影排行榜')
    plt.xlabel('平均评分')
    plt.ylabel('电影名称')
    # 显示X轴的标签
    plt.xticks(rotation=45, ha='right')  # 旋转标签以便阅读
    # 显示图表
    plt.tight_layout()  # 调整布局以适应标签
    plt.savefig(chart_folder + '电影排行榜.png')
