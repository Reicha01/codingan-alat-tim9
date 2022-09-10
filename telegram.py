import RPi.GPIO as GPIO
import time as t
import math

# IMPORT THIS FOR MESSAGING
import telepot
from telepot.loop import MessageLoop
# END OF MESSAGING IMPORT

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

a = t.time()

GPIO.setup(21,GPIO.IN)
#this was the setup

telur = 0
total = 0
telurlewat = False
printing = True

# #START of messaging setup
def action(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    print ('Received: %s' %command)
    
    if '/start' in command:
        message = "Selamat Datang di SMACIHO"+ '\n' +'\n' + "/StockTelur : Telur yang tersedia hari ini" + '\n' + "/Beli : Membeli Telur"
        telegram_bot.sendMessage (chat_id, message)

    if '/StockTelur' in command:
        message = "Total telur hari Ini: "+str(total)
        telegram_bot.sendMessage (chat_id, message)

    if '/Beli' in command:
        message = "/1kg" + '\n' + "/2kg" 
        telegram_bot.sendMessage (chat_id, message)
        
    if '/1kg' in command:
        message = "Terimakasih telah membeli di Toko kami. Barang segera kami siapkan" + '\n' + "/Kembali"
        telegram_bot.sendMessage (chat_id, message)
        
    if '/1kg' in command:
        message = "/Kembali"
        telegram_bot.sendMessage (chat_id, message)
        
    if '/2kg' in command:
        message = "Terimakasih telah membeli di Toko kami. Barang segera kami siapkan" 
        telegram_bot.sendMessage (chat_id, message)
        
    if '/2kg' in command:
        message = "JIka membeli lebih dari 2kg"
        telegram_bot.sendMessage (chat_id, message)
        
    if '/2kg' in command:
        message = "Silahkan Datang Ke Toko Kami atau Hubungi No.Tlpn : 085749529416"
        telegram_bot.sendMessage (chat_id, message)
        
    if '/2kg' in command:
        message = "/Kembali"
        telegram_bot.sendMessage (chat_id, message)
        
    if '/Kembali' in command:
        message = "/start"
        telegram_bot.sendMessage (chat_id, message)
        
        
telegram_bot = telepot.Bot('5400067695:AAEVOE_3ROtsuLvmLVY0CVR1goyBrG0D9RM')
print (telegram_bot.getMe())
MessageLoop(telegram_bot, action).run_as_thread()
print ('Mulai Menghitung')

# END OF MESSAGING SETUP

while True:
    sensor=GPIO.input(21)
    if (sensor==1) and (telurlewat==False):
        telur = telur+1
        total = total + 1
        print("lewat"+str(telur))
        telurlewat = True
    elif(sensor==0 and telurlewat==True):
        telurlewat = False
        t.sleep(2)
        #print("GAK ENEK NG PROGRAM")
     
    b = t.time()
    c = (b - a)
    itv = c % 2 #rubah kelipatan disini
    intItv = math.floor(itv)
    if(intItv==0 and printing):
        #action disini
        print("lewat "+str(telur))
        print("total "+str(total))
        telur = 0
        #print(math.floor(c))
        printing = False
    elif(intItv != 0 and not printing) :
        printing = True
