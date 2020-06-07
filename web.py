#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
NUAA_iCal_Web Backend
based on Flask

@Author: MiaoTony
@CreateTime: 20191215
@UpdateTime: 20200213

"""
from flask import Flask, render_template, request, jsonify, url_for, \
    make_response, send_file, redirect, send_file
from flask import session as s
import requests

from getClassSchedule import session, host, aao_login, getCourseTable, \
    parseCourseTable, getExamSchedule, parseExamSchedule
from generateICS import create_ics, export_ics, create_exam_ics
from datetime import datetime, timedelta
from pytz import timezone
from time import time as nowtime
from http.cookies import SimpleCookie
from base64 import b64encode

from config import secret_key

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key  # 嘻嘻嘻

# s['flag_login'] = False
choice = 0  # 0 for std, 1 for class.个人课表or班级课表
# semester_year = '2019-2020'
# semester = '1'
semester_start_date = datetime(2020, 2, 24, 0, 0, 0,
                               tzinfo=timezone('Asia/Shanghai'))
# 20200213 Update to 2019-2020(2) Semester.

# 百度统计
js_statistic = """
<script>
    var _hmt = _hmt || [];
    (function() {
    var hm = document.createElement("script");
    hm.src = "https://hm.baidu.com/hm.js?30c55341ebeaa8f7a62f974564dc47c3";
    var s = document.getElementsByTagName("script")[0]; 
    s.parentNode.insertBefore(hm, s);
    })();
</script>
"""


@app.before_request
def before_request():
    if request.path == "/ical":
        if not s['flag_login']:
            # "<h3> ERROR! </br><a href='/'>请先登录！</a> </h3>"
            return redirect('/')


@app.after_request
def after_request(temp_response):
    return temp_response


@app.route('/favicon.ico')
def web_get_favicon():
    return send_file('static/favicon.ico')


@app.route('/vue', methods=['GET'])
def web_index():
    return render_template("index.html")


# @app.route('/get_captcha', methods=['GET'])
# def web_get_captcha():
#     """
#     获取验证码图片
#     """
#     captcha_resp = session.get(
#         host + '/eams/captcha/image.action')  # Captcha 验证码图片
#     # captcha_img = Image.open(BytesIO(captcha_resp.content))
#     # global captcha_text
#     # captcha_text = image_to_string(captcha_img)  # 前提是装了Tesseract-OCR，可以试试自动识别
#     # print(captcha_text)
#     response = make_response(captcha_resp.content)
#     response.headers['Content-Type'] = 'image/png'
#     return response


@app.route('/', methods=['GET'])
def web_login():
    """
    登录入口
    """
    s['flag_login'] = False
    session.cookies.clear()  # 先把之前的cookie给清除了
    # 改成用户的UA
    session.headers["User-Agent"] = request.headers.get('User-Agent')

    # 获取验证码图片，并转换为base64编码
    captcha_resp = session.get(
        host + '/eams/captcha/image.action')  # Captcha 验证码图片
    captcha_b64data = b64encode(captcha_resp.content).decode("utf-8")
    captcha_b64data = "data:image/png;base64," + captcha_b64data

    # 在同一个session下确保验证码有效
    cookie_string = ";".join([str(x) + "=" + str(y)
                               for x, y in captcha_resp.cookies.items()])
    s['cookie'] = cookie_string
    print(cookie_string)

    # return render_template("login.html")  # 临时测试用
    response = make_response(render_template(
        "login.html", pic_captcha=captcha_b64data))
    session.cookies.clear()
    # response.set_cookie(
    #     'desp', 'NUAA-iCal...For more information -- Please refer to https://github.com/miaotony/NUAA_ClassSchedule ')
    # s['id'] = request.remote_addr + str(nowtime())  # TODO 加一个id，用来防止重复提交请求
    # response.set_cookie('id', s.get('id'))
    return response


@app.route('/', methods=['POST'])
def web_login_post():
    """
    登录教务系统
    """
    session.cookies.clear()
    
    # 从request对象读取表单内容
    stuID = request.form['stuID']
    stuPwd = request.form['stuPwd']
    captcha_str = request.form['captcha']
    # print(stuID, stuPwd, captcha_str)

    # 确保在同一个cookie下访问
    cookie_string = s['cookie']
    temp_cookie = SimpleCookie()
    temp_cookie.load(cookie_string)
    temp_cookies = {}
    for key, morsel in temp_cookie.items():
        temp_cookies[key] = morsel.value
    print(temp_cookies)
    session.cookies = requests.utils.cookiejar_from_dict(temp_cookies)

    state, desp = aao_login(stuID, stuPwd, captcha_str, 1)
    print(desp)
    print("LOGIN", s.get('flag_login'))
    if state:
        s['flag_login'] = True
        # return redirect('/ical')
        # return """<head><meta http-equiv="refresh" content=";url=/ical"><title></title>""" + \
        #     js_statistic + "</head>" + \
        #     '<h3> Login OK! <br />正在导出课表及考试信息并生成iCal文件，' + \
        #     '<br /><strong>即将弹出下载界面!</strong></h3><br /><br /><a href=/>点击此处返回主页</a>'

        return web_ical()


    else:
        return """<head><meta http-equiv="refresh" content="3;url=/"><title>Error!</title>""" + \
            js_statistic + "</head>" + \
            '<h3>' + desp + '<br />即将返回主页...</h3>'


def web_export_ical():
    """
    导出ial文件
    """
    print('\n## Meow~下面开始获取{}课表啦！\n'.format({0: '个人', 1: '班级'}.get(choice)))
    courseTable = getCourseTable(choice=choice)
    list_lessonObj = parseCourseTable(courseTable)

    print('## 下面开始获取考试信息啦！\n')
    examSchedule = getExamSchedule()
    list_examObj = parseExamSchedule(examSchedule)

    print('## 信息获取完成，下面开始生成iCal日历文件啦！')
    cal = create_ics(list_lessonObj, semester_start_date)
    cal = create_exam_ics(cal, list_examObj)

    print('## 日历生成完成，下面开始导出啦！\n')
    response = make_response(cal.to_ical())
    response.headers["Content-Disposition"] = "attachment; filename=Schedule.ics"

    s['flag_login'] = False  # Fix `Login ERROR` bug.
    print('## 构造ical文件response完成！')
    session.cookies.clear()
    return response


@app.route('/ical', methods=['GET'])
def web_ical():
    """
    网页端导出ical文件
    """
    print('EXPORT ICAL!')
    return web_export_ical()


if __name__ == '__main__':
    while True:  # 防止程序崩溃后退出 （没用
        try:
            app.run(debug=True)
        except Exception as e:
            print('ERROR!', e)
        finally:
            session.cookies.clear()  # 清cookie
        #     flag_login = False
