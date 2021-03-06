import os
# Don't forget to import request, you silly goose
from flask import Flask, render_template, jsonify,request
import sqlalchemy
import random
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, pprint
from flask_cors import CORS
import queue
import threading
import time
import importlib


# def test_func3(string):
#     return "<h1>This is a test 3 {} </h1>".format(string)

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

# When deployed to App Engine, the `GAE_ENV` environment variable will be
# set to `standard`
def get_connection():
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        engine_url = 'mysql+pymysql://{}:{}@/{}?unix_socket={}'.format(
            db_user, db_password, db_name, unix_socket)
        return engine_url
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        engine_url = 'mysql+pymysql://{}:{}@{}/{}'.format(
            db_user, db_password, host, db_name)
        return engine_url

    # The Engine object returned by create_engine() has a QueuePool integrated
    # See https://docs.sqlalchemy.org/en/latest/core/pooling.html for more
    # information


    # engine = sqlalchemy.create_engine(engine_url, pool_size=3)
#
# max_size=10
# master_variable=0
# first_clip=0
# queue_1=queue.Queue(maxsize=10)
# queue_2=queue.Queue(maxsize=10)
#
#
# def test_func():
#     return '<h1>This is a test 1</h1>'
#
def test_queue():
    global queue_1
    # queue_1=queue.Queue(maxsize=0)
    queue_1.put(1)
    queue_1.put(2)
    queue_1.put(3)
    print(queue_1.get())
    queue_1.task_done()
    print(queue_1.get())
    queue_1.task_done()
    print(queue_1.get())
    queue_1.task_done()
    return 'queue done'
#
def test_queue2():
    global queue_2
    queue_2.put(10)
    queue_2.put(20)
    queue_2.put(30)
    print(queue_2.get())
    queue_2.task_done()
    print(queue_2.get())
    queue_2.task_done()
    print(queue_2.get())
    queue_2.task_done()

# # def set_up_queues(x, var):
# #     if var==0:
# #         global first_clip
# #         first_clip=x
# #     else:
# #         queue_1.put(x)
#
#
# def do_stuff(q):
#   while not q.empty():
#     print(q.get())
#     q.task_done()
#
# def thread_test(q, delay):
#     while True:
#         print(q.get())
#         time.sleep(delay)
#         # print("current thread: {}".format(threading.current_thread()))
#         q.task_done()


app = Flask(__name__)
url = get_connection()
app.config['SQLALCHEMY_DATABASE_URI'] = url
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

# def test_func2(string):
#     return '<h1>This is a test {} 2</h1>'.format(string)

class Users(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class UsersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password')

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)

class UserSettings(db.Model):
    __tablename__='user_settings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    bool_setting = db.Column(db.Boolean)
    num_setting = db.Column(db.Integer)
    word_setting = db.Column(db.String)

    def __init__(self, bool_setting, num_setting, word_setting):
        self.bool_setting = bool_setting
        self.num_setting = num_setting
        self.word_setting = word_setting
        self.user_id = 1

class UserSettingSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'bool_setting', 'num_setting', 'word_setting')

user_setting_schema = UserSettingSchema()
user_settings_schema = UserSettingSchema(many=True)

# def test_func4():
#     return '<h1>This is a test 4</h1>'

@app.route('/')
def main():
    return '<h1>HELLO CORS {}</h1>'.format("hello")
@app.route('/loop', methods=['POST'])
def get_loop():
    # data = request.get_json(force=True)
    # word = data['word']
    data = request.get_data()
    print(data)

    return '<h1>LOOPING WORD: {} {}</h1>'.format("testing", data)

@app.route('/test')
def test_route():
    print('LOGGING IN TEST 1')
    test_queue()
    test_queue2()
    return test_func()
#
# @app.route('/test2')
# def test_routeq():
#     q = queue.Queue(maxsize=0)
#     num_threads=300
#
#     for i in range(num_threads):
#         worker = threading.Thread(target=thread_test, args=(q, 2))
#         worker.setDaemon(True)
#         worker.start()
#
#     for y in range (10):
#       for x in range(100):
#         q.put(x + y * 100)
#       q.join()
#       print("Batch {} Done".format(y))
#
#     return '<h1>this was test 2</h1>'
#
# @app.route('/test3/<string>')
# def test_routew(string):
#     test_string = test_func3(string)
#     return test_string
#
# @app.route('/test4')
# def test_routee():
#     q = queue.Queue(maxsize=0)
#
#     for x in range(20):
#       q.put(x)
#
#     do_stuff(q)
#     print('END OF QUEUE?')
#     return test_func4()

