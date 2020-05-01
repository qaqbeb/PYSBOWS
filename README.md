python spider
base on weibo sdk

获取授权使用get _access_token.py，先阅读access_token.txt中的信息
用户先向应用授权使用获取到code
将code填写到code.txt文件中
运行get_access_token.py，在access_token.txt文件中得到授权信息
将授权信息填写进config.json中的access_token条目（此后不需要重新授权）
运行pyspider.py，即可获取生成文件