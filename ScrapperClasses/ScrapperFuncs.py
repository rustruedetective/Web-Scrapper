from datetime import date
from bs4 import BeautifulSoup

from .DataStructures import Row
from .DateConversionFuncs import conv_date_type1, conv_date_type2, conv_date_type3, conv_date_type3_2
from .DBFuncs import close_db, insert_rows_db, start_db, create_db
from .UtilFuncs import has_numbers, split_alpha_numbers
import os
from os.path import exists

""" You can use these functions to get the data out of any type of the 3 webpages """

def get_divs_per_page(soup):
    """ Extracts a list of divs that have data in them and the type of page in a tuple. """

    data = soup.find_all("div", class_="itinerary-card tile tile--result-search")
    if data != []:
        return (data, 1)
    data = soup.findAll("div", {"ng-repeat": "(countMap,catGroupElement) in definitiveResultList"},class_="ng-scope")
    if data != []:
        return (data, 2)
    data = soup.find_all("div", class_="divItinContent content-box")
    if data != []:
        return (data, 3)
    return -1



def parse_type1_div(div):
    """ Extracts data from div of page type 1. """

    # print("Page Type 1 Detected")
    rows_per_div = []
    total_dates = []
    center_dates_div = div.find("div", class_="VueCarousel-slide itinerary-slider__slide VueCarousel-slide-active VueCarousel-slide-center")
    side_dates_div = div.find("div", class_="VueCarousel-slide itinerary-slider__slide")
    
    active_date_center = None
    if center_dates_div != None:
        total_dates = center_dates_div.find_all("div", class_="itinerary-slider__wrapper itinerary-slider__wrapper--small")
        active_date_center = center_dates_div.find("div", class_="itinerary-slider__wrapper itinerary-slider__wrapper--active itinerary-slider__wrapper--small")
    if active_date_center != None:
        total_dates.append(active_date_center)

    active_date_only_one_available = None
    if side_dates_div != None:    
        total_dates += side_dates_div.find_all("div", class_="itinerary-slider__wrapper itinerary-slider__wrapper--small")
        active_date_only_one_available = side_dates_div.find("div", class_="itinerary-slider__wrapper itinerary-slider__wrapper--active")
    if active_date_only_one_available != None:
        total_dates.append(active_date_only_one_available)

    for date in total_dates:
        row = Row()
        row.push_content("Cruise", "Name", div.a.text)
        row.push_content("Cruise", "Url", div.a["href"])
        row.push_content("Date", "String", conv_date_type1( date.find("span", class_="itinerary-slider__date").text ))
        row.push_content("Price/Person", "IntVal", (date.find("div", class_="itinerary-slider__price").find_next("span").find_next("span").text))
        row.push_content("Price/Person", "Symbol", (date.find("div", class_="itinerary-slider__price").find_next("span").text))
        row.push_content("Nights", "IntVal", (div.find("span", class_="itinerary-card-detail__duration").text).split(" ")[0])
        row.push_content("Nights", "String", "")
        row.push_content("Price/Night", "IntVal", "")
        row.push_content("Price/Night", "Symbol", "")
        row.push_content("Departure", "Name", div.find("span", class_="itinerary-card-detail__port-name").text)
        row.push_content("Destination", "Name", div.find("span", class_="itinerary-card-detail__destination").text)
        row.push_content("Route", "String", div.find("span", class_="itinerary-card-detail__destination").text)
        rows_per_div.append(row)
    return rows_per_div



def parse_type2_div(div):
    """ Extracts data from div of page type 2. """

    # print("Page Type 2 Detected")
    rows_per_div = []
    dates_number = [i["id"] for i in div.find_all("span", class_="dayTable ng-binding processed")]
    dates_price = [i.text for i in div.find_all("div", class_="pricecontainer ng-binding processed")]

    symbol = ""
    for i in range(len(dates_price)):
        if "\xa0" in dates_price[i]:
            dates_price[i] = dates_price[i].split("\xa0")
            if has_numbers(dates_price[i][0]):
                symbol = dates_price[i][1]
                dates_price[i] = dates_price[i][0]
            else:
                symbol = dates_price[i][0]
                dates_price[i] = dates_price[i][1]
        else:
            (symbol, dates_price[i]) = split_alpha_numbers(dates_price[i])
            
    for i in range(len(dates_number)):
        div_with_data = div.find_all("div", class_="cr-description-detail")
        row = Row()
        row.push_content("Cruise", "Name", div_with_data[3].text)
        row.push_content("Cruise", "Url", "#")
        row.push_content("Date", "String", dates_number[i])
        row.push_content("Price/Person", "IntVal", conv_date_type2(dates_price[i]))
        row.push_content("Price/Person", "Symbol", symbol)
        row.push_content("Nights", "IntVal", div_with_data[5].text.split(",")[1].split("N")[0].strip())
        row.push_content("Nights", "String", div_with_data[5].text.replace("\n", "").replace(" ", ""))
        row.push_content("Price/Night", "IntVal", "")
        row.push_content("Price/Night", "Symbol", "")
        row.push_content("Departure", "Name", div_with_data[2].text)
        row.push_content("Destination", "Name", "")
        row.push_content("Route", "String", div_with_data[4].text)
        rows_per_div.append(row)
    return rows_per_div



