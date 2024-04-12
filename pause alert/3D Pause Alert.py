# Libraries
# pip install bitstring==3.1.9
# pip install requests
# pip install lifxlan
# pip install keyboard


import requests
from lifxlan import LifxLAN
import winsound
import sys
import time
import song
import keyboard

def main():
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

        while True:
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
                time.sleep(30)               

            if keyboard.is_pressed('esc'):
                break # finish loop

            

    except Exception as e:
        print(f"An error occurred: {e}")

def lifxBulbLocate():
  
    num_lights = None
    if len(sys.argv) != 2:
        print("\nDiscovery will go much faster if you provide the number of lights on your LAN:")
        print("  python {} <number of lights on LAN>\n".format(sys.argv[0]))
    else:
        num_lights = int(sys.argv[1])

    # instantiate LifxLAN client, num_lights may be None (unknown).
    # In fact, you don't need to provide LifxLAN with the number of bulbs at all.
    # lifx = LifxLAN() works just as well. Knowing the number of bulbs in advance
    # simply makes initial bulb discovery faster.
    print("Discovering lights...")
    lifx = LifxLAN(num_lights)

    # get devices
    devices = lifx.get_devices()
    print("\nFound {} light(s):\n".format(len(devices)))
    for d in devices:
        try:
        	print(d)
        except Exception as e:
            print(f"An error occurred: {e}")

# Call the main function
if __name__ == "__main__":
    main()
    #lifxBulbLocate()