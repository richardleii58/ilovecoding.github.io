import json
import requests
import time
import urllib
from datetime import datetime, timedelta
import keep_alive
from replit import db
import os

pers_in_charge_mail = 'Neo_yang@defence.gov.sg'
pers_in_charge_name = 'SCT Neo Yang'

TOKEN = os.environ['TOKEN']
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
try:
    with open("response_no.txt", "r") as file:
        x = int(file.read())
except FileNotFoundError:
    with open("response_no.txt", "w") as file:
        file.write("0")
    with open("response_no.txt", "r") as file:
        x = int(file.read())

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
    global x
    with open("response_no.txt", "w") as file:
        x += 1
        file.write(str(x))
    print("responding...")
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=MarkdownV2".format(
        text, chat_id)
    get_url(url)


def send_message2(text, chat_id):
    global x
    with open("response_no.txt", "w") as file:
        x += 1
        file.write(str(x))
    print("responding...")
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def send_message3(text, chat_id, kb):
    global x
    with open("response_no.txt", "w") as file:
        x += 1
        file.write(str(x))
    print("responding...")
    text = urllib.parse.quote_plus(text)
    KB = {'keyboard': [], 'one_time_keyboard': True}
    for item in kb:
        KB['keyboard'].append([{'text': item}])
    #print(KB)
    url = URL + "sendMessage?text={}&chat_id={}&reply_markup={}".format(
        text, chat_id, json.dumps(KB))
    get_url(url)


def send_message4(text, chat_id, kb):
    global x
    with open("response_no.txt", "w") as file:
        x += 1
        file.write(str(x))
    print("responding...")
    text = urllib.parse.quote_plus(text)
    KB = {'keyboard': [], 'one_time_keyboard': True}
    for item in kb:
        KB['keyboard'].append([{'text': item}])
    #print(KB)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=MarkdownV2&reply_markup={}".format(
        text, chat_id, json.dumps(KB))
    get_url(url)


def send_message5(text, chat_id):
    global x
    with open("response_no.txt", "w") as file:
        x += 1
        file.write(str(x))
    print("responding...")
    text = urllib.parse.quote_plus(text)
    kb = {'force_reply': False}
    url = URL + "sendMessage?text={}&chat_id={}&reply_markup={}".format(
        text, chat_id, json.dumps(kb))
    get_url(url)


def send_message6(text, chat_id):
    global x
    with open("response_no.txt", "w") as file:
        x += 1
        file.write(str(x))
    print("responding...")
    text = urllib.parse.quote_plus(text)
    kb = {'force_reply': True}
    url = URL + "sendMessage?text={}&chat_id={}&reply_markup={}".format(
        text, chat_id, json.dumps(kb))
    get_url(url)


def forward_msg(To, From, msg):
    global x
    with open("response_no.txt", "w") as file:
        x += 1
        file.write(str(x))
    print("responding...")
    To = urllib.parse.quote_plus(str(To))
    From = urllib.parse.quote_plus(str(From))
    msg = urllib.parse.quote_plus(str(msg))
    url = URL + "copyMessage?chat_id={}&from_chat_id={}&message_id={}".format(
        To, From, msg)
    print(url)
    get_url(url)

def send_photo(photo, chat_id, cap):
    global x
    with open("response_no.txt", "w") as file:
        x += 1
        file.write(str(x))
    print("responding...")
    photo = urllib.parse.quote_plus(photo)
    url = URL + "sendPhoto?photo={}&chat_id={}&caption={}".format(
        photo, chat_id, cap)
    get_url(url)


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


latest = None

def process(updates):
    for x in updates['result']:
        try:
            if 'message' in x and x['message']['chat']['id'] == db['admin']:
                admin(x)
            else:
                user(x)
        except Exception as e:
            print('errorShux')
            print(e)


