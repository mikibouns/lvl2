#!/home/igor/Документы/PYTHON/python_geekbrais/python_lvl2/bin/python3
# -*- coding: utf-8 -*-

from client import *
from subprocess import call
import pytest

# call('python_lvl2_lesson1_client', shell=True)


def test_check_ip(check_ip):
    assert check_ip('127.0.0.1') == True

def test_check_ip_error(check_ip):
    assert check_ip('127.0.0.1') == False