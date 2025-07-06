import subprocess
import sys
import os

# Absolute path to your music_login.py
script_path = os.path.join(os.path.dirname(__file__), "music_login.py")

# Check if the file exists
if not os.path.exists(script_path):
    print(f"ERROR: Cannot find 'music_login.py' at:\n{script_path}")
else:
    subprocess.run([sys.executable, script_path])

