from ghrepository import GHRepository
from repositorydataenum import RepositoryData
from view import View
from csvhandler import CsvHandler


def test_create_and_get_data_from_repository():
    repo = GHRepository("test/url")

    print("key is ", RepositoryData.NAME.name)
    repo.add_data_by_name(RepositoryData.NAME.name, "first repo")

    print(repo.get_repository_data_by_name(RepositoryData.NAME.name))
    
def test_save_interval_from_view():
    print(View.set_save_interval())
    
def test_set_stop_from_view():
    print(View.set_stop())
    
def test_set_start_from_view():
    print(View.set_start())

def test_read_csv_file():
    csv_handler = CsvHandler
    file = csv_handler.readCsvFile("5000csv.csv",";")

    for row in file["rows"]:
        print(row[RepositoryData.NAME.value])
        print(type(row))

def test_create_csv_file():
    data = {"header" : ["htest1","htest2"], "rows" : [["rtest1","rtest2"], ["rtest1.1","rtest1.2"]]}
    ret_msg = CsvHandler.createCsvFile(data=data,wanted_file_name="testcsv.csv")
    print(ret_msg)

#test_create_and_get_data_from_repository()
#test_save_interval_from_view()
#test_set_stop_from_view()
test_create_csv_file()