def user(x):
    Admin=db['admin']
    months=['Jan','Feb','Mar','Apr','May','Jun',
          'Jul','Aug','Sep','Oct','Nov','Dec','RESET']
    dates=['1','2','3','4','5','6','7','8','9','10',
         '11','12','13','14','15','16','17','18','19','20',
         '21','22','23','24','25','26','27','28','29','30','31','RESET']
    msg=x['message']['text']
    chat=x['message']['from']['id']
    year=db['today'][2]
    if msg=='NEW_ADMIN_CHANGE12345':
        db['admin']=x['message']['chat']['id']
        send_message2('Admin group changed',db['admin'])
    if (str(chat) not in db['users'] and msg not in months) or msg.upper() in "/START":
        send_message3('What month would you like to check the availability for?',chat,months)
        db['users'][str(chat)]={}
        db['users'][str(chat)]['stage']='Input month'
    else:
        if msg.upper()=='RESET':
            db['users'][str(chat)]={}
            db['users'][str(chat)]['stage']='Input month'
            send_message3('What month would you like to check the availability for?',chat,months)
        elif msg in months:
            send_message3('You have selected the month of {}. Which date would you like to book for?'
                          .format(msg),chat,dates)
            if str(chat) not in db['users']:
                db['users'][str(chat)]={}
            db['users'][str(chat)]['stage']='Input date'
            db['users'][str(chat)]['month']=msg
        elif msg in dates and db['users'][str(chat)]['stage']=='Input date':
            db['users'][str(chat)]['stage']='Input time'
            db['users'][str(chat)]['date']=msg
            send_message3('You have selected the date {}. Which time would you like to book for?'
                          .format(msg),chat,['AM','PM','Full','RESET'])
        elif msg in ['AM','PM','Full'] and db['users'][str(chat)]['stage']=='Input time':
            db['users'][str(chat)]['stage']='Input deets'
            db['users'][str(chat)]['time']=msg
            if months.index(db['users'][str(chat)]['month'])+1<int(db['today'][1]) or (months.index(db['users'][str(chat)]['month'])+1==int(db['today'][1]) and int(db['users'][str(chat)]['date'])<int(db['today'][0])):
                year=str(int(year)+1)
                
            
            if db['users'][str(chat)]['month']+db['users'][str(chat)]['date']+year not in db['bookings']:
                send_message6(
                    'Please input meeting details (POC, contact number, meeting title, specific timings etc.) Send "RESET" to restart booking process'
                    ,chat)
            else:
                if msg=='Full':
                    p=db['bookings'][db['users'][str(chat)]['month']+db['users'][str(chat)]['date']+year]
                    if (p['AM']=={}) and (p['PM']=={}):
                            send_message6(
                                'Please input meeting details (POC, contact number, meeting title, specific timings etc.)'
                                ,chat)
            
                    else:
                        if p['AM']!={}:
                            curr_deets=p['AM']['deets']
                            send_message2(
                                'There is already a booking at this date and time. The details are as following:\n\n{}\nDo contact the users directly to request for any changes'
                                .format(curr_deets),chat)
                        if p['PM']!={}:
                            curr_deets=db['bookings'][db['users'][str(chat)]['month']+db['users'][str(chat)]['date']+year]['PM']['deets']
                            send_message2(f'There is already a booking at this date and time. The details are as following:\n\n{curr_deets}\nDo contact the POC directly to request for change and contact {pers_in_charge_name} at {pers_in_charge_mail}  via osn to implement the change',chat)
                        db['users'][str(chat)]['stage']='Input month'
                        send_message3('What month would you like to check the availability for?',chat,months)

                else:
                    if msg=='AM':
                        if db['bookings'][db['users'][str(chat)]['month']+db['users'][str(chat)]['date']+year]['AM']=={}:
                            send_message6(
                                'Please input meeting details (POC, contact number, meeting title, specific timings etc.)'
                                ,chat)
            
                        else:
                            curr_deets=db['bookings'][db['users'][str(chat)]['month']+db['users'][str(chat)]['date']+year]['AM']['deets']
                            send_message2(
                                'There is already a booking at this date and time. The details are as following:\n\n{}\nDo contact the users directly to request for any changes'
                                .format(curr_deets),chat)
                            db['users'][str(chat)]['stage']='Input month'
                            send_message3('What month would you like to check the availability for?',chat,months)
                    else:
                        if db['bookings'][db['users'][str(chat)]['month']+db['users'][str(chat)]['date']+year]['PM']=={}:
                            send_message6(
                                'Please input meeting details (POC, contact number, meeting title, specific timings etc.)'
                                ,chat)
                        else:
                            curr_deets=db['bookings'][db['users'][str(chat)]['month']+db['users'][str(chat)]['date']+year]['PM']['deets']
                            send_message2(
                                'There is already a booking at this date and time. The details are as following:\n\n{}\nDo contact the users directly to request for any changes'
                                .format(curr_deets),chat)
                            db['users'][str(chat)]['stage']='Input month'
                            send_message3('What month would you like to check the availability for?',chat,months)
        elif 'reply_to_message' in x['message'] and x['message']['reply_to_message']['text'][:88]== 'Please input meeting details (POC, contact number, meeting title, specific timings etc.)':
            deets=msg
            time=db['users'][str(chat)]['time']
            month=db['users'][str(chat)]['month']
            date=db['users'][str(chat)]['date']
            if months.index(db['users'][str(chat)]['month'])+1<int(db['today'][1]) or (months.index(db['users'][str(chat)]['month'])+1==int(db['today'][1]) and int(db['users'][str(chat)]['date'])<int(db['today'][0])):
                year=str(int(year)+1)
            bd=month+date+year
            
            if time=='Full':
                db['pending'][bd]={}
                db['pending'][bd]['AM']={'deets':deets,'booker':str(chat)}
                db['pending'][bd]['PM']={'deets':deets,'booker':str(chat)}
                send_message3(f'Your booking has been forwarded to the admins for confirmation. You may make another booking in the meantime.\n\nIf you do not receive a response within 2 working days, or if you need a quick response, please call the following number (63074559) or {pers_in_charge_mail}.',chat,months)
                send_message6('New Booking:\nDate:{} {} {} {}\nDetails:{}\n\nSend "Request" to request further details, or send "Confirm" to confirm the booking, or "Reject" to reject it'.format(date,month,year,time,deets),db['admin'])
            else:
                if bd not in db['pending']:
                    db['pending'][bd]={}
                db['pending'][bd][time]={'deets':deets,'booker':str(chat),'status':'Pending'}
                send_message3(f'Your booking has been forwarded to the admins for confirmation. You may make another booking in the meantime.\n\nIf you do not receive a response within 2 working days, or if you need a quick response, please call the following number (63074559) or {pers_in_charge_mail}.',chat,months)
                send_message6('New Booking:\nDate:{} {} {} {}\nDetails:{}\n\nSend "Request" to request further details, or send "Confirm" to confirm the booking, or "Reject" to reject it'.format(date,month,year,time,deets),db['admin'])
            if 'pending' not in db['users'][str(chat)]:
                db['users'][str(chat)]['pending']=[(bd,time)]
            else:
                db['users'][str(chat)]['pending'].append((bd,time))
            
        elif 'reply_to_message' in x['message'] and x['message']['reply_to_message']['text'][:86]== 'Please include all details (POC, contact number, meeting title, specific timings etc.)':
            replied=x['message']['reply_to_message']['text']
            deets=msg
            counter=replied.split(':')[-1]
            bd=db['editpending'][counter][0]
            time=db['editpending'][counter][1]
            if time=='Full':
                db['pending'][bd]['AM']['deets']=deets
                db['pending'][bd]['PM']['deets']=deets
            else:
                db['pending'][bd][time]['deets']=deets
            send_message3(f'Your booking has been forwarded to the admins for confirmation. You may make another booking in the meantime.\n\nIf you do not receive a response within 2 working days, or if you need a quick response, please call the following number (63074559) or {pers_in_charge_mail}.',chat,months)
            send_message6('New Booking:\nDate:{} {}\nDetails:{}\n\nSend "Request" to request further details, or send "Confirm" to confirm the booking, or "Reject" to reject it'.format(form_date(bd),time,deets),db['admin'])

            



