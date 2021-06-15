"""
--*-- conding:utf-8 --*--
Author:zhaifanhua
Email:me@zhaifanhua.com
Time:2020.11.08 上午 02:27
"""

import json
import os
import sys
import time
from past.builtins import raw_input
from domain import domain_create
import xmltodict
import requests


def getxml(domain: str):
    url = "http://panda.www.net.cn/cgi-bin/check.cgi"
    res = requests.post(url, {"area_domain": domain})
    return res.content.decode('utf-8')


def xml_to_json(xmldoc):
    try:
        tmp = json.loads(json.dumps(xmltodict.parse(xmldoc, encoding='')))
    except Exception:
        tmp = {
            'property':{
                'returncode': -1,
                'original': '000',
            }
        }
    return tmp["property"]


def parse_out(domain: list):
    path = "./result"
    if not os.path.exists(path):
        os.makedirs(path)
    for key in domain:
        res_dict = xml_to_json(getxml(key))
        if res_dict["returncode"] == "200":
            statu = "请求成功"
        else:
            statu = "请求失败"
        if res_dict["original"][:3] == "210":
            original = "-------域名可以注册--------"

            with open("./result/result_true.txt", "a", encoding="utf8") as result_true:
                result_true.write(key + "\n")

        elif res_dict["original"][:3] == "211":
            original = "域名已经被注册"
        elif res_dict["original"][:3] == "212":
            original = "域名参数传输错误"
        else:
            original = "查询超时"
        out_str = "域名：{0}\t请求状态：{1}\t注册状态：{2}".format(key, statu, original)
        with open("./result/result.txt", "a", encoding="utf8") as result:
            result.write(out_str + "\n")
        time.sleep(2)
        print(out_str)
    raw_input("查询完毕！请在result文件夹下的result_true.txt中查看可购买的域名！感谢您的使用，请按任意键退出此窗口！")


def read_json():
    try:
        with open('./config.json', 'r', encoding="utf8") as c:
            config_json = json.load(c)
    except:
        print("配置文件出错！请检查config.json文件！按任意键退出此窗口")
        time.sleep(8)
        sys.exit(1)
    if config_json["count"] is None or config_json["bits"] is None:
        raw_input("配置文件出错！请检查config.json文件！ 按任意键退出此窗口")

    return config_json


if __name__ == '__main__':
    config = read_json()
    domain_list = domain_create(domain_list=list(config["domain_list"]), count=int(config["count"]),
                                bits=int(config["bits"]), ext=list(config["exts"]))
    parse_out(domain_list)
