from bs4 import BeautifulSoup
import json

def get_urls_from_html(file_name):
    """ This function gets the urls of all websites from home page. """

    with open(file_name, "r") as file:
        strr = file.read()
        soup = BeautifulSoup(strr, "lxml")
    urls = soup.find("select", id="select-country").find_all("option")
    return urls



def get_urls_from_json(file_name):
    """ This function gets the urls of all websites from the json file. """
    with open(file_name, "r") as file:
        urls = json.load(file)
    return urls



def store_urls_in_json(file_name, urls):
    """ This function stores the urls of all websites to a json file. """

    with open(file_name, "w") as file:
        urls_list = []
        for url in urls:
            if url['value'] != "":
                urls_list.append( { "Location" : url.text, "Url": url['value'] } )
        json.dump(urls_list, file)



def store_urls_in_text(file_name, urls):
    """ This function stores the urls of all websites to a text file. """

    with open(file_name, "w") as file:
        for url in urls:
            file.write(f"{url['Location']}                       {url['Url']}\n")