"""
    The row structure contains all fields for a particular ship.
"""

class Row:
    """ The dictionary contains Data Keys: Cruise, Date..etc
        Each of the inner dictionary keys are called Content Keys: Content, Url.. """

    def __init__(self):
                    #DATA KEYS        CONTENT KEYS
        self.row = {
                    "Cruise"      : {"Name"   : "", 
                                     "Url"    : ""},
                    "Date"        : {"String" : ""},
                    "Price/Person" : {"IntVal" : "0" ,
                                     "Symbol" : ""},
                    "Nights"      : {"IntVal" : "0",
                                     "String" : ""},
                    "Price/Night"  : {"IntVal" : "0"  ,
                                     "Symbol" : ""},
                    "Departure"   : {"Name"   : ""},
                    "Destination" : {"Name"   : ""},
                    "Route"       : {"String" : ""}
                }



    def push_content(self, data_key, content_key, content):
        """ Inserts values in the row dictionary. """

        self.row[data_key][content_key] = content



    def data_keys(self):
        """ Get all the data keys used in the row. """

        lis = []
        for data_key in self.row:
            lis.append(data_key)
        return lis



    def content_keys(self, data_key):
        """ Get all the content keys used in the row. """

        lis = []
        for content_key in self.row[data_key]:
            lis.append(content_key)
        return lis



    def view_row(self):
        """ Prints the row. """
        
        row_str = ""
        for data_key in self.row:
            row_str += data_key + ": "
            for content_key in self.row[data_key]:
                row_str += content_key + "( " + self.row[data_key][content_key] + " ) "
            row_str += "\n"
        row_str += "--------"
        print(row_str)