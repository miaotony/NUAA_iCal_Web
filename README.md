# **NUAA_iCal_Web**  
## description  

This is the **online version** of `NUAA_ClassSchedule`, based on `flask`.  
For local version, please refer to https://github.com/miaotony/NUAA_ClassSchedule.  


本项目为 `NUAA_ClassSchedule` 的在线版本，基于flask进行搭建。  
本地版本请参考： https://github.com/miaotony/NUAA_ClassSchedule  

目前已经部署在了 heroku 上，网址：  
https://nuaaical.herokuapp.com/  
或 [点击此处访问](https://nuaaical.herokuapp.com/)  


**Web端仍在测试中**，欢迎提出issues & PRs.  
感兴趣的欢迎来写个好看一点的前端界面呗~  


## **Important!! 免责条款**  
本项目课表由官方教务系统导出，但使用时**请仔细对照教务系统核对是否所有课程均正常导出**！  

**对于解析异常导致的各种后果请自行承担！**   
*（坚决不背锅）*  

## web端部署折腾记  
详见blog：  
![https://miaotony.github.io/2019/12/29/Tech_NUAAiCalWeb_deploy/](https://miaotony.github.io/2019/12/29/Tech_NUAAiCalWeb_deploy/)  


## Usage  
### Step 1  
```bash
    pip install -r requirements.txt
```
Use `pip3` for linux.

### Step 2  
程序入口(Entry point): `web.py`  

For development environment, you can try it like this.   
```bash
    python web.py
```
Use `python3` for linux.  

**WARNING: Do not use the development server in a production environment.**   
Use a production WSGI server instead.  
For example, you can try `gunicorn`:  
```bash
    gunicorn web:app
```

## Reference  
`NUAA_ClassSchedule`  本项目本地版本
>项目网址：[点这里](https://github.com/miaotony/NUAA_ClassSchedule)  
https://github.com/miaotony/NUAA_ClassSchedule    

更多关于ical的信息请戳上面的网址呀~  


## Copyright  
本项目仅供学习研究使用，请在合理合法范围内使用，未经允许禁止任何形式的商用。  
最终解释权归本项目开发者所有。  

Copyright © 2019 [MiaoTony](https://github.com/miaotony)