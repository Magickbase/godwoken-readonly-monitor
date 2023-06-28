#! -*- coding:utf-8 -*-
# desc: godwoken node service monitor

from flask import Flask, jsonify, Response
from prometheus_client import Gauge, CollectorRegistry, push_to_gateway, generate_latest
import json
import re
import os
import requests

app = Flask(__name__)

class godwoken():
    def __init__(self):
        self.godwoken_baseurl = os.getenv('GODWOEKN_BASEURL')
        # 创建一个新的注册表对象
        self.registry = CollectorRegistry()

        # 创建Gauge类型指标
        self.api_status = Gauge('api_status', 'API status', registry=self.registry)
        self.gw_chain_block_height = Gauge('gw_chain_block_height', 'Godwoken chain block height', registry=self.registry)


    def update_metrics(self):
        ''' 获取 gw api status '''

        data = {
            "id": 42,
            "jsonrpc": "2.0",
            "method": "gw_ping",
            "params": []
        }
        try:
            r = requests.post(url=self.godwoken_baseurl,data=json.dumps(data))
            if "pong" in r.text and r.status_code == 200:
                self.api_status.set(1)
            else:
                self.api_status.set(0)
        except Exception as e:
            print(e)
            self.api_status.set(1)


        ''' 获取区块高度 '''
        # 发送 GET 请求获取指标数据
        try:
            response = requests.get(url=self.godwoken_baseurl + '/metrics')
            # 使用正则表达式从指标数据中过滤出 gw_chain_block_height 的值
            pattern = r'^gw_chain_block_height\s+(\d+)$'
            match = re.search(pattern, response.text, re.MULTILINE)
            if match:
                block_height = int(match.group(1))
                self.gw_chain_block_height.set(block_height)
        except Exception as e:
            print(e)
            self.gw_chain_block_height.set(1)

        data = generate_latest(self.registry)
        return Response(data, mimetype='text/plain')

# 定义一个路由，用于暴露指标
@app.route('/metrics')
def metrics():
    data = godwoken().update_metrics()
    return data

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
