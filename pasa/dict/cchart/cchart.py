# -*- coding: utf-8 -*-

from pasa.utils import getOrElse


class Cchart(object):
    def __init__(self, yaml):
        self.form = getOrElse(yaml, 'form', [])
        self.ctype = getOrElse(yaml, 'ctype', "")

    def __repr__(self):
        return "{{form={}, ctype={}}}".format(self.form, self.ctype)
