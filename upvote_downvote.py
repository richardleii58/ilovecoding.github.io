
import json 
import requests
import time
import urllib
#import sqlite3
import datetime
import keep_alive
#import os
#import mysql.connector
from replit import db

TOKEN = "6329785274:AAHBLa5x51N_74W9QpqhUcI77os5MhtbO2o"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)



def get_url(url):
  response = requests.get(url)
  content = response.content.decode("utf8")
  return content


def get_json_from_url(url):
  content = get_url(url)
  js = json.loads(content)
  return js


def get_updates(offset=None):
  url = URL + "getUpdates?timeout=100"
  if offset:
    url += "&offset={}".format(offset)
  js = get_json_from_url(url)
  return js


def get_last_chat_id_and_text(updates):
  num_updates = len(updates["result"])
  last_update = num_updates - 1
  text = updates["result"][last_update]["message"]["text"]
  chat_id = updates["result"][last_update]["message"]["chat"]["id"]
  return (text, chat_id)


def send_message(text, chat_id):
  text = urllib.parse.quote_plus(text)
  url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
  get_url(url)

def promote_Chat_Member(chat_id, user_id,k):
  url1=URL+'promoteChatMember?chat_id={}&user_id={}&is_anonymous=False&can_manage_chat=False&can_delete_messages=False&can_manage_voice_chats=False&can_restrict_members=False&can_promote_members=False&can_change_info=False&can_invite_users=True&can_pin_messages=False'.format(chat_id,user_id)
  url2=URL+'setChatAdministratorCustomTitle?chat_id={}&user_id={}&custom_title={}'.format(chat_id,user_id,k)
  get_url(url1)
  get_url(url2)

def get_last_update_id(updates):
  update_ids = []
  for update in updates["result"]:
    update_ids.append(int(update["update_id"]))
  return max(update_ids)

