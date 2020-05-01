import requests
import weibo
import xlwt
import json
import jsonpath
import sys
from weibo import APIClient


stdi,stdo,stde=sys.stdin,sys.stdout,sys.stderr
reload(sys)
sys.setdefaultencoding("utf-8" )
sys.stdin,sys.stdout,sys.stderr=stdi,stdo,stde

filename_in = "./config.json"
filename_out = "./friends_list.txt"
filename_lastest_weibo = "./lastestweibo.txt"

        
def get_config(filename_in):       #��ȡ��config_json�ļ���������ݣ�����һ���ֵ�
        with open(filename_in,'r')as load_f:
                load_dict=json.load(load_f)
                load_f.close()
        return load_dict


def home_timeline(access_token,page):        #����access_token����home_timeline api�����غ��ѵ�����΢����Ϣ
        url = "https://api.weibo.com/2/statuses/home_timeline.json"
        url = url + "?access_token="+access_token+"&count=100&page="+str(page)
        js = requests.get(url)
        return js.content


def friendlist(access_token,client):    #����access_token����friendlist api�������û������к����б����Ϣ
        js=client.friendships.friends.get(access_token=access_token,screen_name="swj515")
        return js

def generate_sheet(js,cursor):          #���ݵ���api�õ���json��Ϣ������Ӧ�ı��
        num=0
        name_list = jsonpath.jsonpath(js,'$..name')
        followers_count_list = jsonpath.jsonpath(js,'$..followers_count')
        friends_count_list = jsonpath.jsonpath(js,'$..friends_count')
        statuses_count_list = jsonpath.jsonpath(js,'$..statuses_count')
        bi_followers_count_list = jsonpath.jsonpath(js,'$..bi_followers_count')
        workbook=xlwt.Workbook(encoding='gbk')
        w = workbook.add_sheet('My Worksheet')
        w.write(0,0,'�����û���\��Ŀ')
        w.write(0,1,'��˿��')
        w.write(0,2,'��ע��')
        w.write(0,3,'������')
        w.write(0,4,'΢����')
        w.write(0,6,'ƽ����Ծ�̶ȣ�΢������')
        w.write(0,7,'��˿�����')
        for i in range(len(name_list)):
                w.write(i+1,0,name_list[i])
        
        for i in range(len(followers_count_list)):
                w.write(i+1,1,followers_count_list[i])
                if followers_count_list[i] == max(followers_count_list):
                        mark=i
        
        for i in range(len(friends_count_list)):
                w.write(i+1,2,friends_count_list[i])
        
        for i in range(len(bi_followers_count_list)):
                w.write(i+1,3,bi_followers_count_list[i])
        
        for i in range(len(statuses_count_list)):
                w.write(i+1,4,statuses_count_list[i])
                num+=statuses_count_list[i]

        w.write(1,6,(num/len(statuses_count_list)))
        st = name_list[mark]+"("+ str(followers_count_list[mark]) +")"
        w.write(1,7,st)
        workbook.save('friends_list.xls')




def output_timeline(js):
        user_list = jsonpath.jsonpath(js,'$..user')
        text_list = jsonpath.jsonpath(js,'$..text')
        time_list = jsonpath.jsonpath(js,'$..created_at')
        fp = open(filename_lastest_weibo,"w")
        for i in range(len(user_list)):
                user = user_list[i]
                s1 = unicode('�û�����','gbk')
                s2 = "\n" + s1 + user["screen_name"]
                fp.write(s2)
                s1 = unicode('΢�����ݣ�','gbk')
                s2 = "\n" + s1 + text_list[i]
                fp.write(s2)
                s1 = unicode('����ʱ�䣺','gbk')
                s3 = "\n" + s1 + time_list[i]
                fp.write(s3)
                fp.write("\n")
        fp.close()

         

def main():
        data = get_config(filename_in)
        client = APIClient(app_key=data["APP_KEY"], app_secret=data["APP_SECRET"], redirect_uri=data["CALLBACK_URL"])
        access_token=data["access_token"]
        js = friendlist(access_token,client)
        js = json.dumps(js,ensure_ascii=False)
        fp = open(filename_out,"w")
        fp.write(js)
        fp.close()
        print("������ļ��ɹ�")
        js = json.loads(js)
        generate_sheet(js,0)
        js = home_timeline(access_token,1)
        js = json.loads(js)
        output_timeline(js)
        js = home_timeline(access_token,2)
        js = json.loads(js)
        output_timeline(js)
        fp.close()
        
        

if __name__ == '__main__':
    main()
