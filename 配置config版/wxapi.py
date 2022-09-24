import random
from time import time, localtime
import requests
from datetime import datetime
import re,os,sys


#########################################################################################################
# 打开配置文件,并转为json格式读取信息
with open("config.txt", encoding="utf-8") as f:
    config = eval(f.read())
# 接收的用户
users =config['users']
# 模板ID
template_id=config['template_id']
# 天气信息
city_id=config['city_id']
# 城市疫情
city=config['city']
# 测试号配置信息
app_id = config['app_id']
app_secret = config['app_secret']
# 特殊日期
to_time=config['to_time']
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
    os.system("pause")
    sys.exit(1)
