import os
import Client
#from Cryptodome.Cipher import AES
#from Cryptodome.Random import get_random_bytes
import subprocess


class menu_option():
    def __init__(self, key, description, pointer, menu_id = 0):
        self.key = key
        self.description = description
        self.pointer = pointer
        self.menu_id = menu_id



class cryptographer:
    target_ip = None
    target_port = None
    menu_array = []
    path_to_code = "C:\\Users\\neri\\Documents\\Coding\\Python\\Top_portfolio_projects\\Cryptochat\\Crypto.py"

    def logo_printer(self):
        print("[***********************************************************]")
        print("[   _____                  _         _____ _           _    ]")
        print("[  / ____|                | |       / ____| |         | |   ]")
        print("[ | |     _ __ _   _ _ __ | |_ ___ | |    | |__   __ _| |_  ]")
        print("[ | |    | '__| | | | '_ \| __/ _ \| |    | '_ \ / _` | __| ]")
        print("[ | |____| |  | |_| | |_) | || (_) | |____| | | | (_| | |_  ]")
        print("[  \_____|_|   \__, | .__/ \__\___/ \_____|_| |_|\__,_|\__| ]")
        print("[               __/ | |                                     ]")
        print("[              |___/|_|                 BY Neri Carcasci    ]")
        print("[***********************************************************] \n \n \n")

    def show_menu(self, menu_id):
        self.clear_terminal()
        self.logo_printer()
        for i in self.menu_array:
            if i.menu_id == menu_id:
                print(i.key + ") " + i.description)
        choice = input("Choice:")
        return choice

    def run_menu(self, menu_id):
        option = self.show_menu(menu_id)
        for i in self.menu_array:
            if i.menu_id == menu_id and i.key == option:
                print(i.description)
                i.pointer()

    def main_initialiser(self):
        self.run_menu(0)

    def chat_initialiser(self):
        self.run_menu("chat")

    def manual_initialiser(self):
        self.run_menu("manual")

    def get_ip(self):
        try: 
            self.target_ip = input("IP:")

        except:
            print("External error: IP answer invalid")


    def get_port(self):
        try: 
            self.target_port = int(input("PORT:"))

        except:
            print("External error: PORT answer invalid")


    def chat_connect(self):

        if self.target_ip != None and self.target_port != None:
            print("Initialising client")
            try:
                self.client_class = Client.Client("192.168.30.95", self.target_port)
            except:
                print("Internal error: Client failed to start")
        else:
            print("Initialising client with default credentials")
            try:
                self.client_class = Client.Client()
            except:
                print("Internal error: Client failed to start")

        
    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def message_encrypt(self):
        self.run_menu("encrypt_style")

    def shift_encryption(self):
        s = int(input("shift:"))
        text = input("Message:")
        result = ""
        # transverse the plain text
        for i in range(len(text)):
            char = text[i]
            # Encrypt uppercase characters in plain text
            if (char.isupper()):
                result += chr((ord(char) + s - 65) % 26 + 65)
            # Encrypt lowercase characters in plain text
            else:
                result += chr((ord(char) + s - 97) % 26 + 97)
        print(result)

    def split_len(self, seq, length):
        return [seq[i:i + length] for i in range(0, len(seq), length)]


    def columnar_transposition(self, key, plaintext):
        key = input("key:")
        plaintext = input("Message:")
        order = {int(val): num for num, val in enumerate(key)}
        ciphertext = ''
        for index in sorted(order.keys()):
            for part in self.split_len(plaintext, len(key)):
                try:
                    ciphertext += part[order[index]]
                except IndexError:
                    continue

        print(ciphertext)

    def reverse_encryption(self):
        message = input("Message:")
        translated = ''  # cipher text is stored in this variable
        i = len(message) - 1
        while i >= 0:
            translated = translated + message[i]
            i = i - 1
        print(translated)

    def message_decrypt(self, mes):
        #crypt_obj = AES.new("Exe3080kEyMrIa80", AES.MODE_CBC, "16 character vec")
        #try:
            msg_decrypted = crypt_obj.encrypt(mes)
        #except:
            print("Internal error: Incorrect key or unsuitable message supplied")

    def show_source_code(self):
        #subprocess.run(["open", "Crypto.py"], check=True)
        os.startfile(self.path_to_code, 'open')

    def init_menu(self):
        self.menu_array.append(menu_option("1", "Chat", self.chat_initialiser))
        self.menu_array.append(menu_option("2", "Manual Mode", self.manual_initialiser))
        self.menu_array.append(menu_option("3", "Source Code", self.show_source_code))
        self.menu_array.append(menu_option("1", "IP", self.get_ip, "chat"))
        self.menu_array.append(menu_option("2", "PORT", self.get_port, "chat"))
        self.menu_array.append(menu_option("3", "Connect", self.chat_connect, "chat"))
        self.menu_array.append(menu_option("b", "Back", self.main_initialiser, "chat"))
        self.menu_array.append(menu_option("1", "Encrypt", self.message_encrypt, "manual"))
        self.menu_array.append(menu_option("2", "Decrypt", self.message_decrypt, "manual"))
        self.menu_array.append(menu_option("b", "Back", self.main_initialiser, "manual"))
        self.menu_array.append(menu_option("1", "Shift Enryption", self.shift_encryption, "encrypt_style"))
        self.menu_array.append(menu_option("2", "Columnar Transposition", self.columnar_transposition, "encrypt_style"))
        self.menu_array.append(menu_option("3", "Reverse Encryption", self.reverse_encryption, "encrypt_style"))
        self.menu_array.append(menu_option("b", "Back", self.main_initialiser, "encrypt_style"))


    def __init__(self):
        self.init_menu()
        self.main_initialiser()

crypto = cryptographer()