def admin(x):
    months=['Jan','Feb','Mar','Apr','May','Jun',
          'Jul','Aug','Sep','Oct','Nov','Dec']
    msg=x['message']['text']
    chat=x['message']['chat']['id']
    default_buttons=['Cancel booking','Edit details']
    
    if msg=='Cancel booking':
        buttons=[]
        for item in db['bookings']:
            for time in db['bookings'][item]:
                if db['bookings'][item][time] != {}:
                    buttons.append(item+' '+time)
        send_message3('Select a booking to cancel',chat,buttons)
        db['adminStat']='C'
    elif msg=='RESETALL777':
        db['bookings']={}
        db['users']={}
        send_message3('Data reset',chat,default_buttons)
    elif msg=='Edit details':
        buttons=[]
        for item in db['bookings']:
            for time in db['bookings'][item]:
                if db['bookings'][item][time] != {}:
                    buttons.append(item+' '+time)
        send_message3('Select a booking to edit',chat,buttons)
        db['adminStat']='E'

    elif msg[:3] in months and msg[-2:] in ['AM','PM']:
        if db['adminStat']=='C':
            date=msg[:-3]
            time=msg[-2:]
            deets=db['bookings'][date][time]['deets']
            send_message3('Booking date: {}\nDetails: {}\n\nConfirm cancellation?'.format(date+' '+time,deets),chat,['Yes','No'])
            db['adminStat']=['C',date,time]

        elif db['adminStat']=='E':
            date=msg[:-3]
            time=msg[-2:]
            deets=db['bookings'][date][time]['deets']
            send_message6('Booking date: {}\nDetails: {}\n\nEnter new details'.format(date+' '+time,deets),chat)
            db['adminStat']=['E',date,time]

    elif msg in ['Yes','No'] and db['adminStat'][0]=='C':
        if msg == 'Yes':
            date=db['adminStat'][1]
            time=db['adminStat'][2]
            booker=db['bookings'][date][time]['booker']
            db['bookings'][date][time]={}
            send_message2('Your booking for {} {} has been cancelled'.format(form_date(date),time),booker)
            send_message3('Cancellation done! Click a button below',chat,default_buttons)
            db['adminStat']=None
        else:
            db['adminStat']=None
            send_message3('Click a button below',chat,default_buttons)
            

    elif 'reply_to_message' in x['message']:
        replied_to=x['message']['reply_to_message']['text']
        if replied_to[:11]=='New Booking':
            if msg.upper()=='CONFIRM':
                date=replied_to.split(':')[2].strip('\nDetails').split(' ')
                p1=date[1]+date[0]+date[2]
                p2=date[3]
                if p2=='Fu':
                    create(p1,'AM')
                    create(p1,'PM')
                else:
                    create(p1,p2)
            elif msg.upper()[:6]=='REJECT':
                r=msg[6:]
                date=replied_to.split(':')[2].strip('\nDetails').split(' ')
                p1=date[1]+date[0]+date[2]
                p2=date[3]
                if p2=='Fu':
                    reject(p1,'AM',r)
                    reject(p1,'PM',r)
                else:
                    reject(p1,p2,r)

            elif msg.upper()[:7]=='REQUEST':
                date=replied_to.split(':')[2].strip('\nDetails').split(' ')
                p1=date[1]+date[0]+date[2]
                p2=date[3]
                if p2=='Fu':
                    booker=db['pending'][p1]['AM']['booker']
                    p2='Full'
                    send_message6('Please include all details (POC, contact number, meeting title, specific timings etc.) for booking on {} {} \n\nYour previous request was missing the following:'.format(p1,p2)+msg[7:]+'\nref:'+str(db['editcounter']),booker)
                    db['editpending'][str(db['editcounter'])]=[p1,p2]
                    db['editcounter']=db['editcounter']+1
                else:
                    booker=db['pending'][p1][p2]['booker']
                    send_message6('Please include all details (POC, contact number, meeting title, specific timings etc.) for booking on {} {} \n\nYour previous request was missing the following:'.format(p1,p2)+msg[7:]+'\nref:'+str(db['editcounter']),booker)
                    db['editpending'][str(db['editcounter'])]=[p1,p2]
                    db['editcounter']=db['editcounter']+1
                    
                
        elif replied_to[:12]=='Booking date' and db['adminStat'][0]=='E':
            db['bookings'][db['adminStat'][1]][db['adminStat'][2]]['deets']=msg
            db['adminStat']=None
            send_message3('Details edited! Click a button below',chat,default_buttons)
            
            
        
    else:
        send_message3('Click a button below',chat,default_buttons)
        

