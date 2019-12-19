## description  
**NUAA_iCal_Web**  

This is the **online version** of `NUAA_ClassSchedule`, based on `flask`.  
For local version, please refer to https://github.com/miaotony/NUAA_ClassSchedule.  


本项目为 `NUAA_ClassSchedule` 的在线版本，基于flask进行搭建。  
本地版本请参考： https://github.com/miaotony/NUAA_ClassSchedule  


目前已经部署在了 heroku 上，网址：  
https://nuaaical.herokuapp.com/  
或 [点击此处访问](https://nuaaical.herokuapp.com/)  


同时也部署在了 Azure 上，*（不过准备到期了）*，网址：  
https://nuaaicalweb.azurewebsites.net/   


**Web端仍在测试中**，欢迎提出issues & PRs.  
感兴趣的欢迎来写个好看一点的前端界面呗~  


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

Copyright © 2019 [MiaoTony](https://github.com/miaotony)