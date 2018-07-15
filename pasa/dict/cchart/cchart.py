# -*- coding: utf-8 -*-

from pasa.utils import get_or_else


class Cchart(object):
    def __init__(self, yaml):
        self.form = get_or_else(yaml, 'form', [])
        self.ctype = get_or_else(yaml, 'ctype', "")

    def __repr__(self):
        return "{{form={}, ctype={}}}".format(self.form, self.ctype)
