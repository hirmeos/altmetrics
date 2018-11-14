# -*- coding: utf-8 -*-
import os

from flask import Flask

CONFIG = os.getenv('CONFIG', 'DevConfig')

app = Flask(__name__)
app.config.from_object(f'core.settings.{CONFIG}')
