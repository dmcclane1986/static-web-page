from textnode import TextNode, TextType
import shutil
import os

def main():
   # node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
   # print(node)
    destination_path = "public"
    source_path = "static"
    if os.path.exists(destination_path):
        shutil.rmtree(destination_path) 

    os.mkdir(destination_path)
    
    copy_static_files(source_path, destination_path)

def copy_static_files(current_path, destination_path):
    contents = os.listdir(current_path)
    for thing in contents:
        full_source_path = os.path.join(current_path, thing)
        full_dest_path = os.path.join(destination_path, thing)
        if os.path.isfile(full_source_path):
            print(f"Copying file: {full_source_path} to {full_dest_path}")
            shutil.copy(full_source_path, full_dest_path)
        if os.path.isdir(full_source_path):
            os.mkdir(full_dest_path)
            print(f"Creating directory: {full_dest_path}")
            copy_static_files(full_source_path, full_dest_path)
            

if __name__ == "__main__":
    main()