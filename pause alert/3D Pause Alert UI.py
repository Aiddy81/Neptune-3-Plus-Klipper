# Libraries
# pip install bitstring==3.1.9
# pip install requests
# pip install lifxlan
# pip install keyboard
# pip install tkinter
# pip install cryptography


# python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
# $env:ENCRYPTION_KEY="your_key_here"

#First, run this command to generate a Fernet key:
#
#python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
#
#This will print a new Fernet key to the console. Copy this key.
#
#Then, set the ENCRYPTION_KEY environment variable to the key you just copied:
#
#$env:ENCRYPTION_KEY="your_key_here"
# setx ENCRYPTION_KEY "your_value" -> sets it perminently
#
#Replace "your_key_here" with the key you copied.
#
#Now, the ENCRYPTION_KEY environment variable is set to your Fernet key for the current session. You can use it in your Python script with os.environ.get('ENCRYPTION_KEY').
#
#Please note that this will only set the environment variable for the current session. If you close and reopen PowerShell, you’ll need to set the environment variable again. If you want to set it permanently, you’ll need to use the System Properties dialog or a tool like setx.

# set and load
# $env:ENCRYPTION_KEY ="your_value"; python your_script.py


import requests
from lifxlan import LifxLAN
import winsound
import sys
import time
import song
import keyboard
import tkinter as tk
from tkinter import messagebox
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64
import configparser
import os
import threading

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        print(os.environ.get('ENCRYPTION_KEY'))
        if os.environ.get('ENCRYPTION_KEY'):
            self.key = self.derive_key(os.environ.get('ENCRYPTION_KEY').encode(), b"salt")  # Get key from environment variable
        else:
            print("No secret key found, please set the environment variable ENCRYPTION_KEY")
        
        self.create_widgets()
        self.load_config()

        self.loop_running = threading.Event()

    def derive_key(self, password, salt, iterations=100000):
        backend = default_backend()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=iterations,
            backend=backend
        )
        return kdf.derive(password)  # Removed base64 encoding

    
    def encrypt(self, message: str) -> str:
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(message.encode()) + padder.finalize()
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), default_backend())
        encryptor = cipher.encryptor()
        ct = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(iv + ct).decode('utf-8')

    def decrypt(self, token: str) -> str:
        data = base64.b64decode(token)
        iv = data[:16]
        ct = data[16:]
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), default_backend())
        decryptor = cipher.decryptor()
        result = decryptor.update(ct) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(result) + unpadder.finalize()

    def create_widgets(self):
        self.bot_token_label = tk.Label(self, text="Bot Token")
        self.bot_token_label.pack(padx=10, pady=10)
        self.bot_token_entry = tk.Entry(self)
        self.bot_token_entry.pack(padx=10, pady=10)

        self.bot_name_label = tk.Label(self, text="Bot Name")
        self.bot_name_label.pack(padx=10, pady=10)
        self.bot_name_entry = tk.Entry(self)
        self.bot_name_entry.pack(padx=10, pady=10)

        self.klipper_api_key_label = tk.Label(self, text="Klipper API Key")
        self.klipper_api_key_label.pack(padx=10, pady=10)
        self.klipper_api_key_entry = tk.Entry(self)
        self.klipper_api_key_entry.pack(padx=10, pady=10)

        self.start_button = tk.Button(self, text="Start", command=self.start_loop_in_thread)
        self.start_button.pack(side="left", padx=10, pady=10)

        self.stop_button = tk.Button(self, text="Stop", command=self.stop_loop)
        self.stop_button.pack(side="right", padx=10, pady=10)

        self.save_button = tk.Button(self, text="Save Config", command=self.save_config)
        self.save_button.pack(side="bottom", padx=10, pady=10)

    def start_loop_in_thread(self):
        self.loop_running.set()
        t2 = threading.Thread(target=self.start_loop).start()

    def start_loop(self):
        try:
            # Connect to Moonraker API
            moonraker_url = "http://192.168.2.21:7126/api/job"  # Replace with your Moonraker address and port
            response = requests.get(moonraker_url)
            data = response.json()
            

            # Connect to LIFX light
            lifx = LifxLAN(3)  # Replace with the number of LIFX lights you have
            lights = lifx.get_lights()
            #Select a particular light by its label
            #Replace 'Your Light Label' with the actual label of your light
            #selected_light = next((light for light in lights if light.get_label() == 'Laser Light'), None)
            for light in lights:
                if light.get_label() == 'Laser Light':
                    selected_light = light
                else:
                    selected_light = False
                
                if light.get_label() == 'Adrian Room Light':
                    selected_light2 = light  
                else:
                    selected_light2 = False

            while self.loop_running.is_set():
                #print("in loop")
                # Check if print has a paused or m600 status
                if data['state'] in ['Paused', 'm600']:
                    song.play() # plays the song.py

                    # Turn on the light and make it red
                    if selected_light.get_power() == 0:
                        selected_light.set_power("on")
                        selected_light.set_color((65535, 65535, 65535, 3500), rapid=True)  # Red color

                    if selected_light2.get_power() == 0:    
                        selected_light2.set_power("on")

                    # Replace 'YOUR_BOT_TOKEN' with your actual Telegram bot token
                    # Replace 'YOUR_CHAT_ID' with your actual Telegram chat ID
                    bot_token = 'YOUR_BOT_TOKEN'
                    chat_id = 'YOUR_CHAT_ID'
                    message = 'Print Paused or Filament Change'

                    # Construct the API URL
                    api_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

                    # Send the message
                    response = requests.post(api_url, data={'chat_id': chat_id, 'text': message})

                    # Print the response
                    print(response.json())
                else:
                    if selected_light:
                        if selected_light.get_power() > 0:
                            selected_light.set_power("off")
                    print("Print is not paused or in M600 state\n")
                    print("State: ", data['state'])
                    time.sleep(1)

                #if keyboard.is_pressed('esc'):
                    #break
                    #stop_loop()
                    

                

        except Exception as e:
            print(f"An error occurred: {e}")

    def stop_loop(self):
        self.loop_running.clear()
        messagebox.showinfo("Info", "Loop stopped")
        #self.save_config()
         # finish loop
       

    def save_config(self):
        try:
            bot_token = self.bot_token_entry.get()
            bot_name = self.bot_name_entry.get()
            klipper_api_key = self.klipper_api_key_entry.get()
            print(f"Saving: BotToken={bot_token}, BotName={bot_name}, KlipperApiKey={klipper_api_key}")  # Debug print

            config = configparser.ConfigParser()
            config['DEFAULT'] = {'BotToken': self.encrypt(bot_token),
                                 'BotName': self.encrypt(bot_name),
                                 'KlipperApiKey': self.encrypt(klipper_api_key)}

            # Write the configuration to a file
            with open('/config.ini', 'w') as configfile:
                config.write(configfile)

        except Exception as e:
            print(f"An error occurred: {e}")

    def load_config(self):
        if os.path.exists('config.ini'):
            config = configparser.ConfigParser()
            config.read('config.ini')
            # Check if config file is empty
            if config.defaults():
                bot_token = config['DEFAULT']['BotToken']
                bot_name = config['DEFAULT']['BotName']
                klipper_api_key = config['DEFAULT']['KlipperApiKey']
                if not bot_token and bot_name and klipper_api_key:
                    self.bot_token_entry.insert(0, self.decrypt(bot_token))
                    self.bot_name_entry.insert(0, self.decrypt(bot_name))
                    self.klipper_api_key_entry.insert(0, self.decrypt(klipper_api_key))

    



root = tk.Tk()
root.geometry("800x600")  # Width x Height

app = Application(master=root)
#app.mainloop()
# Create threads
t1 = threading.Thread(app.mainloop())

