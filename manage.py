#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@FileName: manage.py
@Time    : 2022/8/14 18:14
@Author  : 热气球
@Software: PyCharm
@Version : 1.0
@Contact : 2573514647@qq.com
@Des     : 
"""
from RealProject import create_app

app = create_app()
if __name__ == '__main__':
    app.run(debug=True)
