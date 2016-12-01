# -*- coding: utf-8 -*-
from base64 import b64encode
from Crypto.Cipher.XOR import XORCipher
from cryptoshop import encryptfile, decryptfile
import MySQLdb
import hashlib
import os

class CheckPermissions(object):
    def __init__(self):
        self.connect = MySQLdb.connect('localhost', 'root', 'E3HKsGhpDeg', 'perm_sys')
        self.cursor = self.connect.cursor()
        self.secret_key = False
        self.path = ""

    # User operations part
    def user_add(self, login, passw):
        passw = hashlib.md5(passw).hexdigest()
        key = b64encode(os.urandom(10)).decode("utf-8")

        self.cursor.execute("""
            INSERT INTO users (login, pass, secret_key)
            VALUES ('%s', '%s', '%s');
        """ % (login, passw, key))
        self.connect.commit()

    def user_remove(self, login):
        self.cursor.execute("""
            DELETE FROM users
            WHERE login = '%s';
        """ % (login))
        self.connect.commit()

    def user_exist(self, login):
        self.cursor.execute("""
            SELECT id FROM users WHERE login = '%s';
        """ % login)
        result = self.cursor.fetchone()[0]
        return True if result else False

    def user_auth(self, login, passw):
        self.cursor.execute("""
            SELECT pass, secret_key  FROM users WHERE login = '%s';
        """ % login)
        result =  self.cursor.fetchone()

        db_passw = result[0]
        passw = hashlib.md5(passw).hexdigest()
        if db_passw == passw:
            self.secret_key = result[1]
            return True
        else:
            return False

    #  File operations part
    def recreate_path(self, f):
        return ("/Users/" + os.getlogin() + "/" + f[2:] if f[:2] == "~/" else f)

    def check_file(self, path):
        self.path = self.recreate_path(path)
        if os.path.exists(self.path):
            if os.path.isfile(self.path):
                self.path_to_file = self.path
                return True
            else:
                print "It's not a file. Please, try another path."
                return False
        else:
            print "This path are not found. Please, try another path."
            return False

    def encode_file(self, path):
        if self.check_file(path):
            result = encryptfile(self.path, self.secret_key, algo="srp")

    def decode_file(self, path):
        if self.check_file(path):
            result = decryptfile(self.path, self.secret_key)

perm = CheckPermissions()

while True:
    print """
        1) Вход в систему
        2) Регистрация нового аккаунта
    """
    check = raw_input("Введите значение пункта: ")
    if check == "1":
        login = raw_input("Введите логин: ")
        while True:
            if perm.user_exist(login):
                passw = raw_input("Введите пароль: ")
                if perm.user_auth(login, passw):
                    print "Вы успешно вошли в систему"
                    print """
                        1) Зашифровать файл
                        2) Расшифровать файл
                    """
                    check = raw_input("Введите значение пункта: ")

                    if check == "1":
                        path = raw_input("Введите путь до файла: ")
                        perm.encode_file(path)

                    elif check == "2":
                        path = raw_input("Введите путь до файла: ")
                        perm.decode_file(path)

                    break
                else:
                    print "Данный пароль введен не корректно, попробуйте ещё"

        break
    elif check == "2":
        login = raw_input("Введите желаемый логин: ")
        passw = raw_input("Введите желаемый пароль: ")
        perm.user_add(login, passw)
        print "Пользователь создан!"
