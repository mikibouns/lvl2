#!/home/igor/Документы/PYTHON/python_geekbrais/python_lvl2/bin/python3
# -*- coding: utf-8 -*-

from python_lvl2_lesson1_client import *
from subprocess import call
import pytest

# call('python_lvl2_lesson1_client', shell=True)

def setup_function(check_ip):
    print('возвращаемое значение: {}'.format(check_ip('127.0.0.1')))


def teardown_function(module):
    pass


def test_check_ip(check_ip):
    assert check_ip('127.0.0.1') == False