def add_points(updates):
  for x in updates['result']:
    try:
      if 'reply_to_message' in x['message'] and x['message']['text']=='+':
        if x['message']['text']=='+':
          sender=str(x['message']['from']['id'])
          points=db['mem'][sender][1]
          if points>=1700:
            to_add_to=str(x['message']['reply_to_message']['from']['id'])
            if to_add_to not in db['mem']:
              name_to_add=x['message']['reply_to_message']['from']['first_name']
              db['mem'][to_add_to]=[name_to_add,0]    
            old_points=db['mem'][to_add_to][1]
            new_points=old_points + 3
            name=x['message']['reply_to_message']['from']['first_name']
            chat = x["message"]["chat"]["id"]
            check_uprank(old_points, new_points, chat, name,to_add_to)
            name_to_add=x['message']['reply_to_message']['from']['first_name']
            db['mem'][to_add_to][1]=new_points 
            date_to_add=datetime.date.today()
            db['Ph'].append([to_add_to,3,date_to_add.isoformat()])
            chat = x["message"]["chat"]["id"]
            send_message('That was insightful!',str(chat))
      elif 'new_chat_participant' in x and x['message']['from']!=x['new_chat_participant']:
        to_add_to=str(x['message']['from']['id'])
        if to_add_to not in db['mem']:
          name_to_add=x['message']['from']['first_name']
          db['mem'][to_add_to]=[name_to_add,0]
        old_points=db['mem'][to_add_to][1]
        new_points=old_points + 1
        name=x['message']['from']['first_name']
        chat = x["message"]["chat"]["id"]
        db['mem'][to_add_to][1]=new_points
        check_uprank(old_points, new_points, chat, name,to_add_to)
        date_to_add=datetime.date.today()
        db['Ph'].append([to_add_to,1,date_to_add.isoformat()])
      elif ('text' in x['message']) or ('reply_to_message' in x['message'] and x['message']['text']!='+'):
        to_add_to=str(x['message']['from']['id'])
        points=len(x['message']['text']//25)
        db['inactive'][to_add_to]=0
        if points>3:
          points=3
        if points>0:
          to_add_to=str(x['message']['from']['id'])
          if to_add_to not in db['mem']:
            name_to_add=x['message']['from']['first_name']
            db['mem'][to_add_to]=[name_to_add,0]
          old_points=db['mem'][to_add_to][1]
          new_points=old_points + points
          name=x['message']['from']['first_name']
          chat = x["message"]["chat"]["id"]
          check_uprank(old_points, new_points, chat, name,to_add_to)
          db['mem'][to_add_to][1]=new_points
          name_to_add=x['message']['from']['first_name']
          date_to_add=datetime.date.today()
          lsttoadd=([to_add_to,points,date_to_add.isoformat()])
          db['Ph'].append(lsttoadd)
        if x['message']['text']=='Get_secret_leaderboard':
          update_rank(x["message"]["chat"]["id"])
        if x['message']['text']=='Get_secret_stat':
          send_message(str(db['test']),x['message']['chat']['id'])
                    
                
    except Exception as e:
      print('errorShux')
      print(e)


def check_demotion(old,new,chat,user):
    ps={'MINU Initiate':150,'Senior Initiate':250,'Crewman':400, 'SGT MINU':700, 'Staff SGT MINU':1000, 'Captain':1200, 'Lt. Commander':1500, 'Commander':1700, 'Cpt. Commander':2000, 'Rear Admiral':2599, 'Vice Commander':3000 ,'Commander MINU':2600}
    keyss=list(ps.keys())
    for k in keyss:
      if old>ps[k] and new<ps[k]:
        if k=='MINU Initiate':
          demote_chat_member(chat, user)
        else:
          promote_Chat_Member(chat, user,prev)
        break
      else:
        prev=k

def demote_chat_member(chat_id,user_id):
  url1=URL+'promoteChatMember?chat_id={}&user_id={}&is_anonymous=False&can_manage_chat=False&can_delete_messages=False&can_manage_voice_chats=False&can_restrict_members=False&can_promote_members=False&can_change_info=False&can_invite_users=False&can_pin_messages=False'.format(chat_id,user_id)
  get_url(url1)

    
def decay(date, chat):
  today=datetime.date.today()
  for item in db['Ph']:
    diff=today-datetime.date.fromisoformat(item[2])
    dayss=diff.days
    #print(dayss)
    
    if dayss>=360:
      points_to_deduct=item[1]
      old_points=db['mem'][item[0]][1]
      new_points=old_points-points_to_deduct
      db['mem'][item[0]][1]=new_points
      check_demotion(old_points,new_points,chat,item[0])
      db['Ph'].remove(item)
  #print('break')

def decay2(chat):
    for mem in db['mem']:
        if mem in db['inactive']:
            db['inactive'][mem]+=1
        else:
            db['inactive'][mem]=1
        if db['inactive'][mem]>30:
            db['mem'][mem][1]-=20
            pts=db['mem'][mem][1]
            old_pts=pts+20
            check_demotion(old_pts,pts,chat,mem)
        


def check_uprank(old,new,chat_id,user_name,user_id):
  ps={'MINU Initiate':150,'Senior Initiate':250,'Crewman':400, 'SGT MINU':700, 'Staff SGT MINU':1000, 'Captain':1200, 'Lt. Commander':1500, 'Commander':1700, 'Cpt. Commander':2000, 'Rear Admiral':2599, 'Vice Commander':3000 ,'Commander MINU':2600}
  keyss=list(ps.keys())
  for k in keyss:
    if old<ps[k] and new>=ps[k]:
      send_message('Congratulations '+user_name+', you have ranked up to '+k+',',str(chat_id))
      promote_Chat_Member(chat_id, user_id,k)
      break

def update_rank(chat):
  month=datetime.datetime.now().strftime("%b")
  day=datetime.datetime.now().strftime("%d")
  year=datetime.datetime.now().strftime("%Y")
  send_message('Leaderboard update:\nTop 20 '+month+' '+day+' '+year+'\n' +rankboard(), str(chat))

#stored_placement={}

def rankboard():
  board=''
  rankedlist=[]
  for item in db['mem']:
    if db['mem'][item][1]<2000000000:
      rankedlist.append(db['mem'][item])
  
  rankedlist.sort(key=lambda x: x[1], reverse=True)
  for i in range(len(rankedlist)):
    name=rankedlist[i][0]
    points=rankedlist[i][1]
    rank=check_rank(points)
    if i<20:
      board+=rank+' '+name+' : '+str(points)+change_rank(name,i+1)+'\n'
      db['Prevrank'][name]=i+1
    else:
      db['Prevrank'][name]=100

    

  return board

    
def change_rank(name,new_place):
  if name in db['Prevrank']:
    old_place=db['Prevrank'][name]
    if new_place<old_place:
      return '\u2b06\ufe0f'
    elif new_place>old_place:
      return '\u2b07\ufe0f'
    else:
      return ''
  else:
    return '\u2b06\ufe0f'
    



    
def check_rank(points):
  ps={'MINU Initiate':150,'Senior Initiate':250,'Crewman':400, 'SGT MINU':700, 'Staff SGT MINU':1000, 'Captain':1200, 'Lt. Commander':1500, 'Commander':1700, 'Cpt. Commander':2000, 'Rear Admiral':2599, 'Vice Commander':3000 ,'Commander MINU':2600}
  keyss=ps.keys()
  prev=''
  for item in keyss:
    if points<ps[item]:
      if item=='Cadet':
        return ''
      else:
        return prev
    elif points>ps[item]:
      prev=item
    elif points==ps[item]:
        return item
  if prev=='Admiral':
    return 'Admiral'

def create_default():
  db['mem']={'29325643':['trish',2000000000],'54944873':['Luke',2000000000],'62323009':['Nina',2000000000],'64932241':['Derek',2000000000],'135036697':['Wenjie',2000000000],'464325890':['Jango',2000000000],'749008508':['Varun',2000000000],'2105507722':['FUR-B',2000000000]}
  db['Ph']=[]
  db['Prevrank']={}
  db['inactive']={}

def check_glitch(chat):
  to_go=URL+'getChatAdministrators?chat_id='+str(chat)
  update=get_json_from_url(to_go)
  for x in update['result']:
    if 'custom_title' not in x:
      user=x['user']['id']
      print(user)
      get_url(URL+'setChatAdministratorCustomTitle?chat_id={}&user_id={}&custom_title=Cadet'.format(chat,user))



def main():
  testttt=False
  if 'test' not in db:
    db['test']=1
    testttt=True
  else:
    db['test']=db['test']+1
  if 'inactive' not in db:
    create_default()
  
  if 'rankupdate' not in db:
    db['rankupdate']=True

  last_update_id = None
  while True:
    db['test']=db['test']+1
    try:
      updates = get_updates(last_update_id)
      chat=''
      if len(updates["result"]) > 0:
        last_update_id = get_last_update_id(updates) + 1
        add_points(updates)
        chat=updates['result'][-1]['message']['chat']['id']
        if testttt==True:
          send_message('db reset','749008508')
        datee=datetime.date.today()
        decay(datee, chat)
      hour=datetime.datetime.now().strftime("%H")
      if chat!='':
        if int(hour)>=13 and int(hour)<16 and db['rankupdate']==False and chat!='':
          update_rank(chat)
          check_glitch(chat)
          decay(datee, chat)
          decay2(chat)
          db['rankupdate']= True  
        elif (int(hour)<13 or int(hour)>=16) and db['rankupdate']==True:
          db['rankupdate']= False  

      
      time.sleep(0.5)
    except Exception as e:
      print('errorSHUXXX')
      print(e)
            

if __name__ == '__main__':
  keep_alive.keep_alive()
  main()
  

