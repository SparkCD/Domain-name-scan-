"""
--*-- conding:utf-8 --*--
Author:zhaifanhua
Email:me@zhaifanhua.com
Time:2020.11.08 上午 02:27
"""

import random


def domain_create(domain_list, count=50, bits=5, ext: list = [".com", ".cn", ".net"]):
    """
            域名生成方法
    :param domain_list:域名可选字典
    :param count:域名生成数量
    :param bits:域名长度
    :param ext:域名后缀
    :return: domain_list
    """
    if len(domain_list) == 0:
        domain_list = [chr(i) for i in range(97, 123)]  # 默认为a到z全字典
    input_str = ""

    input_list = []
    for n in range(count):
        for f in range(bits):
            i = random.randint(0, len(domain_list) - 1)
            input_str += domain_list[i]
        if len(ext) == 0:
            ext = [".com"]
        for e in ext:
            input_list.append(input_str + e)
        input_str = ""
    return input_list


if __name__ == '__main__':
    num_list = ['t', 'u', 'b', 'g', 'l', 'z', 'y', 'q']
    print(domain_create(num_list, 500, 5))
