from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbpymongo


# HTML 화면 보여주기
@app.route('/')
def myshop():
    return render_template('index.html')


# 주문하기(POST) API
@app.route('/order', methods=['POST'])
def save_order():
    # 이름|수량|주소|전화번호 받아오기
    name_receive = request.form['name_give']
    count_receive = request.form['count_give']
    address_receive = request.form['address_give']
    phone_receive = request.form['phone_give']

    # 데이터 몽고디비에 저장하기
    doc = {
        'name': name_receive,
        'count': count_receive,
        'address': address_receive,
        'phone': phone_receive
    }
    db.myshop.insert_one(doc)

    return jsonify({'msg': '주문이 완료되었어요😊'})


# 주문 목록보기(Read) API
@app.route('/order', methods=['GET'])
def view_order():
    # 몽고디비에서 저장된 데이터 가져오기
    orders = list(db.myshop.find({}, {'_id': False}))
    # orders 정보 보내주기
    return jsonify({'all_orders':orders})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)