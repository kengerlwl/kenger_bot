from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

def jwt_token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 尝试从 Cookies 获取 access_token
        access_token = request.cookies.get('access_token') or request.headers.get('Authorization', '').replace('Bearer ', '')

        if not access_token:
            return jsonify({'error': 'Missing access token'}), 401
        
        # 使用 Flask-JWT-Extended 验证 JWT 的有效性
        try:
            # 设置访问令牌到当前请求
            request._access_token = access_token  # 可以通过这个来传递 token
            verify_jwt_in_request()  # 验证JWT的有效性，确保令牌是有效的
            current_user = get_jwt_identity()  # 获取用户身份信息
            request._current_user = current_user  # 将用户信息存入请求上下文
        except Exception as e:
            return jsonify({'error': 'Invalid or expired token', 'message': str(e)}), 401

        return f(*args, **kwargs)

    return decorated_function