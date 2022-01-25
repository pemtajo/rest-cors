#!/usr/bin/python3
# coding=UTF-8
# encoding=UTF-8

from bs4 import BeautifulSoup
from flask import Flask, request
from flask_cors import CORS
import requests
import os
import unicodedata as ud
from datetime import datetime

app = Flask(__name__)
CORS(app)

def remove_chars(str):
    str = ud.normalize('NFD', str) # * " \ / < > : | ?
    str = str.replace('\\', '')
    str = str.replace('/', '')
    str = str.replace('[', '')
    str = str.replace(']', '')
    str = str.replace(':', '-')
    str = str.replace('|', '-')
    str = str.replace('#', '')
    str = str.replace('^', '')

    str = str.replace('*', '')
    str = str.replace('"', '')
    str = str.replace('<', '')
    str = str.replace('>', '')
    str = str.replace('?', '')
    return str

@app.route("/jira", methods=["GET"])
def jira():
    try:
        url = request.args.get('url')
        r = requests.get(url, headers = {'Authorization': request.headers['Authorization']})
        data = r.json()
        return {'title': remove_chars(data['fields']['summary']), 'description':data['fields']['description']}
    except Exception as exp:
        print(exp)
        return {'error': str(exp)}, 500

@app.route("/title", methods=["GET"])
def url_informations():
    try:
        url = request.args.get('url')
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        return {'title': remove_chars(soup.title.string), 'zettelkasten': datetime.now().strftime("%Y%m%d%H%M")}
    except Exception as exp:
        print(exp)
        return {'error': str(exp)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=os.getenv("PORT", 5000))