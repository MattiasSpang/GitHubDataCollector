from enum import Enum

#
# This Enum contains all data that a GitHub Repository can contain. 
# (The enum is used as input in get_repo_data function from GHRepository class)
#
class RepositoryData(Enum):
    NAME = 0
    HAS_GHA = 1
    TOTAL_COMMITS = 2
    MEDIAN_ISSUES_TIME = 3
    MEDIAN_PR_TIME = 4
    NR_OF_CONTRIBUTORS = 6
    NR_OF_STARS = 9
    MAIN_LANGUAGE = 16
    TOTAL_ISSUES = 17
    TOTAL_PR = 19
    CONTRIBUTOR_1 = 20
    CONTRIBUTOR_2 = 21
    CONTRIBUTOR_3 = 22
    CONTRIBUTOR_4 = 23
    CONTRIBUTOR_5 = 24
    CONTRIBUTOR_6 = 25
    CONTRIBUTOR_7 = 26
    CONTRIBUTOR_8 = 27
    CONTRIBUTOR_9 = 28
    CONTRIBUTOR_10 = 29
    CREATED_AT = 30

