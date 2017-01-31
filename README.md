# Movie recommendation system
This is the Github repository for the 'movie recommendation system' project. This project was a part of the Data Science course on the university of Rotterdam. 
This repository contains the following folders:

- documentation: Contains the documentation for the project (including the fact sheet).

- models: Contains all the algorithms that are used within the application.
    - model_init_login: contains the algorithms that are used to generate movies that users can rate at their initial login.

- db_backup: Contains the backup for the db (create/insert script)

- load_db: Contains the scripts needed to load/process the data (including the scraping of the images/plots of movies).

- unused_algo: Contains the algorithms that were created but weren't
used due to several reasons (e.g. performance).

- application: contains all the files/folders that are used on the web server to run the application. This includes all the PHP, HTML & CSS files. This folder
contains an exact copy of the application. This means that it also includes our
Python scripts. This also means that this script could be implemented on a server any time, given that the server supports the used packages & has the correct database installed (database connection within scripts would have to be
changed)

#Credits
Thanks to Bilal Aarabe, Yoeri Bruchem, Gabriële de la Cruz & Mick van Hulst for the development of this project. 

Note: There is an extra file called 'README.md' in this directory. This file is added because the project is uploaded on Github. Github uses md files (markdown files) as description files for projects.