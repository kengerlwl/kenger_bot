from flask import Flask, render_template, request, jsonify
from LLM import rag_chain  # 导入后端逻辑

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    question = request.form.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    try:
        answer = rag_chain.invoke(question)
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)