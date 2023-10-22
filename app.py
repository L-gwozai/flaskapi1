from flask import Flask, request, jsonify
import random
import string
from tools import send_markdown_email
import os
app = Flask(__name__)

# 存储生成的随机token和关联的数据
webhook_tokens = {}

def generate_token():
    # 生成一个随机的16字符令牌
    token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
    return token

@app.route('/generate_webhook', methods=['POST'])
def generate_webhook():
    # 生成一个随机token
    token = generate_token()
    # 存储关联的数据
    data = request.json
    webhook_tokens[token] = data
    return jsonify({'webhook_url': f'/webhook/{token}'})

@app.route('/webhook/<token>', methods=['POST'])
def webhook(token):
    if token in webhook_tokens:
        data = webhook_tokens[token]
        received_data = request.json
        receiver_email = data["receiver_email"]
        markdown_text = data["markdown_text"]
        subject = data["subject"]
        if receiver_email != "":
            send_markdown_email(receiver_email, markdown_text, choice=1, subject=subject)
            # 在这里执行与参数相关的操作
            # print(f'Received webhook data for token {token}: {received_data}')
            return f"已发送 {markdown_text} 到邮箱 {receiver_email}"
        else:
            return '接收邮箱为空', 403
    else:
        return '密钥错误', 403

# if __name__ == '__main__':
#     app.run(debug=True)
if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000), host='0.0.0.0')