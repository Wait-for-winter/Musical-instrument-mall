from flask import Flask, request, jsonify
from flask.views import MethodView
import pymysql
from sqlalchemy.testing.suite.test_reflection import users

app = Flask(__name__)
userID=None
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
        id=data.get('id')
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
                sql = "SELECT * FROM user WHERE id=%s"
                cursor.execute(sql, (id))
                result = cursor.fetchone()

                if result:
                    # 如果用户已存在，返回状态 0
                    return jsonify({'status': 0}), 200
                else:
                    # 如果用户不存在，将新用户插入数据库
                    sql = "INSERT INTO user (id,password) VALUES (%s,%s)"
                    cursor.execute(sql, (id, password))
                    connection.commit()
                    # 返回状态 1 表示注册成功
                    return jsonify({'status': 1}), 201
        except Exception as e:
            print(f"数据库出问题惹 : {e}")
            return jsonify({'error': '数据库出问题惹'}), 500
        finally:
            connection.close()

        # 如果用户名或密码缺失，返回错误
        return jsonify({'error': 'Invalid data'}), 400

class LoginAPI(MethodView):
    def post(self):
        # 从请求中获取 JSON 数据
        data = request.get_json()
        id = data.get('id')
        global userID
        userID = id #保存登录状态
        password = data.get('password')

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
                # 检查用户名和密码是否匹配
                sql = "SELECT * FROM user WHERE id=%s AND password=%s"
                cursor.execute(sql, (id, password))
                result = cursor.fetchone()

                if result:
                    print("登上去惹")
                    # 如果凭据正确，返回状态 1 表示登录成功
                    return jsonify({'status': 1}), 200
                else:
                    print("登不上诶")
                    # 如果凭据不正确，返回状态 0 表示登录失败
                    return jsonify({'status': 0}), 401
        except Exception as e:
            print(f"数据库出问题惹 : {e}")
            return jsonify({'error': '数据库出问题惹'}), 500
        finally:
            connection.close()

        # 如果用户名或密码缺失，返回错误
        return jsonify({'error': 'Invalid data'}), 400


class AddToCartAPI(MethodView):
    def post(self):
        # 从请求中获取 JSON 数据
        data = request.get_json()
        userid = userID
        productid = data.get('Pro_id')
        quantity = int(data.get('num'))
        typeid=data.get('detail_id')

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
                # 检查是否已经存在该用户和商品的记录
                sql_check = "SELECT * FROM cart WHERE userid=%s AND typeid=%s"
                cursor.execute(sql_check, (userid, typeid))
                result = cursor.fetchone()

                if result:
                    # 更新数量
                    new_quantity = int(result['quantity']) + quantity
                    sql_update = "UPDATE cart SET quantity=%s WHERE typeid=%s AND typeid=%s"
                    cursor.execute(sql_update, (new_quantity, typeid, typeid))
                else:
                    # 插入新记录
                    sql_insert = "INSERT INTO cart (userid, typeid, quantity) VALUES (%s, %s, %s)"
                    cursor.execute(sql_insert, (userid, typeid, quantity))

                connection.commit()
                print("加进去惹")
                return jsonify({'status': 1,'message': '加进去惹'}), 200
        except Exception as e:
            print(f"数据库出问题惹 : {e}")
            return jsonify({'status': 0,'error': '数据库出问题惹'}), 500
        finally:
            connection.close()

        # 如果缺少必要的参数，返回错误
        return jsonify({'status': 0,'error': 'Invalid data'}), 400



class ProductDetailsAPI(MethodView):
    def get(self):
        # 从请求中获取查询参数
        pro_id = request.args.get('Pro_id')

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
                # 查询产品详细信息
                sql_product = "SELECT * FROM product WHERE productID=%s"
                cursor.execute(sql_product, (pro_id,))
                product_info = cursor.fetchone()

                if not product_info:
                    print("找不到产品信息")
                    return jsonify({'error': '找不到产品信息'}), 404

                # 查询类型ID列表
                sql_type_ids = "SELECT type_id FROM product_types WHERE productID=%s"
                cursor.execute(sql_type_ids, (pro_id,))
                type_ids = [row['type_id'] for row in cursor.fetchall()]

                # 构造返回结果
                result = [
                    {
                        'Pro_name': product_info['Pro_name'],
                        'Pro_price': product_info['Pro_price'],
                        'Pro_id': product_info['Pro_id'],
                        'store_name': product_info['store_name'],
                        'store_id': product_info['store_id']
                    },
                    type_ids
                ]

                print("查询成功")
                return jsonify(result), 200
        except Exception as e:
            print(f"数据库出问题惹 : {e}")
            return jsonify({'error': '数据库出问题惹'}), 500
        finally:
            connection.close()

        # 如果缺少必要的参数，返回错误
        return jsonify({'error': 'Invalid data'}), 400

# 添加产品详情接口
product_details_view = ProductDetailsAPI.as_view('product_details_api')
app.add_url_rule('/product', view_func=product_details_view, methods=['GET'])

# 添加购物车接口
add_to_cart_view = AddToCartAPI.as_view('add_to_cart_api')
app.add_url_rule('/cart/add', view_func=add_to_cart_view, methods=['POST'])

# 登录
login_view = LoginAPI.as_view('login_api')
app.add_url_rule('/login', view_func=login_view, methods=['POST'])
# 注册
register_view = RegisterAPI.as_view('register_api')
app.add_url_rule('/register', view_func=register_view, methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True)