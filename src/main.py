import os
import shutil

def copy(source, destination):
    if os.path.exists(destination) == True:
        print(f"Formatting {destination}")
        shutil.rmtree(destination)
    os.makedirs(destination, exist_ok=True)
    for entry in os.listdir(source):
        src_path = os.path.join(source, entry)
        dst_path = os.path.join(destination, entry)
        if os.path.isfile(src_path):
            print(f"Copying file:{src_path} to {dst_path}")
            shutil.copy(src_path, dst_path)
        elif os.path.isdir(src_path):
            print(f"Copying dir:{src_path} to {dst_path}")
            os.makedirs(dst_path, exist_ok=True)
            copy(src_path, dst_path)

def main():
    copy("static", "public")

if __name__ == "__main__":
    main()
