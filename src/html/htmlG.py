"""
作者: 郑声军
日期: 2024-06-06
功能: web页面生成器
"""

def generate(top_recommendations, before_flag, after_flag):
    # 检查输入数据的正确性
    if not ('movieName' and 'predicted_rating' in top_recommendations.columns):
        raise ValueError("输入的DataFrame缺少必要的列'movieName'或'predicted_rating'")

    # 创建 HTML 文件的基本结构
    html_head = """
    <!DOCTYPE html>
    <html lang="zh">
    <head>
        <meta charset="UTF-8">
        <title>电影推荐</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(to bottom, #f7f7f7, #eaeaea);
            }
            h1 {
                color: #333;
                text-align: center;
                padding: 20px 0;
                transition: color 0.3s ease;
            }
            .movie-recommendation {
                margin: 20px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                transition: box-shadow 0.3s ease;
                border-radius: 5px;
                overflow: hidden;
            }
            .movie-title {
                font-size: 20px;
                font-weight: bold;
                padding: 10px 0;
                background-color: #f7f7f7;
                border-bottom: 1px solid #ddd;
                transition: background-color 0.3s ease, color 0.3s ease;
            }
            .movie-rating {
                font-size: 16px;
                color: #555;
                padding: 10px 0;
                text-align: right;
            }
            .movie-recommendation:hover {
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            .movie-title:hover {
                background-color: #eaeaea;
                color: #333;
            }
        </style>
    </head>
    """

    # HTML 主体内容
    html_body = "<body> <h1>推荐电影列表</h1> "
    for index, row in top_recommendations.iterrows():
        html_body += f"""
        <div class="movie-recommendation">
            <div class="movie-title" style="color:red">电影名称:{row['movieName']}</div>
            <div class="movie-rating">预测评分: {row['predicted_rating']}</div>
        </div>
        """

    if before_flag:
        # 用户ID的分布情况.png
        # 评分数据特征异常 箱线图.png
        # 电影ID的分布情况.png
        # 评分的分布情况.png
        # 电影数据特征异常 箱线图.png
        # 将各种图表写入html中
        html_body += """
        <h1>评分数据缺失扇形图</h1>
        <div class="movie-recommendation">
            <img src="./chart/forest/评分数据缺失扇形图.png" alt="评分数据缺失扇形图">
        </div>
        
        <h1>电影数据缺失扇形图</h1>
        <div class="movie-recommendation">
            <img src="./chart/forest/电影数据缺失扇形图.png" alt="电影数据缺失扇形图">
        </div>
        
       """

    if after_flag:
        # 评分数据特征异常 箱线图.png
        # 电影数据特征异常 箱线图.png
        # 将各种图表写入html中
        html_body += """
        <h1>电影排行榜</h1>
        <div class="movie-recommendation">
            <img src="./chart/forest/电影排行榜.png" alt="电影排行榜">
        </div>
        """
    # HTML 结尾
    html_foot = """
    </body>
    </html>
    """

    # 将 HTML 内容写入文件
    try:
        with open('推荐电影.html', 'w', encoding='utf-8') as file:
            file.write(html_head + html_body + html_foot)
        print("电影推荐 HTML 文件已生成。")
    except Exception as e:
        print(f"无法生成 HTML 文件: {str(e)}")
