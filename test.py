from check_pendrive import check_drives
import time

while True:
	drives = check_drives()
	print("Detected drives:", drives)
	time.sleep(3)
