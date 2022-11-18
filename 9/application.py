from flask import Flask, render_template, Blueprint, request, redirect
import urllib.request, json

endpoint = 'http://127.0.0.1:8080/pastebin/api'

app = Flask(__name__)

bp = Blueprint('mybp', __name__, 
               static_folder='static',
               static_url_path='/pastebin/static',
               template_folder='templates',
               url_prefix='/pastebin')

@bp.route(f'/', methods=['GET'])
@bp.route(f'/index.html', methods=['GET'])
def get_index():
    count_users = 0
    url = f'{endpoint}/users/'
    data = None
    headers = {'Accept': 'application/json'}
    method = 'GET'
    req = urllib.request.Request(url=url,
                                 data=data,
                                 headers=headers,
                                 method=method)
    with urllib.request.urlopen(req) as f:
        data = json.loads(f.read())
        count_users = len(data)

    count_pastes = 0
    url = f'{endpoint}/pastes/'
    data = None
    headers = {'Accept': 'application/json'}
    method = 'GET'
    req = urllib.request.Request(url=url,
                                 data=data,
                                 headers=headers,
                                 method=method)
    with urllib.request.urlopen(req) as f:
        data = json.loads(f.read())
        count_pastes = len(data)

    return render_template('index.html', 
                           count_users=count_users,
                           count_pastes=count_pastes)

@bp.route(f'/createuser', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        url = f'{endpoint}/users/'
        data = {'username': request.form['username'],
                'password': request.form['password']}
        headers = {'Accept': 'application/json',
                    'Content-Type': 'application/json;charset=utf-8'}
        method = 'POST'
        req = urllib.request.Request(url=url,
                                 data=json.dumps(data).encode('utf-8'),
                                 headers=headers,
                                 method=method)
        urllib.request.urlopen(req)
        return redirect('/pastebin/')
    elif request.method == 'GET':
        return render_template('createuser.html')

@bp.route(f'/createpaste', methods=['GET', 'POST'])
def create_paste():
    if request.method == 'POST':
        url = f'{endpoint}/users/{request.form["username"]}/verify/?password={request.form["password"]}'
        data = None
        headers = {'Accept': 'application/json'}
        method = 'GET'
        req = urllib.request.Request(url=url,
                                    data=json.dumps(data).encode('utf-8'),
                                    headers=headers,
                                    method=method)
        try:
            res = urllib.request.urlopen(req)
            if(res.getcode() == 200) :
                url = f'{endpoint}/users/{request.form["username"]}/pastes/?password={request.form["password"]}'
                data = {'title': request.form['title'],
                        'content': request.form['content']}
                headers = {'Accept': 'application/json',
                            'Content-Type': 'application/json;charset=utf-8'}
                method = 'POST'
                req = urllib.request.Request(url=url,
                                        data=json.dumps(data).encode('utf-8'),
                                        headers=headers,
                                        method=method)
                urllib.request.urlopen(req)
                return redirect('/pastebin/')
        except urllib.error.HTTPError:
            return redirect('/pastebin/createpaste')
    elif request.method == 'GET':
        return render_template('createpaste.html')

@bp.route(f'/users/<username>/pastes', methods=['GET'])
def get_pastes(username):
    count_pastes = 0
    url = f'{endpoint}/users/{username}/pastes/'
    data = None
    headers = {'Accept': 'application/json'}
    method = 'GET'
    req = urllib.request.Request(url=url,
                                 data=data,
                                 headers=headers,
                                 method=method)
    with urllib.request.urlopen(req) as f:
        data = json.loads(f.read())
        count_pastes = len(data)

    return render_template('pastes.html', 
                           user_name=username,
                           count_pastes=count_pastes,
                           pastes=data)

app.register_blueprint(bp)

if __name__=='__main__':
    app.run(port=8890)
	


