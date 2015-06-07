import tornado.options
import tornado.httpserver
import tornado.ioloop
import tornado.web
import logging
import os.path
import tornado.database
import re

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="database host")
define("mysql_database", default="recipe", help="database name")
define("mysql_user", default="ai", help="database user")
define("mysql_password", default="ai", help="database password")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/home/(.*)",WebHandler),
            (r"/login",UserLoginHandler),
            (r"/registration",RegistrationHandler),
            (r"/logout",LogoutHandler)
        ]
        settings = dict(
            app_title=u"Recipe Planner",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            #xsrf_cookies=False,
            cookie_secret="11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/"            
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        
        self.db = tornado.database.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if user_json:
            return tornado.escape.json_decode(user_json)
        else:
            return None

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")

class HomeHandler(BaseHandler):
    def get(self):
        print "website started"
        self.render("index.html")


class WebHandler(BaseHandler):
    def get(self,page):
        print "rendering ",page
        self.render(page)
    def post(self,page):
        print "rendering ",page
        self.render(page)

class RegistrationHandler(BaseHandler):
    def post(self):
        print "sending data to database"
        username = self.get_argument('username')
        email = self.get_argument('email')
        password = self.get_argument('password')
        print "username ",username
        print "email ", email
        print "password ",password
        uname = self.db.query("SELECT * FROM users WHERE name = %s",username)
        if not uname:
            self.db.execute("INSERT INTO users (name,email,password)" " VALUES (%s,%s,%s)",username, email, password)
            logging.info("inserted successfully")
            self.set_current_user(username)
            self.write("Registration successful")
        else:
            logging.info("User already exists.Log in to continue")
            self.write("User already exists.Log in to continue")
            self.redirect("/home/log-in.html")

class UserLoginHandler(BaseHandler):
    def post(self):
        oauth = self.get_argument('oauth')
        if oauth == "yes":
            print "oauth, login"
            email = self.get_argument('email')
            # argument = {}
            # argument['user'] = email
            print "email",email
            argument = email
            self.finish(dict(argument=argument))
            #self.render("profile.html",argument=argument)
            return
        else:
            email = self.get_argument('uname')
            password = self.get_argument('password')
            print "email ",email
            print "password ",password
            query = self.db.query("SELECT password FROM users WHERE name = %s or email = %s",email,email)
            if not query:
                logging.info("user not present")
                #self.set_current_user(username)
                self.redirect("/home/register.html")
            else:
                logging.info("done")
                argument = email
                self.render("profile.html",argument=argument)

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        print "logout successful"
        self.redirect("/home/log-in.html")
        

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
