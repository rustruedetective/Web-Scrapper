import datetime
from .UtilFuncs import split_alpha_numbers

def conv_date_type1(date_str):
    """ Converts the date string of type 1 webpage into a proper format. """

    date_lis = date_str.split("'")
    year = date_lis[1]
    (month, day) = split_alpha_numbers(date_lis[0])
    date = datetime.datetime.strptime(f'{day} {year}', f"%d %y")
    day = date.day
    if date.day < 10:
        day = "0" + str(date.day)
    return str(f'{date.year}-{month.strip()}-{day}')



def conv_date_type2(date_str):
    """ Converts the date string of type 2 webpage into a proper format. """

    return date_str
    # does not conversion need yet...
    # date = datetime.datetime.strptime(date_str, "%Y-%b-%d")
    # return str(date.date())



def conv_date_type3(date_str):
    """ Converts the date string of type 3 webpage into a proper format. """

    date = datetime.datetime.strptime(date_str, "%d/%m/%Y")
    return str(date.date())



def conv_date_type3_2(date_str):
    """ Converts the date string of 3's 2nd type webpage into a proper format. """

    date = datetime.datetime.strptime(date_str, "%d.%m.%Y")
    return str(date.date())