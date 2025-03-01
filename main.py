from flask import Flask, render_template, request, jsonify
from LLM import rag_chain  # 导入后端逻辑
from flask_cors import CORS


app = Flask(__name__, template_folder="front", static_folder="front/src")
CORS(app, resources={r"/chat": {"origins": "*"}})  # 允许所有来源访问 /chat 路由

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/chat', methods=['POST'])
def chat():
    # 获取请求头中的 Authorization
    api_key = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not api_key:
        return jsonify({'error': 'Missing API Key'}), 401
    
    # 确保请求是 JSON 格式
    if not request.is_json:
        return jsonify({'error': 'Unsupported Media Type'}), 415
    
    try:
        data = request.get_json()
        messages = data.get('messages', [])
        
        if not messages:
            return jsonify({'error': 'No messages provided'}), 400
        
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

@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    print("after request")
    return response

if __name__ == '__main__':
    app.run(debug=True)