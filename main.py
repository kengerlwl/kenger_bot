from flask import Flask, render_template, request, jsonify, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from LLM import rag_chain  # 导入后端逻辑
from flask_cors import CORS
import datetime
from Config import Config
from Kit.webKit import jwt_token_required
from Kit import *
from ai_detect import openai_client
# from entity.User import db

app = Flask(__name__, template_folder="/home/kenger/kenger_aibot/ai_front/dist", static_folder="/home/kenger/kenger_aibot/ai_front/dist/assets")
# app.config.from_object(Config)
# Initialize the app with the db instance
# db.init_app(app)

CORS(app, resources={r"/chat": {"origins": "*"}})  # 允许所有来源访问 /chat 路由




# 配置 Flask-JWT-Extended
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # 更改为强随机密钥，用来加密和解密JWT（JSON Web Token）的密钥。
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=1)  # 设置令牌过期时间
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']  # 允许从请求头和 Cookie 获取 Token
app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'  # 指定 Cookie 名称
app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # 如果不需要 CSRF 保护，可以关闭
jwt = JWTManager(app)
from service.userService import UserService
# 用户数据库模拟（可以替换成数据库存储）
users_db = {}

@app.route('/')
def index():
    return render_template('index.html')

# 注册接口
@app.route('/kenger/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')
    
    

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    if username in users_db:
        return jsonify({'error': 'User already exists'}), 400

    # 存储哈希密码
    # hash_pw = generate_password_hash(password)
    rsp , info = UserService.register_user(username, password)
    if not rsp:
        return jsonify({'error': info}), 400
    # users_db[username] = generate_password_hash(password)

    return jsonify({'message': 'User registered successfully'}), 201

# 登录接口
@app.route('/kenger/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')
    # return jsonify({'message': 'Login successful'}), 200

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    rsp, info  = UserService.authenticate_user(username, password)

    # rsp, info = UserService.authenticate_user(username, password)
    if not rsp:
        return jsonify({'error': info}), 401

    # 创建JWT
    access_token = create_access_token(identity=username)
    
    # 设置JWT到Cookie中
    response = make_response(jsonify({'message': 'Login successful'}))
    response.set_cookie('access_token', access_token, httponly=True, max_age=app.config['JWT_ACCESS_TOKEN_EXPIRES'])
    
    return response

# 受保护的聊天接口，要求用户登录后访问
@app.route('/v1/chat/completions', methods=['POST'])
@jwt_token_required
def chat():
    # 获取当前用户的身份信息
    current_user = get_jwt_identity()


    
    # 确保请求是 JSON 格式
    if not request.is_json:
        return jsonify({'error': 'Unsupported Media Type'}), 415
    
    try:
        data = request.get_json()
        messages = data.get('messages', [])
        
        if not messages:
            return jsonify({'error': 'No messages provided'}), 400
        print("messages:", messages)
        
        # 获取用户的问题
        user_question = messages[0].get('content')
        print("*" * 30)
        print(user_question)
        
        if not user_question:
            return jsonify({'error': 'No user question provided'}), 400
        
        # 获取模型参数
        model = data.get('model', 'gpt-3.5-turbo')
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens', 150)

        # 调用 rag_chain
        answer = rag_chain.invoke(user_question)
        
        # 构造兼容 OpenAI API 的响应
        response = {
            "choices": [{
                "message": {
                    "content": answer
                }
            }]
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=10)  # 设置最大线程数


@app.route('/kenger/ai_prob', methods=['POST'])
def ai_prob():
    data = request.get_json()
    texts = data.get('text', '')
    print("texts:", texts)
    logger.info(f"AI检测文本：{texts}")
    
    rsp = openai_client.cal_ai_prob(texts=texts)
    return jsonify(rsp)

    # if not texts:
    #     return jsonify({'error': 'Text input is required'}), 400

    # texts = texts.split('\n')

    # def process_text(text):
    #     return openai_client.cal_ai_prob(text)

    # # 每次请求新建一个 ThreadPoolExecutor，避免被 Flask 回收
    # with ThreadPoolExecutor(max_workers=10) as executor:
    #     results = list(executor.map(process_text, filter(None, texts)))

    # logger.info(f"AI检测结果：{results}")
    # return jsonify(results)

@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    print("after request")
    return response

if __name__ == '__main__':
    app.run(debug=True)