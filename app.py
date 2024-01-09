from flask import Flask, request, jsonify,render_template
import os
import json
import time
import requests

import JiaM

app = Flask(__name__)
headers = {
            'Referer':'https://weiban.mycourse.cn/',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
@app.route('/')
def index():
    return render_template("login.html")

@app.route("/Shu",methods=['POST'])
def Shu():
    json_a = request.get_data()
    json_a = json.loads(json_a)
    School = json_a['School']
    user_name = json_a['user_name']
    user_mm = json_a['user_mm']
    yzm = json_a['yzm']
    now = json_a['now']
    data = {}
    try:
        def get_School():
            ti = time.time()
            url = f'https://weiban.mycourse.cn/pharos/login/getTenantListWithLetter.do?timestamp={ti*100000}'
            session = requests.session()
            res = session.post(url,headers=headers).content.decode()
            res = json.loads(res)
            dit = {}
            for i in res['data']:
                for j in i['list']:
                    dit[j['name']] = j['code']
            return dit

        tenantCode = get_School()[School]
        palod = {
            "userName": user_name,
            "password": user_mm,
            "tenantCode": tenantCode,
            "timestamp": now,
            "verificationCode": yzm
            }
        a = JiaM.login(palod)
        session = requests.session()
        ti = time.time()
        url = f'https://weiban.mycourse.cn/pharos/login/login.do?timestamp={ti * 100000}'
        dat = {
            'data': a
        }
        
        res = session.post(url,data=dat).content.decode()
        res = json.loads(res)
        data['data'] = res
        data['state'] = '1'
        data['payload'] = a
    except Exception as e:
        data['state'] = '-1'
        data['data'] = str(e)
    return jsonify(data)



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)