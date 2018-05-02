from urllib import parse
from flask import Flask, request, render_template
from parse import get_permissions
from db import Permission, DoesNotExist
from config import HOST, PORT


app = Flask('permissions')


def render(permissions=None):
    return render_template('main.html', permissions=permissions or {})


@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render()

    link = request.form['link']
    pr = parse.urlparse(link)
    params = parse.parse_qs(pr.query)
    id_ = params['id'][0]
    hl = params.get('hl', ['ru'])[0]

    try:
        permissions = Permission.get(app_id=id_, hl=hl).permissions
    except DoesNotExist:
        permissions = get_permissions(id_, hl)
        Permission.create(app_id=id_, hl=hl, permissions=permissions)

    return render(permissions)


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)