def reject(date,time,r):
    default_buttons=['Cancel booking','Edit details']
    booker=db['pending'][date][time]['booker']
    send_message3('Sorry, your booking was unsuccessful. Reason: {}'.format(r),booker,['Jan','Feb','Mar','Apr','May','Jun',
          'Jul','Aug','Sep','Oct','Nov','Dec'])
    send_message3('Booking rejected',db['admin'],default_buttons)
    del db['users'][booker]
    del db['pending'][date][time]


def create(date,time):
    default_buttons=['Cancel booking','Edit details']
    details=db['pending'][date][time]['deets']
    booker=db['pending'][date][time]['booker']
    if date not in db['bookings']:
        db['bookings'][date]={'AM':{},'PM':{}}
    db['bookings'][date][time]={'deets':details,'booker':booker}
    send_message3(f'Your booking for {form_date(date)} {time} has been confirmed. To cancel the booking, please call contact SDB office via 63074559 or through {pers_in_charge_mail}.\n\nDisclaimer: Your booking may be subjected to cancellation by SDB at the latest of 5 working days before the booking date in the case that the room is needed for urgent meetings. You will be informed via this bot in the case of any cancellation. Thank you!',booker,['Jan','Feb','Mar','Apr','May','Jun',
          'Jul','Aug','Sep','Oct','Nov','Dec'])
    send_message3('Booking confirmed',db['admin'],default_buttons)
    #print('test1')
    #db['users'][booker]['pending'].remove((date,time))
    #print('test2')
    del db['pending'][date][time]

