from flask import Flask, jsonify
from flask_cors import CORS
from .routes import api_bp
from .database import get_db

'''初始化Flask应用和数据库，app.py禁止膨胀'''
app = Flask(__name__)

CORS(app)

# 注册蓝图
app.register_blueprint(api_bp, url_prefix='/api')

# 根路径路由
@app.route('/', methods=['GET'])
def index():
    # 动态获取所有API端点
    endpoints = {}
    
    # 遍历所有路由规则
    for rule in app.url_map.iter_rules():
        # 只处理/api开头的路由
        if rule.rule.startswith('/api'):
            # 生成友好的端点名称
            endpoint_name = rule.rule.replace('/api/', '').replace('/', '_').replace('<', '').replace('>', '').replace('int:', '')
            # 确保名称是有效的
            if endpoint_name:
                endpoints[endpoint_name] = rule.rule
    
    return jsonify({
        'message': 'Welcome to DAAT Seeker API',
        'version': '1.0',
        'endpoints': endpoints
    })

# 初始化数据库
db = get_db()
db.init_db()

if __name__ == '__main__':
    app.run(debug=True, port=8086)