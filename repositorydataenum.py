from enum import Enum

#
# This Enum contains all data that a GitHub Repository can contain. 
# (The enum is used as input in get_repo_data function from GHRepository class)
#
class RepositoryData(Enum):
    NAME = 0
    HAS_GHA = 1
    NR_OF_STARS = 12
