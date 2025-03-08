import sys
import shutil
import os

if __name__ == "__main__":
    full_path = sys.argv[1]
    
    dest = "C:\\Users\\freeh\\AppData\\Local\\Rusted_Moss\\mods\\rmml\\rm_mod.md" 
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copyfile(full_path, dest)
