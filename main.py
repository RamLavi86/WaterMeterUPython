# Complete project details: https://RandomNerdTutorials.com/micropython-send-emails-esp32-esp826/
# Micropython lib to send emails: https://github.com/shawwwn/uMail
import umail
import network
import machine
import network
import time
import urequests

# Define LED pin
led_pin = 2  # GPIO 2 (built-in LED on most ESP32 boards)

# Configure LED pin as output
led = machine.Pin(led_pin, machine.Pin.OUT)

# Email details
sender_email = 'ramlavipushnotification@gmail.com'
sender_name = 'Water meter' #sender name
sender_app_password = 'xwzzrkqzerhwbpgo'
recipient_email = 'lavi.ram86@gmail.com'
email_subject = 'Test Email'
email_content = 'Test content'

# Wifi details
ssid = 'Lavi-Mesh'
password = '0528200151'

# Connect to Wi-Fi
def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print("Wi-Fi connected!")
    print("IP address:", wlan.ifconfig()[0])

def send_mail(sender_email, sender_app_password, recipient_email, sender_name, email_subject, email_content):
    # Send the email
    smtp = umail.SMTP('smtp.gmail.com', 465, ssl=True) # Gmail's SSL port
    smtp.login(sender_email, sender_app_password)
    smtp.to(recipient_email)
    smtp.write("From:" + sender_name + "<"+ sender_email+">\n")
    smtp.write("Subject:" + email_subject + "\n")
    smtp.write(email_content)
    smtp.send()
    smtp.quit()

def get_current_hour():
    # URL of the API providing time information
    api_url = "http://worldtimeapi.org/api/timezone/Asia/Jerusalem"
    
    try:
        # Send a GET request to the API
        response = urequests.get(api_url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            
            # Extract the hour from the time data
            hour = int(data['datetime'][11:13])
            
            # Return the hour (0-23)
            return hour
        
        else:
            print("Failed to fetch time data. Status code:", response.status_code)
            return None
    
    except Exception as e:
        print("An error occurred:", e)
        return None

while True:
    print('start main')
    current_hour = get_current_hour()
    if current_hour is not None:
        print(f'Current hour is: {current_hour}')
    # Check Wi-Fi connection
    if network.WLAN(network.STA_IF).isconnected():
        # Wi-Fi connected, turn on LED2
        led.on()
    else:
        # Wi-Fi not connected, turn off LED2 and reconnect
        led.off()
        connect_to_wifi(ssid, password)
    
    # Delay for a short period (e.g., 1 second)
    time.sleep(1)

