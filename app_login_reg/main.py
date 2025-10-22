import tkinter as tk
import json
import os

def login_user(email, password, login):
    with open("users.json", "r") as file:
        users = json.load(file)

    user = False
    p = False

    for u in users:
        if u["email"] == email and u["password"] == password:
            user = True
            p = True
        elif u["email"] == email and u["password"] != password:
            user = True
            p = False

    label_message_login = tk.Label(login, text="AAA")

    if user == True and p == True:
        label_message_login.config(text=f"Accesso effettuato come {email}", fg="green")
    elif user == True and p == False:
        label_message_login.config(text=f"Password errata per questo account!", fg="red")
    else:
        label_message_login.config(text=f"l'account {email} non esiste!", fg="red")
    
    label_message_login.pack()
    login.after(3000, label_message_login.destroy)

def reopen_registration(login):
    login.destroy()
    registrazione()
    
def login_window(window):
    login = tk.Tk()
    login.geometry("500x500")
    login.title("Login")

    window.destroy()

    label_log_email = tk.Label(login, text="Inserire email")
    label_log_email.pack()

    input_log_email = tk.Entry(login)
    input_log_email.pack()

    label_log_password = tk.Label(login, text="Inserire Password")
    label_log_password.pack()

    input_log_password = tk.Entry(login, show="*")
    input_log_password.pack()

    button_login = tk.Button(login, text="Accedi ora!", command=lambda: login_user(input_log_email.get(), input_log_password.get(), login))
    button_login.pack()

    button_reg = tk.Button(login, text="Non sei ancora registrato? fallo ora!", command=lambda: reopen_registration(login))
    button_reg.pack()

class Users:
    _users = []

    def __init__(self, name, surname, email, password):
        self.name = name or ""
        self.surname = surname or ""
        self.email = email or ""
        self.password = password or ""

        self.reload_all_users()
        
        user = {
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "password": self.password
        }

        if not any(u["email"] == self.email for u in Users._users):
            Users._users.append(user)

        self.save_users_on_file()

    def save_users_on_file(self):
        with open("users.json", "w") as file:
            json.dump(Users._users, file, indent=4)

    def reload_all_users(self):
        Users._users = []
        with open("users.json", "r") as file:
            if os.path.exists("users.json") and os.path.getsize("users.json") > 7:
                Users._users.extend(json.load(file))

def crea_utente(nome, cognome, email, password, window, input_name, input_surname, input_email, input_password):
    label_message = tk.Label(window, text="message")
    try:
        exist_already = False

        Users._users = []
        if os.path.exists("users.json") and os.path.getsize("users.json") > 0:
            with open("users.json", "r") as file:
                Users._users.extend(json.load(file))
        
        if any(u["email"] == email for u in Users._users):
            exist_already = True

        if nome != "" and cognome != "" and email != "" and "@" in email and "." in email and password != "" and exist_already == False:
            new_user = Users(nome, cognome, email, password)
            label_message.config(text="L'utente è stato creato con successo!", fg="green")
            label_message.pack()
            window.after(3000, label_message.destroy)
            input_name.delete(0, tk.END)
            input_surname.delete(0, tk.END)
            input_email.delete(0, tk.END)
            input_password.delete(0, tk.END)
        elif nome == "":
            label_message.config(text="Si prega di inserire il nome!", fg="red")
            label_message.pack()
            window.after(3000, label_message.destroy)
        elif cognome == "":
            label_message.config(text="Si prega di inserire il cognome!", fg="red")
            label_message.pack()
            window.after(3000, label_message.destroy)
        elif email == "":
            label_message.config(text="Si prega di inserire la email!", fg="red")
            label_message.pack()
            window.after(3000, label_message.destroy)
        elif "@" not in email or "." not in email:
            label_message.config(text="Si prega di inserire una email valida!", fg="red")
            label_message.pack()
        elif password == "":
            label_message.config(text="Si prega di inserire la password!", fg="red")
            label_message.pack()
            window.after(3000, label_message.destroy)
            window.after(3000, label_message.destroy)
        elif exist_already == True:
            label_message.config(text="Esiste già un account con questa email!", fg="red")
            label_message.pack()
            window.after(3000, label_message.destroy)
    except:
        label_message.config(text="Non siamo riusciti a creare l'utente :(")
        label_message.pack()
        window.after(3000, label_message.destroy)
        input_name.delete(0, tk.END)
        input_surname.delete(0, tk.END)
        input_email.delete(0, tk.END)
        input_password.delete(0, tk.END)

def registrazione():
    window = tk.Tk()
    window.geometry("500x500")
    window.title("Registrazione")

    title_label = tk.Label(window, text="Registra oggi il tuo utente!")
    title_label.pack()

    label_name = tk.Label(window, text="Inserisci il tuo nome")
    label_name.pack()

    input_name = tk.Entry(window)
    input_name.pack()

    label_surname = tk.Label(window, text="Inserisci il tuo cognome")
    label_surname.pack()

    input_surname = tk.Entry(window)
    input_surname.pack()

    label_email = tk.Label(window, text="Inserisci la tua email")
    label_email.pack()

    input_email = tk.Entry(window)
    input_email.pack()

    label_password = tk.Label(window, text="Inserisci la tua password")
    label_password.pack()

    input_password = tk.Entry(window, show="*")
    input_password.pack()

    bottone_registrazione = tk.Button(window, text="Registrati ora", pady=5, command=lambda: crea_utente(input_name.get(), input_surname.get(), input_email.get(), input_password.get(), window, input_name, input_surname, input_email, input_password))
    bottone_registrazione.pack()

    bottone_login = tk.Button(window, text="Sei già registrato? accedi da qui!", command=lambda: login_window(window))
    bottone_login.pack()

    window.mainloop()

registrazione()