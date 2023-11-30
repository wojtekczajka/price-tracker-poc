from PIL import Image  
import os

IMAGE_SIZE = (500, 500)

def delete_files_in_directory(directory_path):
    try:
        files = os.listdir(directory_path)
        for file in files:
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
    except OSError:
        print("Error occurred while deleting files.")

source_directory = "./product_images"
target_directory = "./product_images_resize"

delete_files_in_directory(target_directory)

for file in os.listdir(source_directory):
     filename = os.fsdecode(file)
     if filename.endswith(".jpg") or filename.endswith(".png"): 
        image = Image.open(source_directory +  "/" + filename)
        image = image.resize(IMAGE_SIZE)  
        image.save(target_directory + "/" + filename) 
     else:
         print("Unsupported file format: " + filename)
         continue