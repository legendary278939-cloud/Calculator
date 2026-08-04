import json
import os
import tkinter as tk
from tkinter import messagebox
root=tk.Tk()
FILE_NAME="Cal_history.json"
history_list=[]
root.geometry("360x600")
root.title("Advanced Calculator")
root.resizable(False,False)
entry=tk.Entry(root,font=("Arial",25),justify="right")
entry.grid(row=0,column=0,columnspan=4,padx=0,pady=0)
history_box=tk.Text(root,height=5,width=20,font=("Arial",14))
history_box.grid(row=5,column=0,columnspan=4,padx=10,pady=10)
is_dark_mode=False
def toggle_theme():
    global is_dark_mode
    if is_dark_mode:
        root.config(bg="white")
        entry.config(bg="white",fg="black",insertbackground="black")
        history_box.config(bg="white",fg="black")
        theme_btn.config(text="Light Mode",bg="white",fg="royalblue")
    else:
        root.config(bg="#1e1e1e")
        entry.config(bg="#1e1e1e",fg="white",insertbackground="white")
        history_box.config(bg="#a0a0a0",fg="white")
        theme_btn.config(text="Dark Mode",bg="#a0a0a0",fg="white")
    is_dark_mode=not is_dark_mode

def save_data():
    try:
        with open(FILE_NAME,"w") as file:
           json.dump(history_list,file)
    except Exception as e:
       messagebox.showerror("Error",f"Failed to save calculator history: {e}")

def load_data():
    global history_list
    if os.path.exists(FILE_NAME):
       try:
           with open(FILE_NAME,"r") as file:
              history_list=json.load(file)
           history_box.delete("1.0",tk.END)
           for calculation in history_list:
               history_box.insert(tk.END,calculation)
       except FileNotFoundError:
        history_list=[]
   
    
def click(value):
    entry.insert(tk.END,value)
    
def click(key):
    text=entry.get()
    entry.delete(0,tk.END)
    entry.insert(0,str(text) + str(key))
    
def clear():
    entry.delete(0,tk.END)
    
def clear_history():
    history_list.clear()
    history_box.delete("1.0",tk.END)
    save_data()
    
def backspace():
    text=entry.get()
    entry.delete(0,tk.END)
    entry.insert(0,text[:-1])
    
def equal(event=None):
    try:
        text=entry.get()
        if "%" in text:
            new_text=""
            for i,char in enumerate(text):
                if char=="%":
                    if i+1<len(text) and text[i+1].isdigit():
                        new_text+="/100*"
                    else:
                        new_text+="/100"
                else:
                    new_text+=char
            text=new_text
        result=round(eval(text),4)
        entry.delete(0,tk.END)
        entry.insert(0,result)
        calulation=f"{text}={result}\n"
        history_list.append(calulation)
        history_box.insert(tk.END,calulation)
        save_data()
    except Exception:
        entry.delete(0,tk.END)
        entry.insert(0,"Error")
        
def key_pressed(event):
    key=event.char
    if key in "0123456789-+/*%.":
        click(key)
    elif key in ("\r","\n"):
        equal()
    elif key == "\x08":
        backspace()
    elif key.lower()=="c":
        clear()
    return "break"
    
entry.bind("<Key>",key_pressed)
theme_btn=tk.Button(root,text="Light Mode",font=("Arial",14),command=toggle_theme)
theme_btn.grid(row=2,column=0,columnspan=4,sticky="ew",padx=10,pady=10)
buttons=[("7",6,0),("8",6,1),("9",6,2),("*",6,3),
("4",7,0),("5",7,1),("6",7,2),("-",7,3),
("1",8,0),("2",8,1),("3",8,2),("+",8,3),
("C",9,0),("0",9,1),("x",9,2),("/",9,3),
("=",10,0),("%",10,1)]
for text,row,col in buttons:
    if text=="=":
        action=equal
    elif text=="C":
        action=clear
    elif text=="x":
        action=backspace
    else:
        action=lambda value=text: click(value)
    btn=tk.Button(root,text=text,font=("Arial",14),command=action)
    btn.grid(row=row,column=col,padx=2,pady=2)
    history_btn=tk.Button(root,text="Clear history",font=("Arial",14),command=clear_history)
    history_btn.grid(row=11,column=1,columnspan=3,padx=5,pady=5)
load_data()    
root.mainloop()
