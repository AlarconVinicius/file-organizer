import os 
import shutil
from datetime import datetime

class FileOrganizer:
    file_extensions = ['jpg', 'jpeg', 'png', 'JPG', 'JPEG', 'PNG', 'txt', 'pdf', 'doc', 'docx', 'csv', 'xls', 'xlsx', 'ppt', 'pptx', 'mp4']

    def folder_path_from_file_date(self, file):
        date = self.file_modification_date(file)
        return date.strftime('%Y') + '/' + date.strftime('%Y-%m') + '/' + date.strftime('%Y-%m-%d')

    def file_modification_date(self, file):
        date = datetime.fromtimestamp(os.path.getmtime(file))
        return date
        
    def move_file(self, file):
        path_date = self.folder_path_from_file_date(file)
        new_folder = os.path.join(os.path.dirname(file), path_date)
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)
        
        shutil.move(file, os.path.join(new_folder, os.path.basename(file)))

    def organize(self):
        for foldername, _, filenames in os.walk('.'):
            for ext in set(self.file_extensions):
                ext_files = [os.path.join(foldername, filename) for filename in filenames if filename.endswith(ext)]
                if ext_files:
                    for file in ext_files:
                        self.move_file(file)

FO = FileOrganizer()
FO.organize()