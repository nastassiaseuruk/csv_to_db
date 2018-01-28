# csv_to_db
This script is written to add definite data from csv-file to database(postgres) and return it in sorted view(by company and title) in pdf-file.

## Getting started
For correct work of script you need Python 2.7 installed on your PC, as well as some additional Python modules listed in requirements.txt. 
You can install them using pip
```
pip install -r requirements.txt
```

## Example
For running script you should run it in console. After you should give the path to you csv-file
```
nastassia@Nastassia-2519:~/PycharmProjects/CVS_to_DB$ ./csv_to_db.py
Please enter a path to csv file: /home/nastassia/PycharmProjects/CSV_to_DB/Book1.csv

```
_Please note that you should have internet connection as well, as script assumes that in csv file links to photo are taken from the internet._