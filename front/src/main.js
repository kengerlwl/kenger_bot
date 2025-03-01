// 获取 DOM 元素
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

// 初始化配置
let config = {};

// 发送消息到 OpenAI API
async function sendMessageToOpenAI(message) {
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${config.OPENAI_API_KEY}`
            },
            body: JSON.stringify({
                model: 'gpt-3.5-turbo',
                messages: [{ role: 'user', content: message }],
                temperature: 0.7,
                max_tokens: 150
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP 错误！状态码: ${response.status}`);
        }

        const data = await response.json();
        if (!data.choices || data.choices.length === 0) {
            throw new Error("API 返回数据格式错误");
        }

        return data.choices[0].message.content;
    } catch (error) {
        console.error('请求失败:', error);
        return '抱歉，我遇到了一些问题，请稍后再试。';
    }
}

// 更新对话历史（支持换行 & Markdown 格式）
function updateChatHistory(userMessage, assistantMessagePlaceholder = '处理中...') {
    const chatContainer = document.createElement('div');
    chatContainer.style.display = 'flex';
    chatContainer.style.flexDirection = 'column';
    chatContainer.style.alignItems = 'flex-start';

    // 用户消息
    const userMsg = document.createElement('div');
    userMsg.textContent = `用户: ${userMessage}`;
    userMsg.style.cssText = "margin:5px 0;padding:8px 12px;background:#ff7e00;border-radius:10px;color:#fff;width:fit-content;";

    // 助手消息（Markdown 解析占位符）
    const assistantMsg = document.createElement('div');
    assistantMsg.innerHTML = `助手: <pre>${assistantMessagePlaceholder}</pre>`;
    assistantMsg.style.cssText = "margin:5px 0;padding:8px 12px;background:#6495ed;border-radius:10px;color:#fff;width:fit-content;white-space:pre-wrap;";

    chatContainer.appendChild(userMsg);
    chatContainer.appendChild(assistantMsg);
    chatMessages.appendChild(chatContainer);

    return assistantMsg; // 返回助手消息元素
}

// 发送按钮点击事件
sendBtn.addEventListener('click', async () => {
    const message = userInput.value.trim();
    if (message === '') return;

    userInput.value = ''; // 清空输入框

    // 先更新 UI，显示用户消息，并获取助手消息元素
    const assistantMsgElement = updateChatHistory(message);

    // 调用 OpenAI API 获取回复
    const assistantMessage = await sendMessageToOpenAI(message);

    // 使用 `marked.js` 解析 Markdown
    assistantMsgElement.innerHTML = `助手: ${marked.parse(assistantMessage)}`;
});

// 从 config.json 加载配置（推荐）
async function loadConfig() {
    try {
        const response = await fetch('src/config.json');
        config = await response.json();
        console.log('配置加载完成:', config);
    } catch (error) {
        console.error('配置加载失败:', error);
    }
}

// 如果使用 config.js，则使用以下方法（取消注释即可）
// function loadConfig() {
//     const script = document.createElement('script');
//     script.src = 'src/config.js';
//     script.onload = () => {
//         config = window.config;
//         console.log('配置加载完成:', config);
//     };
//     script.onerror = () => console.error('配置加载失败');
//     document.body.appendChild(script);
// }

// 初始化
async function init() {
    await loadConfig();
}

init();