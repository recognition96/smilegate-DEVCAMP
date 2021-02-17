from flask import Flask, request, render_template, redirect, url_for, abort
from urllib.parse import urlparse
import string
import db_handle


app = Flask(__name__)
DB = db_handle.DataBase()
base = string.digits + string.ascii_letters  # 코드를 구성하는 문자들(숫자, 알파벳 대소문자)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['input_url']  # form 의 input 에 입력된 값을 불러옴
        if validate_url(original_url):
            if urlparse(original_url).scheme == '':  # scheme('http://') 가 없을 시 붙여줌
                original_url = 'http://' + original_url

            DB.insert_url(original_url)  # 저장되지 않은 새로운 url 이라면 해당 url 저장, 아니라면 count++
            url_id = DB.select_id_by_url(original_url)['id']  # 특정 url 에 저장된 id를 불러옴
            code = encode_url(url_id)
            encoded_url = 'localhost/' + code
            return render_template('input_page.html', short_url=encoded_url)

        else:  # 유효하지 않은 url
            return render_template('input_page.html', invalid_url=True)

    elif request.method == 'GET':  # 일반적인 접근 시 기본 화면
        return render_template('input_page.html')


@app.route('/<code>')
def redirect_short_url(code):
    # localhost 페이지가 아니라면 입력된 code 를 id 로 decode 하여 DB 조회
    url_id = decode_url(code)
    origin_url = DB.select_url_by_id(url_id)
    if origin_url is not None:  # 저장되어 있던 url 이라면 해당 url 로 redirect
        redirect_url = origin_url['origin']  # 저장된 실제 url
        return redirect(redirect_url)
    return render_template('home.html')


@app.route('/statistic')
def show_freq_urls():
    urls = DB.select_top5_url()
    return render_template('top5_page.html', urls=urls)


def encode_url(url_idx):
    """
    입력된 url 의 index 를 데이터베이스의 id 컬럼으로 사용하기 위해 encoding

    :param url_idx: [int] DB에 저장된 url의 id값
    :return: [str] id에 해당하는 url의 인덱스로부터 생성된 8자리 코드
    """
    result = []  # 코드화된 url
    while url_idx % 62 > 0 or not result:  # DB 테이블에 저장된 인덱스(id)를 코드화하여 결과 반환
        result.append(base[url_idx % 62])
        url_idx = int(url_idx / 62)
    code = ''.join(result)  # list to str
    code = code.zfill(8)    # 8자리 code 로 만들기 위해 좌측부터 '0'으로 패딩
    return code


def decode_url(code):
    """
    입력된 code 를 decoding 하여 DB의 index 로 변환

    :param code: [str] 변환하고자하는 8자리 코드
    :return: [int] 변환된 index
    """
    code_length = len(code)
    res = 0
    for i in range(code_length):
        res = 62 * res + base.find(code[i])
    return res


def validate_url(str_url):
    """
    입력된 url 검증

    :param str_url: [str] 입력한 url
    :return: [bool] 유효한 url 인지 여부
    """
    return '.' in str_url and len(str_url.rsplit('.', 1)[1]) >= 2


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

