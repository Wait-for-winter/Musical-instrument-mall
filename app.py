from flask import Flask, request, jsonify
from flask.views import MethodView
import pymysql
app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  # 允许所有来源的跨域请求
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
    return response

class RegisterAPI(MethodView):
    def post(self):
        # 从请求中获取 JSON 数据
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        phone = data.get('phone')
        print(f" 用户名: {username}")

        # 连接到 MySQL 数据库
        try:
            connection = pymysql.connect(
                host='localhost',  # 数据库地址
                user='root',  # 数据库用户名
                password='root',  # 数据库密码
                db='database',  # 数据库名称
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            print("数据库连接成功")
        except Exception as e:
            print(f"草了没连上: {e}")
            return jsonify({'error': '草了没连上'}), 500

        try:
            with connection.cursor() as cursor:
                # 检查用户名是否已存在
                sql = "SELECT * FROM user WHERE phone=%s"
                cursor.execute(sql, (phone,))
                result = cursor.fetchone()

                if result:
                    # 如果用户已存在，返回状态 0
                    return jsonify({'status': 0}), 200
                else:
                    # 如果用户不存在，将新用户插入数据库
                    sql = "INSERT INTO user (username, password,phone) VALUES (%s, %s,%s)"
                    cursor.execute(sql, (username, password,phone))
                    connection.commit()
                    # 返回状态 1 表示注册成功
                    return jsonify({'status': 1}), 201
        except Exception as e:
            print(f"Database error: {e}")
            return jsonify({'error': 'Database error'}), 500
        finally:
            connection.close()

        # 如果用户名或密码缺失，返回错误
        return jsonify({'error': 'Invalid data'}), 400

register_view = RegisterAPI.as_view('register_api')
app.add_url_rule('/register', view_func=register_view, methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True)