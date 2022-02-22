import sqlite3

from .DataStructures import Row

def create_table(cur):
    """ Creates a table in a db. """

    cur.execute("""CREATE TABLE rows(
                    Cruise_Name text,
                    Cruise_Url text,
                    Date_String text,
                    Price_Person_IntVal text,
                    Price_Person_Symbol text,
                    Nights_IntVal text,
                    Nights_String text,
                    Price_Night_IntVal text,
                    Price_Night_Symbol text,
                    Departure_Name text,
                    Destination_Name text,
                    Route_String text
                    )""")



def insert_row_db(cur, row):
    """ Inserts a row in a db. """

    params = (
        row.row["Cruise"]["Name"],
        row.row["Cruise"]["Url"],
        row.row["Date"]["String"],
        row.row["Price/Person"]["IntVal"],
        row.row["Price/Person"]["Symbol"],
        row.row["Nights"]["IntVal"],
        row.row["Nights"]["String"],
        row.row["Price/Night"]["IntVal"],
        row.row["Price/Night"]["Symbol"],
        row.row["Departure"]["Name"],
        row.row["Destination"]["Name"],
        row.row["Route"]["String"]
    )
    cur.execute("INSERT INTO rows VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params)



def get_rows_db(cur, current_index):
    """ Returns a list of rows from the datbasebased on the offset index (current_index) we provide.
        Fixed length of rows = 100 """

    rows = []
    cur.execute("SELECT * FROM rows ORDER BY Date_String ASC")
    rows_text = cur.fetchmany(100)
    for i in range(current_index):
        rows_text = cur.fetchmany(100)
    for row_text in rows_text:
        if row_text != None:
            row = Row()
            (
                row.row["Cruise"]["Name"],
                row.row["Cruise"]["Url"],
                row.row["Date"]["String"],
                row.row["Price/Person"]["IntVal"],
                row.row["Price/Person"]["Symbol"],
                row.row["Nights"]["IntVal"],
                row.row["Nights"]["String"],
                row.row["Price/Night"]["IntVal"],
                row.row["Price/Night"]["Symbol"],
                row.row["Departure"]["Name"],
                row.row["Destination"]["Name"],
                row.row["Route"]["String"]
            ) = row_text
            rows.append(row)
    return rows



def start_db(file_name):
    """ Starts the db. """

    conn = sqlite3.connect(file_name)
    cur = conn.cursor()
    return (conn, cur)



def close_db(conn):
    """ Closes the db. """

    conn.commit()
    conn.close()



def insert_rows_db(cur, rows_per_page):
    """ Inserts a whole list of rows into the db. """

    for row in rows_per_page:
        insert_row_db(cur, row)
    pass



def create_db(db_file):
    """ Indep. function that creates a db. """
    
    (conn, cur) = start_db(db_file)
    create_table(cur)
    close_db(conn)