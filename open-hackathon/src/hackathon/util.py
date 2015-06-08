# -*- coding: utf-8 -*-
#
# -----------------------------------------------------------------------------------
# Copyright (c) Microsoft Open Technologies (Shanghai) Co. Ltd.  All rights reserved.
#
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# -----------------------------------------------------------------------------------
from pytz import utc

from hackathon.log import (
    log,
)
import importlib
import urllib2
import json
import os
from datetime import datetime

try:
    from config import Config
except ImportError:
    from config_sample import Config


def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def get_config(key):
    ret = Config
    for arg in key.split("."):
        if arg in ret and isinstance(ret, dict):
            ret = ret[arg]
        else:
            return None
    return ret


def safe_get_config(key, default_value):
    r = get_config(key)
    return r if r else default_value


def mkdir_safe(path):
    if path and not (os.path.exists(path)):
        os.makedirs(path)
    return path


def get_remote(url, headers={}):
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(url, None, headers)
    resp = opener.open(request)
    return resp.read()


def delete_remote(url):
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(url)
    request.get_method = lambda: 'DELETE'
    opener.open(request)
    return "OK"


def get_class(kls):
    # kls is the full name of a class obj. e.g. "hackathon.registration.Registration"
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m


def load_template(url):
    try:
        template = json.load(file(url))
    except Exception as e:
        log.error(e)
        return None
    return template


def call(mdl_cls_func, cls_args, func_args):
    mdl_name = mdl_cls_func[0]
    cls_name = mdl_cls_func[1]
    func_name = mdl_cls_func[2]
    log.debug('call: mdl_name [%s], cls_name [%s], func_name [%s]' % (mdl_name, cls_name, func_name))
    mdl = importlib.import_module(mdl_name)
    cls = getattr(mdl, cls_name)
    func = getattr(cls(*cls_args), func_name)
    func(*func_args)


def get_now():
    return datetime.now(utc)


class Utility(object):
    def get_now(self):
        return get_now()

    def convert(self, input):
        return convert(input)

    def get_config(self, key):
        return get_config(key)

    def safe_get_config(self, key, default_value):
        return safe_get_config(key, default_value)

    def mkdir_safe(self, path):
        return mkdir_safe(path)