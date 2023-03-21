from repositorydataenum import RepositoryData

class GHRepository:
    
    def __init__(self,url: str) -> None:
        self.url : str = url
        self.repository_name : str = ""
        self.data : dict = {}

    def get_name(self) -> str:
        return self.repository_name
    
    def get_url(self) -> str:
        return self.url
    
    def get_repository_data_by_name(self, wanted_data : RepositoryData) -> dict:
        return self.data[wanted_data]

    def get_repository_data(self) -> dict:
        return self.data

    def add_data_by_name(self, name: RepositoryData, data):
        self.data[name] = data

    def toString(self):
        pass

    def to_csv_row(self):
        pass