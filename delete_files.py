
import os
class DeleteFiles:
    def delete_all_files_in_folder(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path) 
    
