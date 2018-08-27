import os
import socket
import pickle
import json
import uuid

from Tkinter import *
from random import choice
from string import ascii_letters

create = 1
connect = 2

reload(sys)
sys.setdefaultencoding('utf-8')

def CreateAuthFile(friend_nickname, friend_id, friend_secretkey, your_data, choice):
    data = {"nickname": friend_nickname, "sessionid": friend_id, "secretkey": friend_secretkey}
    print("TEST",data['secretkey'])
    #data = json.loads(data)
    your_data = json.loads(your_data)
    if(choice == 1):
        auth_key = open('auth_key.txt','w')
        auth_key.write(your_data['secretkey'] + data['secretkey'])
        auth_key.close()
        auth_id = open('auth_id.txt','w')
        auth_id.write(your_data['sessionid'] + data['sessionid'])
        auth_id.close()
    else:
        if(choice == 2):
            auth_key = open('auth_key.txt','w')
            auth_key.write(data['secretkey'] + your_data['secretkey'])
            auth_key.close()
            auth_id = open('auth_id.txt','w')
            auth_id.write(data['sessionid'] + your_data['sessionid'])
            auth_id.close()

tk=Tk()

#CodeId.set(uuid.uuid4())
your_key = StringVar()
your_key.set(''.join(choice(ascii_letters) for i in range(16)))
your_id = StringVar()
your_id.set(''.join(choice(ascii_letters) for i in range(12)))
key = StringVar()
key.set('')
uniqid = StringVar()
uniqid.set('')
label_nickname = Label(text = "Your nickname:")
label_key = Label(text = "Your key:")
label_id = Label(text = "Your id:")
label_friend_key = Label(text = "Friend key:")
label_friend_id = Label(text = "Friend id:")
nickname = Entry(tk, textvariable='')
your_sessionid = Entry(tk, textvariable=your_id)
your_secretkey = Entry(tk, textvariable=your_key)
sessionid = Entry(tk, textvariable=uniqid)
secretkey = Entry(tk, textvariable=key)

array_your_auth_data = {"nickname": nickname.get(), "sessionid": your_sessionid.get(), "secretkey": your_secretkey.get()}
array_your_auth_data = json.dumps(array_your_auth_data)

createroom = Button(tk, text = "Create", command=lambda:CreateAuthFile(nickname.get(), sessionid.get(), secretkey.get(), array_your_auth_data, create))

connectroom = Button(tk, text = "Connect", command=lambda:CreateAuthFile(nickname.get(), sessionid.get(), secretkey.get(), array_your_auth_data, connect))

label_nickname.pack()
nickname.pack()
label_key.pack()
your_secretkey.pack()
label_id.pack()
your_sessionid.pack()
label_friend_key.pack()
secretkey.pack()
label_friend_id.pack()
sessionid.pack()
createroom.pack()
connectroom.pack()

tk.mainloop()
