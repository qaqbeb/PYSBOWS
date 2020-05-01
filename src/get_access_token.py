import requests
import sys
stdi,stdo,stde=sys.stdin,sys.stdout,sys.stderr
reload(sys)
sys.setdefaultencoding("utf-8" )
sys.stdin,sys.stdout,sys.stderr=stdi,stdo,stde

f1 = open("./code.txt",'r')
code = f1.read()
f1.close

APP_KEY = "1314197144"
APP_SECRET = "42f2b859b945d155fdeb6cf7d0ac1260"
CALLBACK_URL = "https://github.com/qaqbeb/PYSBOWS"

url = "https://api.weibo.com/oauth2/access_token?client_id="
url += APP_KEY + "&client_secret="+APP_SECRET+"&grant_type=authorization_code&redirect_uri="+CALLBACK_URL+"&code="+code

st = unicode('说明：\n在浏览器上输入：\n','gbk')
st += unicode('https://api.weibo.com/oauth2/authorize?client_id=1314197144&redirect_uri=https://github.com/qaqbeb/PYSBOWS','gbk')
st += unicode('\n在地址栏中获取code信息，填到源代码目录下的code.txt文件中\n\n\n','gbk')


r = requests.post(url)
f2 = open("./access_token.txt",'w')
f2.write(st)
f2.write(r.text)
f2.close
