#%%
import subprocess
import os

def open_work_programs():
    subprocess.call([
        "C:\Program Files\Firefox Developer Edition\\firefox.exe", 
        "google.com",
        "https://web.whatsapp.com/"
        ])
    os.system("C:\\Users\\jeffe\\AppData\\Local\\Microsoft\\Teams\\Update.exe --processStart Teams.exe")
    os.system("C:\\Users\\jeffe\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")


def turn_off():
    os.system('shutdown -s')