def parse_type3_div(div):
    """ Type 3 webpage has further 2 types of webpages, orange and white. """

    dates = div.find_all("a", class_="btnDep")
    if dates != []:
        return parse_type3Orange_div(div)
    dates = []
    dates = div.find("a", class_="btnMonthClicked")
    if dates != None:
        return parse_type3White_div(div)
    return []



def parse_type3Orange_div(div):
    """ Extracts data from div of page type 3 orange. """
    
    # print("Page Type 3 Orange Detected")
    rows_per_div = []
    for date in div.find_all("a", class_="btnDep"):
        div_with_data = div.find("div", class_="divItinDataSpecial").find_all("span", class_="labelvalue")
        row = Row()
        row.push_content("Cruise", "Name", div_with_data[0].text)
        row.push_content("Cruise", "Url", "#")
        row.push_content("Date", "String", conv_date_type3(date["departuredate"]))
        row.push_content("Price/Person", "IntVal", "")
        row.push_content("Price/Person", "Symbol", "")
        row.push_content("Nights", "IntVal", div_with_data[3].text.split(" ")[2])
        row.push_content("Nights", "String", div_with_data[3].text)
        row.push_content("Price/Night", "IntVal", "")
        row.push_content("Price/Night", "Symbol", "")
        row.push_content("Departure", "Name", div_with_data[2].text)
        row.push_content("Destination", "Name", "")
        row.push_content("Route", "String", div_with_data[1].text)
        rows_per_div.append(row)
    return rows_per_div



def parse_type3White_div(div):
    """ Extracts data from div of page type 3 white. """

    # print("Page Type 3 White Detected")
    rows_per_div = []
    dates = []

    date_clicked = div.find("a", class_="btnMonthClicked")
    dates_BP = div.find_all("a", class_="btnMonthBP")
    dates_Normal = div.find_all("a", class_="btnMonth")

    if date_clicked != None:
        dates.append(date_clicked)
    if dates_BP != []:
        dates += dates_BP
    if dates_Normal != []:
        dates += dates_Normal

    for date in dates:
        date_string = date["departuredate"]
        if "/" in date_string:
            date_string = conv_date_type3( date_string )
        if "." in date_string:
            date_string = conv_date_type3_2( date_string )

        div_with_data = div.find("div", class_="divItinDataSpecial").find_all("span", class_="labelvalue")
        row = Row()
        row.push_content("Cruise", "Name", div_with_data[0].text)
        row.push_content("Cruise", "Url", "#")
        row.push_content("Date", "String", date_string)
        row.push_content("Price/Person", "IntVal", f'{date["itinbestprice"]};{date["maxminitinbestprice"]}' )
        row.push_content("Price/Person", "Symbol", div.find("span", class_="currency").text)
        row.push_content("Nights", "IntVal", div_with_data[3].text.split(" ")[2])
        row.push_content("Nights", "String", div_with_data[3].text)
        row.push_content("Price/Night", "IntVal", "")
        row.push_content("Price/Night", "Symbol", "")
        row.push_content("Departure", "Name", div_with_data[2].text)
        row.push_content("Destination", "Name", "")
        row.push_content("Route", "String", div_with_data[1].text)
        rows_per_div.append(row)
    return rows_per_div



def get_data_from_all_divs(divs, page_type):
    """ Creates a list of rows from the list of divs we provide it. Ofcourse it determines which webpage type
        it is dealing with. """

    if page_type == 1:
        rows_per_page = []
        for div in divs:
            rows_per_div = parse_type1_div(div)
            rows_per_page += rows_per_div
        return rows_per_page
    if page_type == 2:
        rows_per_page = []
        for div in divs:
            rows_per_div = parse_type2_div(div)
            rows_per_page += rows_per_div
        return rows_per_page
    if page_type == 3:
        rows_per_page = []
        for div in divs:
            rows_per_div = parse_type3_div(div)
            rows_per_page += rows_per_div
        return rows_per_page
    return -1



def get_data_per_page(file_name):
    """ Takes a webpage and first determines type of webpage and a list of divs from it. Then takes data
        out of these dives as a list of rows and sends that back. """
        
    tup = get_divs_per_page(BeautifulSoup(open(file_name,"r").read(), "lxml"))
    if tup == -1:
        print("Error Finding Correct Divs")
        return []
    divs = tup[0]
    page_type = tup[1]
    
    rows_per_page = get_data_from_all_divs(divs, page_type)
    if rows_per_page == -1:
        print("Error Extracting Data From Divs")
        return []
    return rows_per_page



def scrap_files(files_dir, db_file, print_rows = 0, store_rows = 0):
    """ Takes in the files that need to be scrapped, then either prints them and/or stores them in the
        Database file. """

    files_to_scrap = list(filter( lambda x: "html" in x, os.listdir(files_dir)))

    if store_rows > 0:
        if not exists(db_file):
            create_db(db_file)
        (conn, cur) = start_db(db_file)
    
    for file in files_to_scrap:
        rows_per_page = get_data_per_page(f"{files_dir}/{file}")

        if print_rows > 0:
            for row in rows_per_page:
                print(f'{file}            |{row.row["Date"]["String"]}')
        if store_rows > 0:
            insert_rows_db(cur, rows_per_page)

    if store_rows > 0:
        close_db(conn)