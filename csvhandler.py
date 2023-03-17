import csv

class CsvReader:

    # Read a csv file in the same folder as the python script and return to user
    def readCsvFile(fileName: str, delimiter: str) -> dict: 
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
            file = open(fileName)
        except OSError:
            print("ERROR: Unable to open the file " + fileName)
            return None
        
        csvReader = csv.reader(file, delimiter = delimiter)

        header = next(csvReader)
        for row in csvReader:
            rows.append(row)

        csvDict = {
            "header"    : header,
            "rows"      : rows
        }

        file.close()

        return csvDict


    def createCsvFile(data: list, headers: list , wantedFileName: str) -> str: # returns true if success and return false if error
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
            file = open(wantedFileName, 'w+')
        except:
            return "OPEN_FILE_ERROR"

        csvWriter = csv.writer(file)

        try: 
            csvWriter.writerow(data["header"])
            csvWriter.writerows(data["rows"])
        except:
            "WRITE_FILE_ERROR"

        file.close()

        print("done!")

        return "SUCCESS"