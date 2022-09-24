> # 微信推送开发文档介绍
> ## 根据模板发送消息
```http
https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Template_Message_Interface.html#5
```
![](https://s1.ax1x.com/2022/08/26/vRAy5D.png)
```Python
# 参数	     是否必填	          说明
# touser	        是	            接收者openid
# template_id	    是	            模板ID
# url	            否	            模板跳转链接（海外帐号没有跳转能力）
# miniprogram	    否	            跳小程序所需数据，不需跳小程序可不用传该数据
# appid	            是	            所需跳转到的小程序appid（该小程序 appid 必须与发模板消息的公众号是绑定关联关系，暂不支持小游戏）
# pagepath	        否	            所需跳转到小程序的具体页面路径，支持带参数,（示例index?foo=bar），要求该小程序已发布，暂不支持小游戏
# data	            是	            模板数据
# color	            否	            模板内容字体颜色，不填默认为黑色
# client_msg_id	    否	            防重入id。对于同一个openid + client_msg_id, 只发送一条消息,10分钟有效,超过10分钟不保证效果。若无防重入需求，可不填


# 可将非必要信息删除
def send(access_token):
    # 请求链接
    url=f'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}'
    # 请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    # POST提交数据
    data={
           "touser":"用户Openid",
           "template_id":"模板id",
           "url":"点击详情后打开的链接http://weixin.qq.com/download",  
        #    "miniprogram":{
        #      "appid":"xiaochengxuappid12345",
        #      "pagepath":"index?foo=bar"
        #    },
        #    "client_msg_id":"MSG_000001",
           "data":{
                   "first": {
                       "value":"恭喜你购买成功！",
                       "color":"#173177"
                   },
                   "keyword1":{
                       "value":"巧克力",
                       "color":"#173177"
                   },
                   "keyword2": {
                       "value":"39.8元",
                       "color":"#173177"
                   },
                   "keyword3": {
                       "value":"2014年9月22日",
                       "color":"#173177"
                   },
                   "remark":{
                       "value":"欢迎再次购买！",
                       "color":"#173177"
                   }
           }
       }
# 在调用模板消息接口后，会返回 JSON 数据包。正常时的返回 JSON 数据包示例：
#  {
#     "errcode":0,
#      "errmsg":"ok",
#      "msgid":200228332
#   }
    response = requests.post(url, headers=headers, json=data).json()
    if response["errcode"] == 0:
        print("[INFO]推送消息成功")
    else:
        print(f"[INFO]微信推送失败:{response}")
```
![](https://s1.ax1x.com/2022/08/26/vRVC0P.png)
> ## 根据上图分析模板信息填写规则
```微信模板
{{first.DATA}}=恭喜你购买成功！
{{keyword1.DATA}}=巧克力
{{keyword2.DATA}}=39.8元
{{keyword3.DATA}}=2014年9月22日
{{remark.DATA}}=欢迎再次购买！
```
> # 了解完推送消息框架,理顺一下思路
> ## 1.获取到access_token即可发送消息
![](https://s1.ax1x.com/2022/08/26/vRePJS.png)
```Python
# 开发文档https://developers.weixin.qq.com/doc/offiaccount/Basic_Information/Get_access_token.html

# 根据开发文档获取access_token
def get_access_token(APPID,APPSECRET):
    url=f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}'
    access_token = requests.get(url).json()['access_token']
    return access_token
```
> ## 2.发送消息的参数:用户的Openid,模板id,url(可要可不要)
![](https://s1.ax1x.com/2022/08/26/vReKiT.png)
![](https://s1.ax1x.com/2022/08/26/vReQWF.png)
> # 最后一点点添加内容(api或者爬虫获取数据)
> ## 随机颜色
```Python
import random
def color():
    color_ra = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])]
    return color_ra
```
> ## 爬取中国天气网:http://www.weather.com.cn/
```Python
# 获取温度
def get_weather(city_id):
    # 时间戳
    t = (int(round(time() * 1000)))
    headers = {
        "Referer": "http://www.weather.com.cn/",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    url = f"http://d1.weather.com.cn/weather_index/{city_id}.html?_={t}"
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"
    #print(response.text)
    response_data_0 = eval(response.text.split(";")[0].split("=")[-1])
    response_data_2 = eval(response.text.split(";")[2].split("=")[-1])
    weatherinfo_0 = response_data_0["weatherinfo"]
    # 城市名称
    city_name = weatherinfo_0['city']
    # 最高气温
    max_wd = weatherinfo_0["temp"]
    # 最低气温
    min_wd = weatherinfo_0["tempn"]
    # 天气
    weather = weatherinfo_0["weather"]
    # 相对湿度
    shidu = response_data_2['SD']
    return city_name, weather, max_wd, min_wd, shidu
```
> ## 添加疫情模块：百度的实时疫情数据爬虫
```Python
# 实时疫情
def cqyq():
    url = 'https://opendata.baidu.com/data/inner?tn=reserved_all_res_tn&resource_id=28565&query=上海新型肺炎最新动态'
    data = requests.get(url).json()['data'][0]['result']['items']
    yq_data = '\n'
    for i in range(3):
        title = data[i]['eventDescription']
        # url = data[i]['eventUrl']
        yq_data += title+"\n"
    print('[INFO]疫情模块加载正常')
    return yq_data
```
> # 最后自己根据自己的需求啥的修改相关内容即可
> # 代码很简单！本质上就是在发送json数据中添加简单的api和爬虫的数据。
> # 完整代码(自己修改之后的,不喜欢自己改)
```Python
import random
from time import time, localtime
import requests
from datetime import datetime
import re


#########################################################################################################
# 接收的用户
users = ["###",'####']
# 模板ID
template_id='####'
# 天气信息id:查询:https://img.weather.com.cn/newwebgis/fc/nation_fc24h_wea_2022010420.json
city_id='####'
# 测试号配置信息
app_id = "####"
app_secret = "####"
# 特殊日期
to_time=[2017,9,1]
##########################################################################################################


# 获取token
def get_access_token():
    post_url = (
        f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}")
    try:

        access_token = requests.get(post_url).json()['access_token']
        print('[INFO]获取access_token成功!')
        return access_token
    except:print('[INFO]获取access_token失败请检查app_id和app_secret')

# 获取随机颜色
def color():
    color_ra = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])]
    return color_ra[0]

# 随机一言
def yiyan():
    url = 'http://api.botwl.cn/api/yiyan?type='
    try:
        yy = requests.get(url).text
        print('[INFO]一言模块加载正常')
        return yy
    except:print('[INFO]一言模块加载失败,请检查接口')

# 重庆疫情
def cqyq():
    url = f'https://opendata.baidu.com/data/inner?tn=reserved_all_res_tn&resource_id=28565&query={city}新型肺炎最新动态'
    try:
        data = requests.get(url).json()['data'][0]['result']['items']
        data_print = '\n'
        for i in range(4):
            title = data[i]['eventDescription']
            data_print += title+"\n"
        print('[INFO]疫情模块加载正常')
        return data_print
    except:print('[INFO]疫情模块加载失败,请重新调试')

# 获取温度
def get_weather(city_id):
    # 时间戳
    t = (int(round(time() * 1000)))
    headers = {
        "Referer": "http://www.weather.com.cn/",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    url = f"http://d1.weather.com.cn/weather_index/{city_id}.html?_={t}"
    try:
        response = requests.get(url, headers=headers)
        response.encoding = "utf-8"
        response_data_0 = eval(re.findall("var cityDZ =(.*?);var", response.text)[0])
        response_data_2 = eval(re.findall("var dataSK =(.*?);var", response.text)[0])
        response_data_3 = eval(re.findall("var dataZS =(.*?);var", response.text)[0])
        weather_data = response_data_0["weatherinfo"]
        # 城市名称
        city_name = weather_data['city']
        # 最高气温
        max_wd = weather_data["temp"]
        # 最低气温
        min_wd = weather_data["tempn"]
        # 天气
        weather = weather_data["weather"]
        # 相对湿度
        shidu = response_data_2['SD']
        # 生活指数
        zs=response_data_3['zs']
        tips = '\n晨练'+zs['cl_hint']+':'+zs['cl_des_s']+'\n穿衣小贴士:'+zs['ct_des_s']
        print('[INFO]天气模块加载正常')
        return city_name, weather, max_wd, min_wd,shidu, tips
    except:print('[INFO]天气模块加载失败,请检查和调试接口')

# 推送信息
def send(template_id,user, access_token, city_name , weather, max_wd, min_wd,shidu, tips, yy,cqyq):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    today = datetime.date(datetime(year=localtime().tm_year, month=localtime().tm_mon, day=localtime().tm_mday))
    week = week_list[today.isoweekday() % 7]
    data = {
        "touser": user,
        "template_id": template_id,  # 模板id
        "url": "http://linxi.tk",
        "topcolor": "#FF0000",
        "data": {
            "date": {
                "value": "{} {}".format(today, week),
                "color": color()
            },
            "time": {
                "value": (datetime.today() - datetime(to_time[0],to_time[1],to_time[2])).days,
                "color": color()
            },
            "city": {
                "value": city_name,
                "color": color()
            },
            "weather": {
                "value": weather,
                "color": color()
            },
            "min_wd": {
                "value": min_wd,
                "color": color()
            },
            "max_wd": {
                "value": max_wd,
                "color": color()
            },
            "tips": {
                "value": tips,
                "color": color()
            },
            "shidu": {
                "value": shidu,
                "color": color()
            },
            "yy": {
                "value": yy,
                "color": color()
            },
            "yiqing": {
                "value": cqyq,
                "color": color()
            },
            "wh": {
                "value": "希望收到消息的你永远开心！",
                "color": color()
            },
        }
    }
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    response = requests.post(url, headers=headers, json=data).json()
    if response["errcode"] == 0:
        print("[INFO]推送消息成功")
    else:
        print(f"[INFO]微信推送失败:{response}")


if __name__ == "__main__":
    # 获取access_token
    access_token = get_access_token()
    # 一言信息
    yy = yiyan()
    # 疫情信息
    cqyq = cqyq()
    # 公众号推送消息
    for user in users:
        # 传入省份和市获取天气信息
        city_name, weather, max_wd, min_wd,shidu,tips = get_weather(city_id)
        send(template_id,user, access_token, city_name, weather, max_wd, min_wd,shidu,tips, yy,cqyq)
```
```模板
{{date.DATA}} 
今天是中考后的第{{time.DATA}}天 
城市：{{city.DATA}} 
天气：{{weather.DATA}} 
最低气温: {{min_wd.DATA}} 
最高气温: {{max_wd.DATA}} 
相对湿度: {{shidu.DATA}} 
生活指数: {{tips.DATA}} 
随机一言: {{yy.DATA}} 
疫情更新: {{yiqing.DATA}} 
林夕的问候:{{wh.DATA}}
```
> # 独立配置信息的在github
```http
https://github.com/linxi-520/wxapi
```
![](https://s1.ax1x.com/2022/08/27/vR0kqI.png)
