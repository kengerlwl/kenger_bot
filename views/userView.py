from flask import render_template, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from views.userView import db, User

# 注册接口
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    # 检查用户是否已存在
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'error': 'User already exists'}), 400

    # 存储哈希密码
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

# 登录接口
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # 获取用户并验证密码
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid username or password'}), 401

    # 创建JWT
    access_token = create_access_token(identity=username)
    
    # 设置JWT到Cookie中
    response = make_response(jsonify({'message': 'Login successful'}))
    response.set_cookie('access_token', access_token, httponly=True, max_age=app.config['JWT_ACCESS_TOKEN_EXPIRES'])
    
    return response