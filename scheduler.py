import time
import subprocess

def run_task():
    
    subprocess.run(["python", "wallpaper.py"])

if __name__ == "__main__":
    while True:
        run_task()
        # Sleep for 3o minutes
        time.sleep(30*30)
