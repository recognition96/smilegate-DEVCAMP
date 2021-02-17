import bcrypt
from flask import Flask, jsonify, request, render_template, url_for
from flask_jwt_extended import *
from werkzeug.utils import redirect

import DB

app = Flask(__name__)
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_SECRET_KEY'] = 'secret-string'
jwt = JWTManager(app)
DB = DB.DataBase()


@app.route('/', methods=['GET', 'POST'])
@jwt_optional
def index():
    """
    기본 페이지. @jwt_optional 사용으로 유저 로그인 시 다른 화면 구성
    """
    username = get_jwt_identity()
    print('current_user :', username)
    user_data = DB.select_user_by_id(username)

    return render_template('index.html', data=user_data)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    회원가입 기능. 아이디와 패스워드를 입력받음
    """
    if request.method == 'GET':
        return render_template('register.html')

    else:
        err = None
        user_data = dict()
        exist_user = DB.select_user_by_id(request.form['id'])
        if exist_user:
            err = '이미 존재하는 아이디입니다.'
            return render_template('register.html', error=err)
        else:
            user_data['id'] = request.form['id']
            user_data['pswd'] = request.form['pswd']
            user_data['pswd'] = bcrypt.hashpw(user_data['pswd'].encode("utf-8"), bcrypt.gensalt())
            user_data['pswd'] = user_data['pswd'].decode("utf-8")  # salt 를 이용하여 암호화 후, str 형태로 DB에 저장

            DB.insert_user(user_data)
            return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    로그인 처리. form 에 입력된 id, password 의 유효성 검사 및 토큰(access/refresh) 발급
    """
    if request.method == 'GET':
        return render_template('login.html')
    else:
        data = request.get_json()
        print('login :', data)
        user_input_id = data['id']
        user_input_pswd = data['password']
        exist_user = DB.select_user_by_id(user_input_id)

        if exist_user:
            # 가입되어 있는 유저
            if exist_user[0]['user_id'] == user_input_id and \
                    bcrypt.checkpw(user_input_pswd.encode("utf-8"), exist_user[0]['password'].encode("utf-8")):
                # 아이디 비밀번호 일치
                access_token = create_access_token(identity=user_input_id)
                refresh_token = create_refresh_token(identity=user_input_id)

                # JWT 쿠키를 반환하기 위해 token 할당
                resp = jsonify({'login': True})
                set_access_cookies(resp, access_token, max_age=60*10)       # 10분 후 만료
                set_refresh_cookies(resp, refresh_token, max_age=60*60*24)  # 24시간 후 만료
                return resp, 200

            else:
                # 아이디 비밀번호 불일치
                return jsonify({'login': False}), 200
        elif not user_input_id:
            # 아이디 미입력
            return jsonify({'login': None}), 200
        else:
            # 가입되지 않은 아이디
            return jsonify({'login': False}), 200


@app.route('/logout', methods=['GET'])
def logout():
    """
    로그아웃 처리. 쿠키에 저장된 access/refresh token 모두 삭제
    """
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200


@app.route('/refresh', methods=['GET'])
@jwt_refresh_token_required
def refresh():
    """
    새로운 access token 으로 갱신
    """
    username = get_jwt_identity()
    access_token = create_access_token(identity=username)
    print('refresh', username)
    resp = jsonify({'refresh': True})
    set_access_cookies(resp, access_token, max_age=60*10)
    return resp, 200


@app.route('/user-list', methods=['GET'])
@jwt_required
def user_list():
    """
    회원가입된 유저들의 목록을 조회
    """
    username = get_jwt_identity()
    all_users = DB.select_all_users()
    return render_template('user_list.html', users=all_users, cur_user=username)


@app.route('/user-edit', methods=['POST'])
@jwt_required
def user_edit():
    """
    회원가입된 유저들의 목록을 조회
    """
    user_id = request.form['user_id']
    DB.update_user_auth(user_id)
    return redirect(url_for('user_list'))


@app.route('/user-delete', methods=['POST'])
@jwt_required
def user_delete():
    """
    회원가입된 유저들의 목록을 조회
    """
    user_id = request.form['user_id']
    DB.delete_user(user_id)
    return redirect(url_for('user_list'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80', debug=True)
