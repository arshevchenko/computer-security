# -*- coding: utf-8 -*-
import os
import hashlib

class CheckSign(object):

    def __init__(self):
        while True:
            ch_file = raw_input("Введите файл для получение сигнатуры: ")
            self.main_file = self.recreate_path(ch_file)
            if os.path.exists(self.main_file):
                if os.path.isfile(self.main_file):
                    self.main_file = self.get_signature(self.main_file)
                    break
                else:
                    print "Указанный путь не является файлом, попробуйте другой."
            else:
                print "Такого пути не существует, укажите другой."

    # For Unix systems
    def recreate_path(self, f):
        return ("/Users/" + os.getlogin() + "/" + f[2:] if f[:2] == "~/" else f)

    def get_signature(self, path):
        selected_file = open(path, 'rb')        

        return selected_file.read(32)

    def check_directory(self):
            while True:
                ch_dir = raw_input("Введите директорию для проверки: ")
                ch_dir = self.recreate_path(ch_dir)
                if os.path.exists(ch_dir):
                    if os.path.isdir(ch_dir):
                        for pwd, dirs, files in os.walk(ch_dir):
                            for p in files:
                                path = os.path.join(pwd, p)
                                if self.main_file == self.get_signature(path):
                                    print path
                        break
                    else:
                        print "Данный путь не является директорией, попробуйте другой."
                else:
                    print "Такого пути не существует, укажите другой."
