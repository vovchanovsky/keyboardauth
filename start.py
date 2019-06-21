import tkinter as tk
from tkinter import messagebox as mb
from math import sqrt
import pickle, time

def write_slogan():
    t1 = tk.Toplevel(root)
    t1.title( u"Enter new passsword")
    t1.geometry("350x100")
    t1.focus_force()
    t1.grab_set()
    message = tk.StringVar()
    temp=['','']
    def cancel():
        t1.destroy()
    def setpwd():
        global matrix
        matrix=[]
        pwd=message.get()
        message_entry.config(disabledbackground="white", disabledforeground="black", state='disabled')
        message_button.destroy()
        rep_message= tk.Label(t1, text="Times left: 15")
        rep_message.place(relx=.5, rely=.5, anchor="c")
        message.set('')
        global Temp, arr, temp_int,m
        Temp,arr,temp_int,m="",[],0,0
        def check():
            global Temp, arr, temp_int, matrix
            if pwd[:len(Temp)+1]!=message.get():
                message.set('')
                Temp,arr,temp_int,m="",[],0,0
            elif(len(Temp) == 0):
                Temp=message.get()
                arr += [int((temp[1]-temp[0])*1000//1)]
                temp_int = temp[1]
            else:
                Temp=message.get()
                arr += [int((temp[0]-temp_int)*1000//1)]+ [int((temp[1]-temp[0])*1000//1)]
                temp_int = temp[1]
            if Temp==pwd:
                matrix += [arr]
                message.set('')
                Temp,arr,temp_int,m="",[],0,0
                tl=15-len(matrix)
                rep_message['text'] = 'Times left: %d' % tl
                if tl==0:
                    with open('entry.pickle','wb') as f:
                        pickle.dump(matrix,f)
                    with open('sysjoin','w') as f:
                        f.write(pwd)
                    mb.showinfo("Success","Password successfully set.")
                    t1.destroy()
        def down(e):
            global m
            if m==0:
                message.set(message.get()+e.char)
                temp[0]=time.time()
                m = 1
        def up(e):
            global m
            if m == 1:
                temp[1]=time.time()
                m = 0
            check()
        t1.bind('<KeyPress>', down)
        t1.bind('<KeyRelease>', up) 
    
    message_entry = tk.Entry(t1,show='*', textvariable=message)
    message_button = tk.Button(t1, text="Confirm", command=setpwd)
    reset_button = tk.Button(t1, text="Cancel", command=cancel)
    message_entry.place(relx=.5, rely=.1, anchor="c")
    message_button.place(relx=.5, rely=.5, anchor="c")
    reset_button.place(relx=.5, rely=.8, anchor="c")

def login():
    with open('sysjoin','r') as f:
        pwd=f.read()
    with open('entry.pickle','rb') as f:
        matrix = pickle.load(f)
    M = []
    for j in range(0,2*len(pwd)-1):
        s = 0
        for i in range(0,10):
            s += matrix[i][j]
        s = s/10
        M = M + [s]
    D = []
    for j in range(0,2*len(pwd)-1):
        s = 0
        for i in range(0,10):
            s += (matrix[i][j]-M[j])*(matrix[i][j]-M[j])
        D += [s/10]
    T_Min,T_Max = [],[]
    for j in range(0,2*len(pwd)-1):
        T_Min += [M[j] - 2.228 * sqrt(D[j])]
        T_Max += [M[j] + 2.228 * sqrt(D[j])]
    Ei = []
    for i in range(10,15):
        ei_ = 0
        for j in range(0,2*len(pwd)-1):
            if not(T_Min[j] < matrix[i][j] < T_Max[j]):
                ei_ += 1
        Ei += [ei_]
    m_wait = 0
    for i in Ei:
        m_wait += i
    m_wait = m_wait/5
    dis = 0
    for i in Ei:
        dis += (i - m_wait)*(i - m_wait)
    dis = dis/5
    e_Max = m_wait + 2.571*sqrt(dis)
    t2 = tk.Toplevel(root)
    t2.title(u"Enter password")
    t2.geometry("350x100")
    t2.focus_force()
    t2.grab_set()
    temp=['','']
    def cancel():
        t2.destroy()
    global Temp, arr, temp_int,m
    Temp,arr,temp_int,m="",[],0,0
    def confirm():
        if Temp==pwd:
            number = 0
            for i in range(0,2*len(pwd)-1):
                if not(T_Min[i] < arr[i] < T_Max[i]):
                    number += 1
            if(number < e_Max):
                mb.showinfo("Success","Welcome, user!")
                t2.destroy()
            else:
                mb.showerror("Error", "Access denied.")
                t2.destroy()
        else:
            mb.showerror("Error", "Access denied.")
            t2.destroy()
    def check():
            global Temp, arr, temp_int, matrix
            if(len(Temp) == 0):
                Temp=message2.get()
                arr += [int((temp[1]-temp[0])*1000//1)]
                temp_int = temp[1]
            else:
                Temp=message2.get()
                arr += [int((temp[0]-temp_int)*1000//1)]+ [int((temp[1]-temp[0])*1000//1)]
                temp_int = temp[1]
    def down(e):
            global m
            if m==0:
                message2.set(message2.get()+e.char)
                temp[0]=time.time()
                m = 1
    def up(e):
        global m
        if m == 1:
            temp[1]=time.time()
            m = 0
            check()
    t2.bind('<KeyPress>', down)
    t2.bind('<KeyRelease>', up)
    message2 = tk.StringVar()
    message_entry = tk.Entry(t2,show='*', textvariable=message2, disabledbackground="white", disabledforeground="black", state='disabled')
    message_button = tk.Button(t2, text="Confirm", command=confirm)
    reset_button = tk.Button(t2, text="Cancel", command=cancel)
    message_entry.place(relx=.5, rely=.1, anchor="c")
    message_button.place(relx=.5, rely=.5, anchor="c")
    reset_button.place(relx=.5, rely=.8, anchor="c")
    
        
root = tk.Tk()
frame = tk.Frame(root)
frame.pack()


learnbutton = tk.Button(frame,
                   text="Learn",
                  fg="red",
                    command=write_slogan)
learnbutton.pack(side=tk.LEFT)
loginbutton = tk.Button(frame,
                   text="Log in",
                  fg="green",
                    command=login)
loginbutton.pack(side=tk.LEFT)
root.title( u"CCTV Control Panel")
root.geometry("350x30")
root.mainloop()

