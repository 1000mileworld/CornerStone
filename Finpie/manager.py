# Launches copies of getStatements.py

import os

os.system('start cmd /K python -c "from getStatements import download; download(1,60)"')
os.system('start cmd /K python -c "from getStatements import download; download(2,120)"')
os.system('start cmd /K python -c "from getStatements import download; download(3,180)"')
os.system('start cmd /K python -c "from getStatements import download; download(4,258)"')
#os.system('start cmd /K python getStatements_single.py')
