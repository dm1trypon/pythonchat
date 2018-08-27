# -*- coding: utf-8 -*- 

import os
import socket
import pickle
import json
import uuid

from Crypto.Cipher import XOR
import base64
from Tkinter import *
#from auth import nickname

def encrypt (key, plaintext):
    cipher = XOR.new(key)
    return base64.b64encode(cipher.encrypt(plaintext))

def decrypt (key, ciphertext):
    cipher = XOR.new(key)
    return cipher.decrypt(base64.b64decode(ciphertext))

#Решаем вопрос с кирилицей
reload(sys)
sys.setdefaultencoding('utf-8')
#-----------------------------

tk=Tk()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind(('0.0.0.0',11719))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)

text=StringVar()
name=StringVar()
#CodeId=StringVar()
name.set("nickname")
text.set('')
#CodeId.set(uuid.uuid4())
#ID_SESSION = uuid.uuid4()
tk.title('SuperChat')
tk.geometry('400x300')

log = Text(tk)
nick = Entry(tk, textvariable=name)
msg = Entry(tk, textvariable=text)
msg.pack(side='bottom', fill='x', expand='true')
nick.pack(side='bottom', fill='x', expand='true')
log.pack(side='top', fill='both',expand='true')
nick.config(state = DISABLED)

def verify_id():
    verify_file_id = open('auth_id.txt','r')
    data_verify_file_id = verify_file_id.read()
    verify_file_id.close()
    return data_verify_file_id

def verify_key():
    verify_file_key = open('auth_key.txt','r')
    data_verify_file_key = verify_file_key.read()
    verify_file_key.close()
    return data_verify_file_key

def history_saver(data_saver):
    if os.path.exists('history.txt'):
        data_saver = json.loads(data_saver)
        file_history = open('history.txt','a')
        #pickle.dump(name + ':' + message + ';', file_history)
        file_history.write(data_saver['name'] + ':' + data_saver['message'] + '\n')
        #print(data_saver['name'])
        file_history.close()
    else:
        data_saver = json.loads(data_saver)        
        file_history = open('history.txt','w')    
        #pickle.dump(name + ':' + message + ';', file_history)
        #file_history.write(name + ':' + message + '\n')
        #print(data_saver['name'])
        file_history.write(data_saver['name'] + ':' + data_saver['message'] + '\n')
        file_history.close()

def history_viewer():
    if os.path.exists('history.txt'):
        file_history = open('history.txt','r')
        record = file_history.read()
        file_history.close()
        #record.split(';')
        log.insert(END,record)

def loopproc():
    log.see(END)
    s.setblocking(False)
    try:
        message = s.recv(128)
        #message = decrypt(verify_key(), message)
        message = json.loads(message)
        message['message'] = decrypt(verify_key(), message['message'])
        #print("UUUU:".message)
        if(verify_id() == message['session_id']):
            #history_saver(name_send, text_send)
            log.insert(END, message['name'] + ':' + message['message'] + '\n')
    except:
        tk.after(1,loopproc)
        return
    tk.after(1,loopproc)
    return

def sendproc(event):
    array = {"name": name.get(), "message": text.get(), "session_id": verify_id()}
    #print(verify_id())
    
    history_saver(json.dumps(array))
    array['message'] = encrypt(verify_key(), array['message'])
    array = json.dumps(array)
    print(array)
    sock.sendto (array,('255.255.255.255',11719))
    text.set('')

msg.bind('<Return>',sendproc)

msg.focus_set()
history_viewer()
tk.after(1,loopproc)
tk.mainloop()
