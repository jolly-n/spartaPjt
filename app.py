from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbpymongo

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/memo', methods=['GET'])
def listing():
    sample_receive = request.args.get('sample_give')
    print(sample_receive)
    return jsonify({'msg':'GET 연결되었습니다!'})

## API 역할을 하는 부분
@app.route('/memo', methods=['POST'])
def post_Article():
    # url, comment 받아오기
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']

    # 받아온 url을 통해 title, image, desc 크롤링해오기
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    # og:image | og:title | og:description 가져오기
    title = soup.select_one('meta[property="og:title"]')['content']
    img = soup.select_one('meta[property="og:image"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content']

    # db에 저장하기
    doc = {
        'title' : title,
        'img' : img,
        'desc' : desc,
        'url' : url_receive,
        'comment' : comment_receive
    }
    db.alonememo.insert_one(doc)

    return jsonify({'msg':'저장이 완료되었습니다😊'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)