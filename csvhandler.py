import csv

class CsvHandler:

    # Read a csv file in the same folder as the python script and return to user
    def readCsvFile(file_name: str, delimiter: str) -> dict: 
        """
        Reads a file and divides headers and rows into a dictionary
        \n
        Can return a dictionary or None if file did not manage to open. 
        \n
        Make sure to handle None exceptions that may get returned
        """
        header = []
        rows = []

        try:
            file = open(file_name)
        except OSError:
            print("ERROR: Unable to open the file " + file_name)
            return None
        
        csv_reader = csv.reader(file, delimiter = delimiter)

        header = next(csv_reader)
        for row in csv_reader:
            rows.append(row)

        csvDict = {
            "header"    : header,
            "rows"      : rows
        }

        file.close()

        return csvDict


    def createCsvFile(data: dict, wanted_file_name: str) -> str: # returns true if success and return false if error
        """
        Creates a csv file from two lists . Can return 3 different messages. 
            * SUCCESS - If the function excecuted as intended.
            * OPEN_FILE_ERROR - The function did not manage to open the file.
            * WRITE_FILE_ERROR - The function did not manage to write to file.
            \n
        If a call to this function is made try to handle the different errors.
        """
        print("begin writing to file...")
        
        try:
            file = open(wanted_file_name, 'w+')
        except:
            return "OPEN_FILE_ERROR"

        csv_writer = csv.writer(file)

        try: 
            csv_writer.writerow(data["header"])
            csv_writer.writerows(data["rows"])
        except:
            "WRITE_FILE_ERROR"

        file.close()

        print("done!")

        return "SUCCESS"
    