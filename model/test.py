﻿# coding:utf-8

from peewee import *
from model import BaseModel


class Test(BaseModel):
    test = TextField()
