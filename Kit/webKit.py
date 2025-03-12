from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

def jwt_token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            print("verify_jwt_in_request")
            verify_jwt_in_request()  # 自动从 Header 或 Cookie 验证 Token
            current_user = get_jwt_identity()
            print("current_user", current_user)
            # 其他逻辑...
        except Exception as e:
            return jsonify({'error': 'Invalid token', 'message': str(e)}), 401
        return f(*args, **kwargs)
    return decorated_function