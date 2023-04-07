from datetime import datetime
from random import randint
import os
import fnmatch

class Logger:

    def __init__(self):
      self.log_name: str = ""
      self.log: list = []

    def set_log_file_name(self, name: str):
        self.log_name = name

    def get_log_file_name(self) -> str:
        return self.log_name

    def write_to_log(self, message: str):
        now = str(datetime.now())
        self.log.append("\n" + "Timestamp: " + now + "  : " +message)

    def get_existing_log_files(self) -> list: 
        
        logs = []
        for file_name in os.listdir('./'):
            if fnmatch.fnmatch(file_name, 'log_*'):
                logs.append(file_name)

        return logs

    def get_new_generated_file_name(self) -> str:

        highest_file_id = 0
        for file_name in os.listdir('./'):
            if fnmatch.fnmatch(file_name, 'log_*'):
                file_id = int(file_name[15:-4])

                if highest_file_id < file_id:
                    highest_file_id = file_id

        date = str(datetime.now().date())
        return  "Log_" + str(date) + "_" + str(highest_file_id + 1) + ".txt"

        

    def write_log_to_file(self):
        
        log_file_name = ""

        if self.log_name != "":
            log_file_name = self.log_name
        else:
            log_file_name = self.get_new_generated_file_name()
            
        log_file = open(log_file_name, "w+")
        log_file.writelines(self.log)
        log_file.close()
        print("Wrote to new log file: " + log_file_name)