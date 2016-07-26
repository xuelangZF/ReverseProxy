#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Last Modified time: 2016-06-01 20:14:13

from ReverseProxy.loadsetting import Setting
import unittest


class TestLoadSetting(unittest.TestCase):
    def setUp(self):
        self.file_path = "tests/setting.conf"
        self.debug = True
        self.online = False
        self.source_domain = "127.0.0.1:5000"
        self.target_domain = "www.jianshu.com"
        self.words_replace = {"简书": "复杂书官网", "发现": "隐藏", "登录": "上船"}

    def test_debug_setting(self):
        debug_setting = Setting(self.debug, self.file_path)
        self.assertEquals(debug_setting.html_expired, 120)
        self.assertEquals(debug_setting.js_css_expired, 3600)
        self.assertEquals(debug_setting.img_expired, 3600)
        self.assertEquals(debug_setting.source_domain, self.source_domain)
        self.assertEquals(debug_setting.target_domain, self.target_domain)
        self.assertEquals(debug_setting.words_replace, self.words_replace)

