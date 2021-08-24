# Initialize settings before downloading statements
import time
from datetime import date
import os

copy_pos = [0,500,1000,1500,2000]
text_path = "Texts\\"
data_path = "Data\\"

today = date.today()
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)

def check_dir(dir):
    if os.path.isdir(dir):
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
    else:
        os.mkdir(dir)

for i,pos in enumerate(copy_pos):
    pos_file = f"Ticker Position {i+1}.txt"
    log_file = f"Log {i+1}.txt"

    #Initialize ticker position
    with open(text_path+pos_file,'w') as f:
        f.write(str(pos))
    
    #Create log file
    with open(text_path+log_file,'w') as f:    
        f.write(f"Log created at {current_time} local time on {today}\n")

    #Make directories, delete files presently in them if they already exist
    check_dir(data_path+f"Cashflow{i+1}\\")
    check_dir(data_path+f"Income{i+1}\\")