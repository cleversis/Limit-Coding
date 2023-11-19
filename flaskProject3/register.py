import mysql.connector

# 连接到 MySQL 数据库
cnx = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="your_database"
)

# 创建用户表的 SQL 语句
create_table_query = """
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
)
"""

# 插入用户数据的 SQL 语句
insert_user_query = """
INSERT INTO users (username, password)
VALUES (%s, %s)
"""

# 执行创建表的 SQL 语句
cursor = cnx.cursor()
cursor.execute(create_table_query)

# 示例：插入一个用户
username = "user1"
password = "password123"

# 执行插入数据的 SQL 语句
cursor.execute(insert_user_query, (username, password))

# 提交事务
cnx.commit()

# 关闭连接
cursor.close()
cnx.close()