def daily_update():
    hour=datetime.now().strftime("%H")
    default_buttons=['Cancel booking','Edit details']
    final='Bookings today:\n'
    x=datetime.now()
    if int(hour)==23:
        x=x+timedelta(1)
    w=x.weekday()
    m=str(int(x.strftime('%m')))
    b=x.strftime('%b')
    d=str(int(x.strftime('%d')))
    y=str(int(x.strftime('%Y')))
    db['today']=[d,m,y]
    t=b+d+y
    if t in db['bookings']:
        for time in db['bookings'][t]:
            if db['bookings'][t][time]!={}:
                final+='{}: {}\n'.format(time,db['bookings'][t][time]['deets'])
    if w>4:
        print('None')
    elif final != 'Bookings today:\n':
        send_message3(final,db['admin'],default_buttons)
    else:
        send_message3('No bookings today',db['admin'],default_buttons)
    ytd=x - timedelta(2)
    m=x.strftime('%b')
    d=str(int(x.strftime('%d')))
    y=str(int(x.strftime('%Y')))
    if m+d+y in db['bookings']:
        del db['bookings'][m+d+y]



def form_date(d):
    month=d[:3]
    year=d[-4:]
    date=d[3:-4]
    final=date+' '+month+' '+year
    return final


#def unform_date(d):
    
    

def main():    
    #del db['bookings']
    #del db['pending']
    if 'users' not in db:
        db['users']={}
    if 'bookings' not in db:
        db['bookings']={}
    if 'pending' not in db:
        db['pending']={}
    if 'today' not in db:
        db['today']=['14','8','2022']
    if 'adminStat' not in db:
        db['adminStat']=None
    if 'daily' not in db:
        db['daily']=True
    if 'editpending' not in db:
        db['editpending']={}
    if 'editcounter' not in db:
        db['editcounter']=0
    if 'admin' not in db:
        db['admin']=123
    
    last_update_id = None
    while True:
        try:
            updates = get_updates(last_update_id)
            if len(updates["result"]) > 0:
              last_update_id = get_last_update_id(updates) + 1
              process(updates)

            hour=datetime.now().strftime("%H")

            if (int(hour)==23 or int(hour)<4) and db['daily']==False:
                db['daily']= True
                daily_update()
                  
            elif (int(hour)<23 and int(hour)>=4) and db['daily']==True:
                db['daily']= False  

            time.sleep(3)
        except Exception as e:
            print('errorSHUXXX')
            print(e)
        
if __name__ == '__main__':
    keep_alive.keep_alive()
    # from bookings import data
    # json.dump(data, open("users.json", "w"), indent = 4)
    # from editpending import items
    # with open("db/editpending.json", "w") as file:
    #     json.dump(items, file, indent=4)
  
    # print(db["users"])
    
    main()
