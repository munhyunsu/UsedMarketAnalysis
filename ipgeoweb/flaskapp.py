#!/usr/bin/env python3

import sys
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('search')
def search():
    return render_template('search.html')
