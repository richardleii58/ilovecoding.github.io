import json
import requests
import time
import urllib
import datetime
import keep_alive
from replit import db

TOKEN = "7413805457:AAH4Gi41ECmrjIONUf2ZtN-hzRZCEul9G74"
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
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=MarkdownV2".format(
        text, chat_id)
    get_url(url)


def send_message2(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def send_photo(photo, chat_id, cap):
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


def admin(x):
    if 'photo' in x['message']:
        file_id = x['message']['photo'][0]['file_id']
        if 'caption' in x['message']:
            cap = x['message']['caption']
        else:
            cap = ''
        if cap[:9] == 'Broadcast':
            for user in db['user']:
                send_photo(file_id, user[0], '🔊 ' + cap[9:])
            send_message("Announcement Sent", -758984080)
    msg = x['message']['text']
    if msg[:9] == 'Broadcast':
        to_send = msg[9:]
        for user in db['user']:
            send_message2('🔊 ' + to_send, user[0])
        send_message2("Announcement Sent", -758984080)
    if msg[:3] == 'New':
        items = msg.split(';')
        num = 1
        while 'Q' + str(num) in db['qns']:
            num += 1
        db['qns']['Q' + str(num)] = {'KW': [], 'Q': items[1], 'A': items[2]}
        send_message2('Qn added' + ' num ' + str(num),
                      x['message']['chat']['id'])
    elif msg == 'List everything':
        send_message2(print_qns(), x['message']['chat']['id'])
    elif msg == 'List questions':
        send_message(list_everything(), x['message']['chat']['id'])
    elif msg[:6] == 'AddKey':
        msg = msg.upper()
        items = msg.split(';')
        lst = items[2].split(',')
        db['qns'][items[1]]['KW'].extend(lst)
        send_message('Keyword added', x['message']['chat']['id'])
    elif msg[:6] == 'AddCat':
        lst = msg.split(';')
        qn = lst[1]
        cat = lst[2]
        if cat in db['cat']:
            if qn not in db['cat'][cat]:
                db['cat'][cat].append(qn)
                send_message2('Question ' + qn + ' added to category ' + cat,
                              -758984080)
            else:
                send_message2('Question already in category', -719645844)
        else:
            db['cat'][cat] = [qn]
            send_message2('Question ' + qn + ' added to category ' + cat,
                          -758984080)

    elif msg[:3] == 'Del':
        items = msg.split(';')
        del db['qns'][items[1]]
        send_message('QnA deleted', x['message']['chat']['id'])
    elif 'reply_to_message' in x['message']:
        #print('A')
        reply = x['message']['reply_to_message']['text']
        #print('B')
        if reply[:3].upper() == 'NEW' and msg[:5].upper() == 'REPLY':
            #print('C')
            reply = reply.split(';;')
            #print('D')
            chat = reply[1]
            qnn = reply[0].split('from')[0]
            #print('E')
            qn_list = []
            #print(kw_input)
            for item in db['qns']:
                for word in db['qns'][item]['KW']:
                    if word.upper() in msg.upper():
                        qn_list.append(item)
            qn_list = list(set(qn_list))
            msg_send = ''
            qn_list.sort()
            for qnnn in qn_list:
                ques = db['qns'][qnnn]['Q']
                msg_send += '*' + qnnn + ':* ' + ques + '\n\n'
            if msg_send != '':
                msg_send = '\n\n*Additionally, here are some related questions you may find useful:*\n\n' + msg_send
                msg_send += 'Type \<_Question\#_\> for the solution\!'
            send_message(
                '*You asked an earlier question and here\'s a possible solution:*\n\nQ:'
                + qnn[3:] + '\n\nA:' + msg[5:] + msg_send, int(chat))
            send_message('Reply sent', -719645844)

    else:
        Instructions = '-Start message with "New" to add new QnA, followed by Qn and Ans separated by semi-colon eg. "New,How To Add,Like this"\n-Send "List everything" to show all qns and ans\n-Send "List questions" to show all qns\n-Start with "AddKey" to add a keyword to a question, followed by the Qn number and Keyword separated by semi-colon eg."AddKey,Q1,Keyword"\n-Start with "Del" to delete a qn followed by the Qn number after a semi-colon eg. "Del,Q1"\n-Start with "AddCat" to add a qn to category followed by qn number and category separated by semi-colons'
        if msg.upper() == 'HELP':
            send_message2(Instructions, x['message']['chat']['id'])
    #send_message(print_qns(),x['message']['chat']['id'])



def check_expiry(chat):
  today=datetime.date.today()
  for user in db['user']:
    if user[0]==chat:
      diff=today-datetime.date.fromisoformat(user[1])
      dayss=diff.days

      if dayss >= 365:
        db['user'].remove(user)

def print_qns():
    final = ''
    for item in db['qns']:
        final += item + 'KW:' + str(
            db['qns'][item]['KW']) + '\n Q:' + db['qns'][item]['Q'] + '\n\n'
    return final


def process(updates):
    for x in updates['result']:
        try:
            if 'message' in x and x['message']['chat']['id'] == -758984080:
                admin(x)
            else:
                msg = x['message']['text']
                chat = x['message']['chat']['id']
                if 'first_name' in x['message']['from']:
                    name = x['message']['from']['first_name']
                else:
                    name = 'Anon'
                tod = datetime.date.today().isoformat()
                if [chat, tod] not in db['user']:
                    db['user'].append([chat, tod])
                else:
                    check_expiry(chat)
                user(msg, chat, name)

                default_instructions = ''
                #send_message(default_instructions, chat)

        except Exception as e:
            print('errorShux')
            print(e)


def list_everything():
    all = list(db['qns'].keys())
    final = ''
    for x in db['cat']:
        final += '\n*' + x + '\:*\n\n'
        for qn in db['cat'][x]:
            if qn in db['qns']:
                final += qn + '\: ' + db['qns'][qn]['Q'] + '\n'
                if qn in all:
                    all.remove(qn)
    if all != []:
        final += '\n*Others*\:\n\n'
        for item in all:
            final += item + '\: ' + db['qns'][item]['Q'] + '\n'

    return final


def user(msg, chat, name):
    keyss = db['qns'].keys()
    #print(msg)
    if msg[0] == 'q' and msg[1].isdigit():
        msg = 'Q' + msg[1:]
    if msg.upper() in keyss:
        qn = db['qns'][msg]['Q']
        ans = db['qns'][msg]['A']
        send_message2(qn + ': ' + ans + '\n\n', chat)
    elif msg[:3].upper() == 'NEW':
        send_message(msg + ' from ' + name + ';;' + str(chat), -758984080)
        send_message(
            'Your question has been forwarded to the admins and they will get back to you via this chat',
            chat)
    elif msg.isdigit() and int(msg) <= len(db['qns']):
        msg = 'Q' + msg
        qn = db['qns'][msg]['Q']
        ans = db['qns'][msg]['A']
        send_message2(qn + ': ' + ans + '\n\n', chat)
    elif msg.upper() == 'ALL':
        send_message(list_everything(), chat)
    elif msg.upper() == '/START':
        send_message(
            'Hi\! I’m *Tristan*\, your ScubeHelper bot\.\n\nAsk me a question\!🧐\nEg\. \"How to upload equpment\"',
            chat)
    else:
        #Instructions='Instructions'
        Instructions = '*No such keyword found\!* 😢 Please type\:\n\n“_all_" to list our question bank\; or\n\n“_new \<question\>_” and our Admin will get back to you\!'
        qn_list = []
        #print(kw_input)
        for item in db['qns']:
            for word in db['qns'][item]['KW']:
                if word.upper() in msg.upper():
                    qn_list.append(item)
        qn_list = list(set(qn_list))
        msg_send = ''
        msg_send2 = ''
        qn_list.sort()
        for qnn in qn_list:
            ques = db['qns'][qnn]['Q']
            msg_send += '*' + qnn + ': *' + ques + '\n\n'
        if msg_send == '':
            msg_send = Instructions
        if msg_send != Instructions:
            msg_send = '*Here are some related questions based on your query\:*\n\n' + msg_send
            msg_send += 'Type \<_Qn No\._\> for the solution\!\nEg\. \"Q1"\n\n'
            msg_send2 = '*If nothing matches your question\,*\ntype:\n\n"_all_" to list our question bank\; or\n\n"_new \<question\>_" and our admins will get back to you'
        send_message(msg_send, chat)
        if msg_send2 != '':
            send_message(msg_send2, chat)


def main():
    global db
    db={}
    print(db)
    if db =={}:
        db={}
        if 'qns' not in db:
            db['qns'] = {}
            db['qns']['Q1'] = {'KW': ['Test123'], 'Q': 'How to do', 'A': 'Just Do'}
            db['track'] = 1
        if 'cat' not in db:
            db['cat'] = {}
        if 'user' not in db:
            db['user'] = []
        last_update_id = None
        while True:
            try:
                updates = get_updates(last_update_id)
                if len(updates["result"]) > 0:
                    last_update_id = get_last_update_id(updates) + 1
                    process(updates)
    
                time.sleep(0.5)
            except Exception as e:
                print('errorSHUXXX')
                print(e)


if __name__ == '__main__':
    keep_alive.keep_alive()
    main()
