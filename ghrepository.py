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

    def set_url(self, url: str):
        self.url = url

    def to_csv_row(self):
        csv_row = []
        csv_row.append(self.url)
        csv_row.append(self.data[RepositoryData.HAS_GHA.name])
        csv_row.append(self.data[RepositoryData.MEDIAN_PR_TIME.name])
        csv_row.append(self.data[RepositoryData.TOTAL_PR.name])
        csv_row.append(self.data[RepositoryData.MEDIAN_ISSUES_TIME.name])
        csv_row.append(self.data[RepositoryData.TOTAL_ISSUES.name])
        csv_row.append(self.data[RepositoryData.NR_OF_CONTRIBUTORS.name])
        csv_row.append(self.data[RepositoryData.NR_OF_STARS.name])
        csv_row.append(self.data[RepositoryData.MAIN_LANGUAGE.name])

        
        for value in range(1,10):
            
            contributor_name = "CONTRIBUTOR_" + str(value)
            try:
                csv_row.append(self.data[contributor_name])
            except:
                print("ERROR: URL: " + self.url + "  CONTRIBUTOR_NAME: " + contributor_name)
                csv_row.append("name error")

        return csv_row