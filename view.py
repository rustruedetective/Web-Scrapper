import web
from WebClasses.WebFuncs import *

db_file = "./DatabaseFile/rows.db"

current_index = 0
urls = (
    '/', 'view',
    '/next', 'next',
    '/previous', 'previous',
    '/close', 'close'
)
app = web.application(urls, globals())
web.config.update({ 'db_file': db_file })
web.config.update({ 'ren': web.template.render('./templates/') })

if __name__ == "__main__":
    print("Go to this link to view:")
    app.run()