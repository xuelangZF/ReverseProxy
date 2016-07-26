#! /usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing

bind = "0.0.0.0:80"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"
