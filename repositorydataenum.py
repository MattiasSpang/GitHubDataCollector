from enum import Enum

#
# This Enum contains all data that a GitHub Repository can contain. 
# (The enum is used as input in get_repo_data function from GHRepository class)
#
class RepositoryData(Enum):
    NAME = 0
    HAS_GHA = 1
    MEDIAN_PR_TIME = 2
    MEDIAN_ISSUES_TIME = 3
    NR_OF_STARS = 12
