from ghrepository import GHRepository
from repositorydataenum import RepositoryData
from view import View


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

test_create_and_get_data_from_repository()
#test_save_interval_from_view()
#test_set_stop_from_view()