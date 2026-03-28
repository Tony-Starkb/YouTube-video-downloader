import os

#print(os.name)
#print(os.getcwd())

#print(os.chdir("D:\\DSA"))
#print(os.getcwd())

#files = os.listdir()
#print(files)

#print(os.path.exists("I:\\"))

#path = os.path.join("E:\\", "myfile.txt")
#print(path)


def check_drives():

	drives = []
	
	for drive in range(65, 91):
		drive_letter = chr(drive) + ":\\"

		if os.path.exists(drive_letter):
			drives.append(drive_letter)

	return drives
