import csv
import base64
import os
import random
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# key + password + text to encrypt = random text
# random text + key + password  = text toencrypt

def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

if os.path.isfile("key.key"):
    pass
else:
    write_key()

def load_key():
    with open("key.key", "rb") as file:
        key = file.read()
    return key

def write_salt():
    salt = os.urandom(16)
    with open("salt.key", "wb") as salt_file:
        salt_file.write(salt)

if os.path.isfile("key.key"):
    pass
else:
    write_salt()

def load_salt():
    with open("salt.key", "rb") as file:
        salt = file.read()
    return salt

master_pwd = input("What is the master password? ")
master_pwd = master_pwd.encode()
# key = load_key() + master_pwd.encode()
# salt = os.urandom(16)
salt = load_key() + load_salt()
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=390000
)
key = base64.urlsafe_b64encode(kdf.derive(master_pwd))
fer = Fernet(key)


lines = list()
list_index = list()

def view():
    with open("pass_python.txt", 'r') as f:
        for line in f:
            data = line.rstrip()
            user, passw = data.split("|")
            print("User:", user, "\nPassword:", fer.decrypt(passw.encode()).decode(), "\n")

    print()
    

def add():
    name = input("Nama Akun: ")
    pwd = input("password: ")

    with open("pass_python.txt", 'a') as f:
        f.write(name + "|" + fer.encrypt(pwd.encode()).decode() + "\n")

    print()

def generate():
    s = "abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
    ukuran = input('Masukan Panjang Password: ')
    panjang = int(ukuran)
    p = "".join(random.sample(s, panjang))
    name = input("Nama Akun: ")

    with open("pass_python.txt", 'a') as f:
        f.write(name + "|" + fer.encrypt(p.encode()).decode() + "\n")

    print()

def hapus():
    lines.clear()
    list_index.clear()
    hapus_akun = input("Hapus akun atau semua? (akun, semua)\n= ")

    if hapus_akun == "semua":
        with open ("pass_python.txt", 'w') as f:
            f.truncate()
        os.remove('pass_python.txt')
        print("semua data terhapus\n")

    elif hapus_akun == "akun":
        nama_akun = input("Nama Akun atau password: ")
        print("Berikut daftarnya..\n\n")
        
        with open("pass_python.txt", 'r') as f:
            for index, line in enumerate(f.readlines()):
                if nama_akun in line:
                    print("[" + str(index) + "]" + " " + line)
                    list_index.append(index)
        print()
                
        nomor_akun = input("Pilih nomor akun yang akan dihapus atau semua! ([nomor], semua)\n=")
        print()

        if nomor_akun in str(list_index):
            with open("pass_python.txt", 'r') as f:
                reader = csv.reader(f)
                for row_number, row in enumerate(reader):
                    if row_number != int(nomor_akun):
                        for value in row:
                            lines.append(value)
                    
        elif nomor_akun == "semua":
            with open("pass_python.txt", 'r') as f:
                reader = csv.reader(f)
                for row_number, row in enumerate(reader):
                    if row_number not in list_index:
                        for value in row:
                            lines.append(value)
        else:
            print("Salah Mode!\n")

        # print(lines)
        with open("pass_python.txt", 'w') as f:
            for value in lines:
                f.write(value + '\n')
                    
    


while True:
    mode = input("Buat Otomatis, Tambah Password, Lihat daftar atau hapus? (buat, lihat, tambah, hapus)\ntekan q untuk keluar\n\n= ")
    if mode == "q":
        break

    if mode == "lihat":
        view()
    elif mode == "tambah":
        add()
    elif mode == "buat":
        generate()
    elif mode == "hapus":
        hapus()
    else:
        print("salah mode!\n")
        continue