@app.route('/users')
def users():
    all_users = Users.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)

@app.route('/settings')
def settings():
    all_settings = UserSettings.query.all()
    result = user_settings_schema.dump(all_settings)
    return jsonify(result.data)

@app.route('/user/<id>', methods=['GET'])
def user_detail(id):
    user = Users.query.get(id)
    return user_schema.jsonify(user)

@app.route('/settings/<id>')
def one_setting(id):
    setting = UserSettings.query.get(id)
    return user_setting_schema.jsonify(setting)

@app.route('/users/<id>/settings', methods=['GET'])
def user_settings(id):
    settings = UserSettings.query.filter_by(user_id=id).first()
    return user_setting_schema.jsonify(settings)

@app.route('/settings', methods=['POST'])
def add_setting():
    data = request.get_json(force=True)
    bool = data['bool']
    num = data['num']
    word = data['word']

    new_setting = UserSettings(bool_setting=bool, num_setting=num, word_setting=word)

    db.session.add(new_setting)
    db.session.commit()

    return user_setting_schema.jsonify(new_setting)

@app.route('/settings/<id>', methods=['PUT'])
def update_settings(id):
    setting = UserSettings.query.get(id)
    new_bool_setting = request.json['bool_setting']
    new_num_setting = request.json['num_setting']
    new_word_setting  = request.json['word_setting']

    setting.bool_setting = new_bool_setting
    setting.num_setting = new_num_setting
    setting.word_setting = new_word_setting

    db.session.commit()
    return user_setting_schema.jsonify(setting)

@app.route('/settings/<id>', methods=['DELETE'])
def delete_settings(id):
    setting = UserSettings.query.get(id)
    db.session.delete(setting)
    db.session.commit()

    return user_setting_schema.jsonify(setting)

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json(force=True)
    username = data['username']
    email = data['email']
    password = data['password']

    new_user = Users(username=username, email=email, password=password)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

# @app.route('/numbers', methods=['POST'])
# def add_number():
#     data = request.get_json(force=True)
#     originalnum = data['original']
#     # modified = data['modified']
#     random = data['random']
#
#     new_number = Numbers(original=originalnum, random=random)
#
#     db.session.add(new_number)
#     db.session.commit()
#
#     return number_schema.jsonify(new_number)
#
# @app.route('/numbers_mod/<id>', methods=['POST'])
# def modify_number(id):
#     number = Numbers.query.get(id)
#     modifiedNum = (number.original * 3)
#     randomNum = float(random.randint(0, 500))
#
#     new_number = Numbers(original=modifiedNum, random=randomNum)
#
#     db.session.add(new_number)
#     db.session.commit()
#
#     return number_schema.jsonify(new_number)
#
# @app.route('/numbers', methods=['GET'])
# def get_numbers():
#     all_numbers = Numbers.query.all()
#     result = numbers_schema.dump(all_numbers)
# #     # return render_template('numbers.html', result=result)
#     return jsonify(result.data)
# #     # return "GET ALL NUMBERS"
#
# @app.route('/numbers/<id>', methods=['GET'])
# def number_detail(id):
#     number = Numbers.query.get(id)
#     return number_schema.jsonify(number)
#
# @app.route('/numbers_last', methods=['GET'])
# def get_last_number():
    # test = Numbers.query.order_by(Numbers.id.desc()).first()
#     result = number_schema.dump(test)
#
#     return jsonify(result.data)
#
# @app.route("/numbers/<id>", methods=["PUT"])
# def number_update(id):
#     number = Numbers.query.get(id)
#     modified = request.json['modified']
#
#     number.modified = modified
#
#     db.session.commit()
#     return number_schema.jsonify(number)
#
# @app.route('/numbers/<id>', methods=['DELETE'])
# def number_delete(id):
#     number = Numbers.query.get(id)
#     db.session.delete(number)
#     db.session.commit()
#
#     return number_schema.jsonify(number)
#
if __name__ == '__main__':
    app.run(debug=True)
