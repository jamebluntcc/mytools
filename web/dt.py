from flask import Flask, render_template, request, jsonify
from models import db, generateDTcls, User
import json

DT = generateDTcls(User)


class myDT(DT):
    def to_list(self):
        return [c.name for c in self.__table__.columns]



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:passwd@host/db'
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data', methods=['GET', 'POST'])
def dt():
    if request.method == 'POST':
        playload = json.loads(request.form['data'])
        data = myDT(**playload)
        rs = data.result()
        return jsonify(rs)


if __name__ == '__main__':
    app.run()