#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Last Modified time: 2016-06-01 20:14:13

from ReverseProxy.urlprocess import *
import unittest


class TestURLProcess(unittest.TestCase):
    def setUp(self):
        self.url_html = "http://www.baidu.com"
        self.url_jpg = "http://cnfeat.qiniudn.com/image/7niu-domin.jpg"
        self.url_png = "http://hupu.com/images/hupu/noneImg.png"
        self.url_css = "http://libs.useso.com/js/ckeditor/4.0.1/contents.min.css"
        self.url_js = "http://libs.useso.com/js/ckeditor/4.0.1/styles.min.js"
        self.url_anchor = "http://v2ex.com/t/285318#reply57"
        self.url_woff = "http://v2ex.com/static/fonts/fontawesome-webfont.woff2"

    def test_replace_domain(self):
        new_domain = "google.com"
        replaced_html = replace_domain(self.url_html, new_domain)
        replaced_jpg = replace_domain(self.url_jpg, new_domain)
        replaced_css = replace_domain(self.url_css, new_domain)
        replaced_js = replace_domain(self.url_js, new_domain)
        replaced_anchor = replace_domain(self.url_anchor, new_domain)
        self.assertEquals(replaced_html, "http://google.com")
        self.assertEquals(replaced_jpg, "http://google.com/image/7niu-domin.jpg")
        self.assertEquals(replaced_css, "http://google.com/js/ckeditor/4.0.1/contents.min.css")
        self.assertEquals(replaced_js, "http://google.com/js/ckeditor/4.0.1/styles.min.js")

    def test_replace_sub_domain(self):
        new_domain = "google.com"
        replace_jpg = replace_sub_domain(self.url_jpg, new_domain)
        replace_css = replace_sub_domain(self.url_css, new_domain)
        self.assertEquals(replace_jpg, "http://cnfeat.google.com/image/7niu-domin.jpg")
        self.assertEquals(replace_css, "http://libs.google.com/js/ckeditor/4.0.1/contents.min.css")

    def test_remove_anchor(self):
        self.assertEquals(remove_anchor(self.url_anchor), "http://v2ex.com/t/285318")

    def test_get_url_suffix(self):
        self.assertEquals(get_url_suffix(self.url_html), "html")
        self.assertEquals(get_url_suffix(self.url_jpg), "jpg")
        self.assertEquals(get_url_suffix(self.url_png), "png")
        self.assertEquals(get_url_suffix(self.url_css), "css")
        self.assertEquals(get_url_suffix(self.url_js), "js")
        self.assertEquals(get_url_suffix(self.url_woff), "woff2")
