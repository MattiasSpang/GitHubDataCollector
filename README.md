> # GHWebscraper
>
> #### USES: 
>    * Asyncio (A asyncrounus library)
>    * BeautifulSoup (A web scraping library)
>    * csv (Python built in csv handling library)
>    * TKinter (A ui application library)
>
> #### STEPS:
>    1. Listen for user settings input. 
>    2. Gather URLs. 
>    3. Collect HTML from every URL.
>    4. Gather desired data. 
>    5. Wrtie to CSV file. 
>
> #### FILE STRUCTURE: 
>    * Project root folder
>        * View
>        * Controllers
>        * Models
>        * Interfaces
>
> #### CODING NAME CONVENTIONS:
>    * We follow Python Enhancement Proposal (PEP8)
>      https://peps.python.org/pep-0008/
>
> #### DESIGN PATTERN:
>    * MVC (Model, View, Controller)
>
>
>
> #### Example CLASSES, FUNCTIONS AND VARIABLES (More an example than an exact list): 
>    * GHRepository [Class] 
>        * private url [Variable]
>        * private repo_name [Variable]
>        * private has_GHA [Variable]
>        * set_variable [Funciton]
>    * WebScraper [Class] 
>        * main_loop [Function]
