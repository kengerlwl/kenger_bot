import sys
sys.path.append('.')

import pytest
from  entity.User import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# # 初始化数据库
# db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__)

    # 配置数据库
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://kenger:WKcqDgd8k5WgF2Xp2koj@127.0.0.1:3306/kenger_blog'  # 使用内存数据库进行测试
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True

    # 初始化db
    db.init_app(app)

    return app


from entity.User import User
from service.userService import UserService
from werkzeug.security import check_password_hash


@pytest.fixture(scope='module')
def setup():
    """Set up the test environment and return the app client"""
    # 创建应用并设置为测试环境
    app = create_app('testing')
    client = app.test_client()
    app_context = app.app_context()
    app_context.push()

    # 创建数据库表
    db.create_all()

    # 释放资源
    yield client

    db.session.remove()
    db.drop_all()
    app_context.pop()


def test_register_user(setup):
    """Test user registration"""
    username = 'testuser'
    password = 'testpassword'

    success, message = UserService.register_user(username, password)
    assert success
    assert message == "User registered successfully"

    # 检查数据库中是否有用户
    user = User.query.filter_by(username=username).first()
    assert user is not None
    assert user.username == username
    assert check_password_hash(user.password, password)


def test_register_existing_user(setup):
    """Test registering an existing user"""
    username = 'testuser'
    password = 'testpassword'

    # 先注册用户
    UserService.register_user(username, password)

    # 再尝试注册同一个用户名
    success, message = UserService.register_user(username, password)
    assert not success
    assert message == "Username already exists"


def test_authenticate_user_success(setup):
    """Test user authentication with correct credentials"""
    username = '1'
    password = '1'

    # 注册用户
    UserService.register_user(username, password)

    # 尝试认证
    success, user = UserService.authenticate_user(username, password)
    assert success
    assert user == username


def test_authenticate_user_invalid_credentials(setup):
    """Test user authentication with incorrect credentials"""
    username = 'testuser'
    password = 'testpassword'

    # 注册用户
    UserService.register_user(username, password)

    # 尝试使用错误的密码认证
    success, message = UserService.authenticate_user(username, 'wrongpassword')
    assert not success
    assert message == "Invalid credentials"


def test_authenticate_user_non_existent(setup):
    """Test user authentication with non-existent user"""
    username = 'nonexistentuser'
    password = 'testpassword'

    success, message = UserService.authenticate_user(username, password)
    assert not success
    assert message == "Invalid credentials"