"""
NUAA_iCal_Web Backend
based on Flask

@time: 20191215
@Author: MiaoTony

"""
from flask import Flask, render_template, request, jsonify, url_for, \
    make_response, send_file, redirect
import requests
# from pytesseract import image_to_string
# from io import BytesIO
# from PIL import Image
from getClassSchedule import *
from generateICS import create_ics, export_ics, create_exam_ics
from datetime import datetime, timedelta
from pytz import timezone


app = Flask(__name__)

flag_login = False
choice = 0  # 0 for std, 1 for class.个人课表or班级课表
# semester_year = '2019-2020'
# semester = '1'
semester_start_date = datetime(2019, 9, 2, 0, 0, 0,
                               tzinfo=timezone('Asia/Shanghai'))


@app.route('/vue', methods=['GET'])
def web_index():
    session.cookies.clear()
    return render_template("index.html")


@app.route('/get_captcha', methods=['GET'])
def web_get_captcha():
    """
    获取验证码图片
    """
    captcha_resp = session.get(
        host + '/eams/captcha/image.action')  # Captcha 验证码图片
    # captcha_img = Image.open(BytesIO(captcha_resp.content))
    # global captcha_text
    # captcha_text = image_to_string(captcha_img)  # 前提是装了Tesseract-OCR，可以试试自动识别
    # print(captcha_text)
    response = make_response(captcha_resp.content)
    response.headers['Content-Type'] = 'image/png'
    return response


@app.route('/', methods=['GET'])
def web_login():
    """
    登录入口
    """
    session.cookies.clear()
    return render_template("login.html")  # 临时测试用
    # '''<form action="/login" method="post">
    #           <p>学号：   <input name="stuID"></p>
    #           <p>密码：   <input name="stuPwd" type="password"></p>
    #           <p>验证码：<input name="captcha"><img src="/get_captcha">
    #           <p><button type="submit">登录 & 导出iCal日历文件</button></p>
    #           </form>
    #           '''
    #    <p><input name="captcha"><img src="http://aao-eas.nuaa.edu.cn/eams/captcha/image.action">


@app.route('/login', methods=['POST'])
def web_login_post():
    """
    登录教务系统
    """
    # 从request对象读取表单内容
    stuID = request.form['stuID']
    stuPwd = request.form['stuPwd']
    captcha_str = request.form['captcha']
    print(stuID, stuPwd, captcha_str)
    state = aao_login(stuID, stuPwd, captcha_str, 1)
    print(state)
    global flag_login
    print("LOGIN", flag_login)
    if isinstance(state, bool):
        flag_login = True
        return redirect('/ical')
    else:
        return '<h3>' + state + '</h3>'


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
    # global flag_login
    # flag_login = False  # Fix `Login ERROR` bug.
    return response


@app.route('/ical', methods=['GET'])
def web_ical():
    """
    网页端导出ical文件
    """
    global flag_login
    print('EXPORT_ICAL', flag_login)
    if flag_login:
        flag_login = False  # Fix `Login ERROR` bug.
        return web_export_ical()
    else:
        return "<h3> ERROR! </br><a href='/'>请先登录！</a> </h3>"


if __name__ == '__main__':
    try:
        app.run(debug=False)
    except Exception as e:
        print('ERROR!', e)
    finally:
        session.cookies.clear()  # 清cookie
        flag_login = False
