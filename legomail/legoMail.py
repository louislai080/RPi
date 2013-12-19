import RPi.GPIO as GPIO
from threading import Thread
import time, os, subprocess
import LCM1602 as LCM
import gmail

E_Msg_Check_Period = 30 # check if a new message is coming periodically
VoiceMsg_path = './save/recv.wav' # directory where to save attachments 
Unreaded = False	# global falg to check if an unread msg

# Define GPIO to Button PIN connection mapping
BtnGPIO = 4    

def check_msg():

	global Unreaded
	while True:
		print "check message"
		GetMsg = gmail.save_voicemsg(VoiceMsg_path)
		if True == GetMsg:
			LCM.lcd_string(1,"Get new Msg")
			LCM.lcd_string(2,"Play new Msg")

			# play new meesage alarm
			subprocess.call(["aplay", "./res/bicyclebell.wav"])
			Unreaded = True
		else:
			LCM.lcd_string(1,"Wait for Msg")
			if Unreaded:
				LCM.lcd_string(2,"Play new Msg")
			else:
				if not os.path.isfile(VoiceMsg_path) :
					LCM.lcd_string(2,"Msg 0")
				else:
					LCM.lcd_string(2,"Play old Msg")


		time.sleep(E_Msg_Check_Period)

	print "check_msg thread terminate"

def main():
	
	global Unreaded

	LCM.lcd_init()
	LCM.lcd_string(1,"Welcome LEGOMail")
	LCM.lcd_string(2,"")

	mail = Thread(target=check_msg,  args=())
	mail.setDaemon(True)    
	mail.start()

	# start the bttom monitor
	
	GPIO.setup(BtnGPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	while True:
		try:
			GPIO.wait_for_edge(BtnGPIO, GPIO.FALLING) # waiting for falling edge interrupt 
			subprocess.call(["aplay", VoiceMsg_path]) # play the received msg
			LCM.lcd_string(1,"Wait for Msg")
			if Unreaded:
				Unreaded = False
				LCM.lcd_string(2,"Play old Msg")
		except KeyboardInterrupt:
			GPIO.remove_event_detect(BtnGPIO)
			GPIO.cleanup()

	print "main terminate"

if __name__ == '__main__':
  main()
