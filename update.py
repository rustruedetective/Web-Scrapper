from UtilClasses.LinkFuncs import get_urls_from_html, get_urls_from_json, store_urls_in_json, store_urls_in_text

html_file = "./Files/index.html"
json_file = "./Files/website_links.json"
text_file = "./Files/website_links.txt"

urls = get_urls_from_html(html_file)
store_urls_in_json(json_file, urls)

urls = get_urls_from_json(json_file)
store_urls_in_text(text_file, urls)