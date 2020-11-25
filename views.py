import re


def render(template_path, params={}):
    with open(template_path, 'r') as f:
        html = f.read()
    # 找到所有模板标记
    if params:
        markers = re.findall('%%(.*?)%%', html)
        for marker in markers:
            tag = re.findall('%%' + marker + '%%', html)[0]
            if params.get('%s' % marker):
                html = html.replace(tag, params.get('%s' % marker))
            else:
                html = html.replace(tag, '')
    return html


def index(request):
    return render('template/index.html', {'username': 'zack', 'password': '123456'})


def login(request):
    return render('template/login.html')


def register(request):
    return render('template/register.html')


def error(request):
    return render('template/error.html')