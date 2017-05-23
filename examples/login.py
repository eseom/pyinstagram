"""
make a settings.py file.

# filename: settings.py
username = '<your usernaem>'
password = '<your password>'
"""

from __future__ import unicode_literals, print_function

from pyinstagram.instagram import Instagram
from pyinstagram.setting import Setting
from settings import username, password

Setting.create_instance('file', {
    'base_directory': './sessions'
})

instagram = Instagram(Setting.instance())
instagram.set_user(username, password)
instagram.login()

print('instagram', instagram)
