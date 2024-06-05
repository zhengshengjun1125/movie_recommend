"""
作者: 郑声军
日期: 2024-06-06
功能: web页面生成器
"""


def generate(top_recommendations):
    # 创建 HTML 文件的基本结构
    html_content = """
    <!DOCTYPE html>
    <html lang="zh">
    <head>
        <meta charset="UTF-8">
        <title>电影推荐</title>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            h1 {{ color: #333; }}
            .movie-recommendation {{ margin: 20px; }}
            .movie-title {{ font-size: 20px; }}
            .movie-rating {{ font-size: 16px; color: #555; }}
        </style>
    </head>
    <body>
        <h1>为您推荐的电影</h1>

    """

    # 将推荐的电影列表添加到 HTML 内容中
    for index, row in top_recommendations.iterrows():
        html_content += """
        <div class="movie-recommendation">
            <div class="movie-title">{title}</div>
            <div class="movie-rating">预测评分: {rating}</div>
        </div>
        """.format(title=row['title'], rating=row['predicted_rating'])

    # 添加 HTML 文件的结尾
    html_content += """
    </body>
    </html>
    """

    # 将 HTML 内容写入文件
    with open('movie_recommendations.html', 'w', encoding='utf-8') as file:
        file.write(html_content)
    print("电影推荐 HTML 文件已生成。")
