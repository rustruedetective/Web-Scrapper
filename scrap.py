from ScrapperClasses.ScrapperFuncs import scrap_files

db_file = "./DatabaseFile/rows.db"
files_dir = "./Files/scrap"

scrap_files(files_dir, db_file, print_rows=1, store_rows=1)