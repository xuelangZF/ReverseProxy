#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Last Modified time: 2016-06-06 09:26:32
from .loadsetting import DomainSetting
import os


app_setting = DomainSetting('setting.conf')
basedir = os.path.abspath(os.path.dirname(__file__))
cache_dir = os.path.join(basedir, "cache/")
