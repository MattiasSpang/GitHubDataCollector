from ghrepository import GHRepository
from repositorydataenum import RepositoryData


def test_create_and_get_data_from_repository():
    repo = GHRepository("test/url")

    print("key is ", RepositoryData.NAME.name)
    repo.add_data_by_name(RepositoryData.NAME.name, "first repo")

    print(repo.get_repository_data_by_name(RepositoryData.NAME.name))

test_create_and_get_data_from_repository()
