# Flask day01
```python
1.Flask 介绍
        Django ：
            优点：大    组件全 session models
            缺点：所有资源全部加载，造成资源上一定的浪费

        Flask ：
            优点：小    短小精悍 session 三方组件多太多了
            缺点：稳定性相对而言较差

        Tornado：
            优点 ：异步 IO 非阻塞 原生Websocket


    2.利用 Django 学习 Flask
        pip install flask

        启动flask：
            from flask import Flask
            app = Flask(__name__)
            app.run()

        flask路由：
            @app.route("/home",methods=["GET","POST"])

        Response三剑客 + 小儿子：
            return "hello s13 students" # Django HttpResponse 返回字符串
            return render_template("index.html") # 返回模板
            return redirect("/index") # 重定向跳转
            小儿子
            return send_file("2.mp3") # 打开文件并返回客户端
            return jsonify({"name":"yinwangba"}) # 返回标准的json格式字符串 content-type: application/json


        Request：
            print(request.form) # form 存放form表单中的序列化数据
            print(request.args) # args 存放URL中的序列化数据
            print(request.values) # values 存放URL和form表单中的序列化数据
            print(request.method) # method 存放请求方式
            print(request.path) # path 路由地址
            print(request.url) # url 请求全部地址 http://127.0.0.1:5000/home?id=jwb&username=ywb
            print(request.host) # host 主机位 127.0.0.1:5000
            print(request.host_url) # host_url 将主机位转成url http://127.0.0.1:5000/
            print(request.data) # data 当请求头content-type无法被识别时
            print(request.json) # json 当请求头content-type：application/json
            print(request.headers) # headers 查看请求头
            print(request.files.get("file")) # files 获取文件对象
            file = request.files.get("file")
            file.save(file.filename)

        Jinja2：
            {{}} 引用变量 非逻辑代码时使用
            {%%} 逻辑代码使用
            | safe
            Markup ： from flask import Markup 后台返回安全标签字符串
            {% block jj2 %}
            {% include "login.html" %}

            {% macro func(name,type_name) %}
                <input type="{{ type_name }}" name="{{ name }}">
                <input type="submit" value="提交文件">
            {% endmacro %}
            {{ func("file","file") }}


        Flask中的Session组件：
            from flask import session
            app.secret_key = "OldBoyEdu.com"
            session被序列化后存放在 浏览器的cookie中


        特殊装饰器：
            @app.template_global()
            def a_and_b(a,b):
                return a+b

            @app.template_filter()
            def abc(a,b,c):
                return a+b+c
```

# Flask 介绍
    Django：
            优点：大、组件全、session、models
            缺点：所有资源全部加载，造成资源上一定的浪费

    Flask：
            优点：小，短小精悍、session，三方组件非常多  flask_*
            缺点： 所有组件都基本来自第三方，组件来自第三方，稳定性相对而言较差一些

    tornado: 龙卷风，
            优点： 异步Io非阻塞，原生websocket ，解决大并发，其它的都需要第三方协助
            缺点： 里面组件太少，第三方组件也太少

# jinja2       ----- 渲染模板
# markupsafe
# werkzeug     ----包含wsgi


默认不支持修改内容自动更新网页内容，需要配置。

1. 启动flask
    ```python
    from flask import Flask

    app = Flask(__name__)

    @app.route('/login')
    def login():
        return 'xxxxxx'

    app.run()
    ```
2. 请求方法
    get、post、put、patch、option、delete、head、trace

    request.values 存放from表单序列化数据和url后的参数
    request.values.to_dict()    转成字典，但如果url里的参数key和form中重名，url会覆盖form


    __name__ 当前文件对象，是为了让解释器知道文件在那里
    避免后台发生直接post标签，需要声明safe，防止xss攻击！！！

    0.9 以前的版本，在模板中应用不存在的变量报错，后面的不报错！！！

    405 访问页面没有权限

    @app.template_global()
    def a_and_b(a,b):
        return a+b

    @app.template_filter()
    def abc(a,b,c):
        return a+b+c