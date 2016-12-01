# -*- coding: cp1251 -*-
import os, random, struct, hashlib, time
from Crypto.Cipher import AES
import sqlite3
import atexit

class MyDatabase:
    root_folder = ''
    dbase_name = ''
    dbase_root = ''
    users_root = ''
    path_to_db =''

    def __init__(self, folder_name ,dbase_name):
        self.create_root_folder(folder_name)
        self.create_database(dbase_name)

    def create_database(self, name):
        name_with_ext = name + '.db'
        self.path_to_db = os.path.join(self.dbase_root, name_with_ext)
        if not os.path.isfile(self.path_to_db):
            con = sqlite3.connect(self.path_to_db)
            cur = con.cursor()
            cur.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, '
                             'login VARCHAR(100), '
                             'password VARCHAR(100), '
                             'rank INTEGER,'
                             'key VARCHAR(2))')
            con.commit()
            con.close()

    def add_user(self, username, password, rank = 0):
        con = sqlite3.connect(self.path_to_db)
        cur = con.cursor()

        password = hashlib.sha256(password).digest()
        secret_key = os.urandom(16)
        cur.execute("INSERT INTO users (login, password, rank, key) VALUES ('{uname}', '{passw}', '{rnk}', '{sec_key}')".
                     format(uname=username, passw=password, rnk = rank, sec_key = secret_key))
        con.commit()
        con.close()
        self.create_user_folder(username)


    def count_users(self):
        con = sqlite3.connect(self.path_to_db)
        cur = con.execute('SELECT COUNT(*) FROM users')
        con.commit()
        ret = cur.fetchone()[0]
        con.close()
        return ret

    def user_exist(self, username):
        con = sqlite3.connect(self.path_to_db)
        cur = con.execute("SELECT COUNT(*) FROM users WHERE login = '{uname}'".format(uname = username))
        con.commit()
        ret = cur.fetchone()[0]
        con.close()
        if ret == 0:
            return False
        elif ret == 1:
            return True
        else:
            return False

    def create_root_folder(self, folder_name):
        # path_to_script = os.path.dirname(os.path.abspath(__file__))
        path_to_script = '/Users/EvShevalie/Documents/'

        # print(path_to_script)
        self.root_folder =  os.path.join(path_to_script, folder_name)
        print(self.root_folder)
        self.dbase_root = os.path.join(self.root_folder,'database')
        self.users_root = os.path.join(self.root_folder,'users')
        if not os.path.exists(self.root_folder):
            os.mkdir(self.root_folder)
        if not os.path.exists(self.dbase_root):
            os.mkdir(self.dbase_root)
        if not os.path.exists(self.users_root):
            os.mkdir(self.users_root)

    def create_user_folder(self, username):
        user_path = os.path.join(self.users_root, username)
        if not os.path.exists(user_path):
            os.mkdir(user_path)


    def encrypt_file(self, key, in_filename, out_filename=None, chunksize=64*1024):
        if not out_filename:
            out_filename = in_filename + '.enc'

        iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        filesize = os.path.getsize(in_filename)

        with open(in_filename, 'rb') as infile:
            with open(out_filename, 'wb') as outfile:
                outfile.write(struct.pack('<Q', filesize))
                outfile.write(iv)

                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += ' ' * (16 - len(chunk) % 16)

                    outfile.write(encryptor.encrypt(chunk))

    def decrypt_file(self, key, in_filename, out_filename=None, chunksize=24*1024):
        if not out_filename:
            out_filename = os.path.splitext(in_filename)[0]

        with open(in_filename, 'rb') as infile:
            origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
            iv = infile.read(16)
            decryptor = AES.new(key, AES.MODE_CBC, iv)

            with open(out_filename, 'wb') as outfile:
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    outfile.write(decryptor.decrypt(chunk))
                outfile.truncate(origsize)

    def check_credentials(self, username, password):
        if self.user_exist(username):
            con = sqlite3.connect(self.path_to_db)
            con.text_factory = str
            cur = con.execute("SELECT password FROM users WHERE login = '{uname}'".format(uname = username))
            con.commit()
            pwd = cur.fetchone()[0]
            con.close()
            if pwd == hashlib.sha256(password).digest():
                return True
            else:
                return False
        else:
            return False

    def encrypt_user_folder(self, username):
        if self.user_exist(username):
            user_folder = os.path.join(self.users_root, username)
            con = sqlite3.connect(self.path_to_db)
            con.text_factory = str
            cur = con.execute("SELECT key FROM users WHERE login = '{uname}'".format(uname = username))
            con.commit()
            key = cur.fetchone()[0]
            con.close()
            tree = os.walk(user_folder)
            for d, dirs, files in tree:
                # ������������� ��� ����� �� ���� ������������
                for f in files:
                    path = os.path.join(d, f)
                    if path[-4:] != '.enc':
                        self.encrypt_file(key,path)
                        os.remove(path)

    def decrypt_user_folder(self, username):
        if self.user_exist(username):
            user_folder = os.path.join(self.users_root, username)
            con = sqlite3.connect(self.path_to_db)
            con.text_factory = str
            cur = con.execute("SELECT key FROM users WHERE login = '{uname}'".format(uname = username))
            con.commit()
            key = cur.fetchone()[0]
            con.close()
            tree = os.walk(user_folder)
            for d, dirs, files in tree:
                for f in files:
                    path = os.path.join(d, f)
                    if path[-4:] == '.enc':
                        self.decrypt_file(key,path)
                        os.remove(path)


if __name__ == '__main__':
    db = MyDatabase('test_folder','permissions')


    action = raw_input('''
    Выберите действие:
     1. Войти в систему
     2. Создать новый аккаунт
    ''')
    if (action == '1'):
        login = raw_input("Введите логин: ")
        password = raw_input("Введите пароль: ")
        if db.check_credentials(login, password):
            print("Вы успешно вошли!")
            db.decrypt_user_folder(login)

            raw_input("Нажмите Enter для того, чтобы вновь скрыть все данные.")
            db.encrypt_user_folder(login)
            exit()
        else:
            print("Логин или пароль не верны, попробуйте ещё раз.")

    elif (action == '2'):
        rank = 0
        login = raw_input("Введите желаемый логин : ")
        if db.user_exist(login):
            print("Данный пользователь уже существует!")
            exit()
        password = raw_input("Введите пароль: ")
        re_password = raw_input("Повторно введите пароль: ")

        if password != re_password:
            print("Пароли не совпадают!")
            exit()
        else:
            if not db.user_exist(login):
                db.add_user(login, password, rank)
                print("Новый пользователь успешно создан!")
        pass
