# 电影推荐

# 数据集说明
1. movies.csv 电影信息
2. ratings.csv 用户对电影的评分

# 字段说明
~~~
Rating.csv:
用户id
电影id
评分
评分时间

csv数据样式说明
userId:movieId:rating:ratingTime
1::1193::5::978300760
1::661::3::978302109
1::914::3::978301968
1::3408::4::978300275
1::2355::5::978824291
1::1197::3::978302268
1::1287::5::978302039
1::2804::5::978300719
1::594::4::978302268
1::919::4::978301368
1::595::5::978824268
~~~

~~~
movie.csv:
电影id
电影名
电影类型

csv数据样式说明
电影id,电影名,电影类型
1,Toy Story (1995),Animation|Children's|Comedy
2,Jumanji (1995),Adventure|Children's|Fantasy
3,Grumpier Old Men (1995),Comedy|Romance
4,Waiting to Exhale (1995),Comedy|Drama
5,Father of the Bride Part II (1995),Comedy
6,Heat (1995),Action|Crime|Thriller
7,Sabrina (1995),Comedy|Romance
8,Tom and Huck (1995),Adventure|Children's
9,Sudden Death (1995),Action
~~~


# 使用
你需要升级你的pip到24以及上
~~~
下载 pandas
pip install pandas
~~~

~~~
下载 scikit-learn
pip install scikit-learn
~~~

运行src下的main.py