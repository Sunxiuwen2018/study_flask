#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from flask import Flask
from flask import request
from flask import session
from flask import render_template, redirect
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.websocket import WebSocket  # 语法提示

from utils.app_dbutils import POOL  # 导入自制dbutil组件提供的线程级别的连接池


app = Flask(__name__)
app.secret_key = "welcome to my site"

# 将所有的socket连接放到列表中
user_socket_list = [
    # 'webSocket_obj'
]

# 单聊需要保存用户标识
user_socket_dict = {
    # 'nick_name': 'webSocket_obj'
}


@app.route('/ql')
def ws():
    """群聊"""
    # print(request.environ)
    user_socket = request.environ.get("wsgi.websocket", '')  # type:WebSocket
    user_socket_list.append(user_socket)
    print(len(user_socket_list), user_socket_list)

    while 1:
        try:
            msg = user_socket.receive()  # 接收消息
            print(msg, type(msg))
            msg = json.loads(msg)

            for uscoket in user_socket_list:
                if uscoket != user_socket:  # 除开自己发给其他人
                    uscoket.send(json.dumps({'msg': msg.get('msg')}))  # 发送消息给所有人
        except:
            user_socket_list.remove(user_socket)  # 如果


@app.route('/single_ws')
def single_ws():
    print(request.environ)
    user_socket = request.environ.get("wsgi.websocket", '')
    username = session.get('user_name')  # 用户名
    print(username)
    if username not in user_socket_dict and username:
        user_socket_dict[username] = user_socket
    while 1:
        try:
            msg = user_socket.receive()  # socket获取数据
            msg = json.loads(msg)
            to_friends = msg.get('to_friend')  # 是一个列表，一个或多个朋友的用户名
            print(to_friends)
            msg = msg.get('msg')  # 要发的信息
            send_msgs = f'来自{username}:{msg}'
            print(send_msgs)
            for i in to_friends:
                print(i)
                # 从socket连接表中获取朋友的socket连接
                print(user_socket_dict)
                friend_socket = user_socket_dict[i]  # type:WebSocket
                friend_socket.send(send_msgs)
        except:
            user_socket_dict.pop(username)


@app.route('/single')
def single_chat():
    """单聊页面"""
    return render_template('chat_single.html')


@app.route('/chat')
def chats():
    """群聊页面"""
    return render_template('chat_mutil.html')


@app.route('/login', methods=['get', 'post'])
def login():
    msg = ""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = POOL.connection()
        cursor = conn.cursor()
        sql = 'select name from userinfo where name ="%s"and password="%s"' % (username, password)
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        conn.close()
        if res:
            session['user_name'] = username
            session['is_login'] = True
            return redirect('/single')
        else:
            msg = "用户名米亚错误"
    return render_template('login.html', msg_dic={'msg': msg})


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        print(username, password)
        try:
            if username and password:
                # 写入数据库
                conn = POOL.connection()
                cursor = conn.cursor()
                sql = 'insert into userinfo (name,password) values ("%s","%s")' % (username, password)
                cursor.execute(sql)
                conn.commit()
                cursor.close()
                conn.close()
                return redirect('/login')
            else:
                msg = "注册不合格"
        except:
            msg = "注册不合格"
    return render_template('register.html', msg_dic={"msg": msg})


@app.route('/add_friends')
def add_friends():
    """加好友"""
    pass


@app.route('/friends')
def friends():
    """加载聊天页面时，通过ajax访问此接口提供该用户的朋友列表
    朋友表，一个用户有多个朋友
    uid  friendid
    1      2
    1      3
    1      6
    2      1
    """
    pass


if __name__ == '__main__':
    # 表示如果是http请求就直接app处理，如果是websocket就交给handler再给app
    http_serv = WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    http_serv.serve_forever()
