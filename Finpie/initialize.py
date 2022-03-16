# Initialize settings before downloading statements
import time
from datetime import date
import os
from glob import glob

copy_pos = [5,60,120,180]
text_path = "Texts\\"
data_path = "Data\\"

today = date.today()
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)

# #Check if directory exists and delete all files
# def check_dir(dir):
#     if os.path.isdir(dir):
#         for f in os.listdir(dir):
#             os.remove(os.path.join(dir, f))
#     else:
#         os.mkdir(dir)

#----------------Delete old files and folders---------------
fileList = glob(text_path+'Ticker Position *')+glob(text_path+'Log *')
for file in fileList:
    os.remove(file)

dirList = os.listdir(data_path)
for dirName in dirList:
    for c in dirName:
        if c.isdigit():
            os.rmdir(data_path+dirName) # only removes empty directories
            break

# if os.path.isfile(text_path+"Missing Symbols.txt"):
#     os.remove(text_path+"Missing Symbols.txt")

#--------------Create files and folders----------------
for i,pos in enumerate(copy_pos):
    pos_file = f"Ticker Position {i+1}.txt"
    log_file = f"Log {i+1}.txt"

    #Initialize ticker position
    with open(text_path+pos_file,'w') as f:
        f.write(str(pos))
    
    #Create log file
    with open(text_path+log_file,'w') as f:    
        f.write(f"{today} {current_time} local time: log created\n")

    #Make directories
    os.mkdir(data_path+f"Cashflow {i+1}\\")
    os.mkdir(data_path+f"Income {i+1}\\")
