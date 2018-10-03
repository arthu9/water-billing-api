from flask import Flask, jsonify, request, session, render_template, url_for, redirect
from model import DBconn
import flask, sys, os

app = Flask(__name__)
app.secret_key = 'celeron0912'
# app.config['SESSION_TYPE'] = 'filesystem'

def spcall(qry, param, commit=False):
    try:
        dbo = DBconn()
        cursor = dbo.getcursor()
        cursor.callproc(qry, param)
        res = cursor.fetchall()
        if commit:
            dbo.dbcommit()
        return res
    except:
        res = [("Error: " + str(sys.exc_info()[0]) + " " + str(sys.exc_info()[1]),)]
    return res

@app.route('/')
def index():
    return render_template('tabu2.html')

@app.route('/user', methods=['GET'])
def user():
    res = spcall('user_credentials', (), )

    if 'Error' in res[0][0]:
        return jsonify({'status': 'error', 'message': res[0][0]})
    else:
        recs = []

        for r in res:
            recs.append(
                {"username": r[0], "first_name": r[1], "last_name": r[2], "mobile_num": r[3], "admin_prev": str(r[4])})
        return jsonify({'status': 'ok', 'entries': recs, 'count': len(recs)})

@app.route('/register')
def register():
    res = spcall('register', ('joren123','Joren Mundane123','Pacaldo123', 'celeron0912123', '09675974534123', False), True)

    if 'Error' in res[0][0]:
        return jsonify({'status': 'error', 'message': res[0][0]})
    else:
        return res[0][0]

@app.after_request
def add_cors(resp):
    resp.headers['Access-Control-Allow-Origin'] = flask.request.headers.get(
        'Origin', '*')
    resp.headers['Access-Control-Allow-Credentials'] = True
    resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET, PUT, DELETE'
    resp.headers['Access-Control-Allow-Headers'] = flask.request.headers.get('Access-Control-Request-Headers',
                                                                             'Authorization')

    # set low for debugging

    if app.debug:
        resp.headers["Access-Control-Max-Age"] = '1'
    return resp


if __name__ == '__main__':
    app.debug=True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)