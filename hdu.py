import execjs
import re
import requests


def hduLogin(account, password):
    headers1 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-cn',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 yiban_iOS/4.9.2'
    }

    # -----  取回lt
    conn = requests.session()
    urlstr = conn.get(
        'https://cas.hdu.edu.cn/cas/login?state=24b335c3-ce7c-44ec-b488-d0092fa1219e&service=https%3A%2F%2Fcas.hdu.edu.cn%2Fcas%2Flogin%3Fservice%3Dhttps%253A%252F%252Fskl.hdu.edu.cn%252Fapi%252Fyiban%252Fpost-oauth%253Fstate%253D24b335c3-ce7c-44ec-b488-d0092fa1219e%2526h5%253Dtrue',
        headers=headers1)
    cookies = urlstr.cookies
    temp = re.findall(r'id="lt" name="lt" value="(.*?)"', urlstr.text)
    lt = temp[0]

    # -----des.js载入
    file = open("des.js", 'r', encoding='utf-8')
    jsstr = file.read()
    file.close()
    # ------计算rsa

    ctx = execjs.compile(jsstr)  # 加载JS文件
    rsa = ctx.call('strEnc', account.strip() + password.strip() + lt, '1', '2',
                   '3')  # 调用js方法  第一个参数是JS的方法名，后面的data和key是js方法的参数

    # --------
    params = 'rsa={0}&ul={1}&pl={2}&lt={3}&execution=e1s1&_eventId=submit'.format(rsa, len(account.strip()),
                                                                                  len(password.strip()), lt)

    # POST 登录取回cookies与location
    urlstr = conn.post(
        'https://cas.hdu.edu.cn/cas/login?state=24b335c3-ce7c-44ec-b488-d0092fa1219e&service=https%3A%2F%2Fcas.hdu.edu.cn%2Fcas%2Flogin%3Fservice%3Dhttps%253A%252F%252Fskl.hdu.edu.cn%252Fapi%252Fyiban%252Fpost-oauth%253Fstate%253D24b335c3-ce7c-44ec-b488-d0092fa1219e%2526h5%253Dtrue',
        data=params, headers=headers1, allow_redirects=False, cookies=cookies)
    cookies = urlstr.cookies

    urlstr = conn.get(urlstr.headers['Location'], headers=headers1, allow_redirects=False, cookies=cookies)
    urlstr = conn.get(urlstr.headers['Location'], allow_redirects=False, cookies=cookies)
    say = re.findall(r'value="(.*?)"', urlstr.text)

    urlstr = conn.post('https://o.yiban.cn/uiss/check?scid=30004_0&type=mobile', data='say=' + say[0], headers=headers1,
                       allow_redirects=False, cookies=cookies)

    return urlstr.cookies['access_token']