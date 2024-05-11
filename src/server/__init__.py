from flask import Flask, render_template, redirect
from werkzeug.routing import BaseConverter

from module.interface.manager import manager

from ws import WSServer
ws_server = WSServer()

# 这部分需要首先进行加载
manager.load_modules()
manager.set_log_callback(lambda log: ws_server.send(log.to_json()))

from api import API_LIST
from api.result import ResultResponse

# 0. 创建对象
folder = '../../static'
app = Flask(__name__, static_url_path="", 
    static_folder=folder, template_folder=folder)

# 1. 设置正则转换器
# https://blog.csdn.net/rytyy/article/details/78939507
class RegexConverter(BaseConverter):
    def __init__(self,url_map,*items):
        super(RegexConverter,self).__init__(url_map)
        self.regex=items[0]

app.url_map.converters['regex'] = RegexConverter

# 2. 注册 API
for api in API_LIST:
    app.register_blueprint(api)

# 3. 自定义返回类型
app.response_class = ResultResponse


''' --- webui 路由设置 --- '''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/<path:name>', methods=["GET", "PUT", "POST"])
def api(name: str):
    # 设置 307，在重定向后会保留请求方法
    return redirect("/" + name, 307)