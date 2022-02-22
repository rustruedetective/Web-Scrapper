import web
from ScrapperClasses.DBFuncs import get_rows_db, start_db, close_db
from ScrapperClasses.DataStructures import Row

def parse_rows(cur, cur_index):
    rows = get_rows_db(cur, cur_index)
    lis = []
    for row in rows:
        l = [
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
            ]
        lis.append(l)
    return lis


    
class view:
    def GET(self):
        (conn, cur) = start_db(web.config.db_file)
        global current_index
        current_index = 0

        lis = parse_rows(cur, current_index)
        close_db(conn)
        return web.config.ren.index(lis)



class next:
    def GET(self):
        (conn, cur) = start_db(web.config.db_file)
        global current_index
        current_index += 1

        lis = parse_rows(cur, current_index)
        close_db(conn)
        return web.config.ren.index(lis)



class previous:
    def GET(self):
        (conn, cur) = start_db(web.config.db_file)
        global current_index
        if current_index > 0:
            current_index -= 1

        lis = parse_rows(cur, current_index)
        close_db(conn)
        return web.config.ren.index(lis)



class close:
    def GET(self):
        exit(0)