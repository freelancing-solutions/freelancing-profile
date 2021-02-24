
class Metatags():
    """
        Default Application Meta Tags
    """
    title = ""
    description = ""
    twitter_title = ""
    twitter_description = ""
    og_title = ""
    og_description = ""
    page = ""
    path = ""
    image_filename = ""
    image_alt = ""

    def __init__(self, title=None, twitter_title=None, og_title=None, description=None, twitter_description=None,
                 og_description=None, page=None,path=None, image_filename=None, image_alt=None):
        self.title = title
        self.twitter_title = twitter_title
        self.og_title = og_title
        self.description = description
        self.twitter_description = twitter_description
        self.og_description = og_description
        self.page = page
        self.path = path
        self.image_filename = image_filename
        self.image_alt = image_alt

    def set_home(self):
        self.title = "Professional & Freelance Profile of Justice Ndou- Web Development Profile"
        self.twitter_title = "#freelancer , Justice Ndou Freelance Profile Home"
        self.og_title = "Freelance Profile of Justice Ndou"
        self.description = "Justice Ndou is a freelance website developer experienced in " \
                           "Google Cloud Platform Applications and API"
        self.twitter_description = "Justice Ndou is a freelance website developer experienced in " \
                                   "Google Cloud Platform Applications and API's"
        self.og_description = "Justice Ndou is a freelance website developer experienced in " \
                              "Google Cloud Platform Applications and API's"
        self.page = "main.home"
        self.path = ""
        self.image_filename = "imgs/justice.png"
        self.image_alt = "Justice Ndou Profile"

        return self

    def set_contact(self):
        self.title = "Contact Justice Ndou for freelance web development"
        self.twitter_title = "Contact Justice Ndou for freelance web development"
        self.og_title = "Contact Justice Ndou for freelance web development"
        self.description = "Contact Justice Ndou for help in Web Development experienced in " \
                           "Python, Javascript, Node.js, and etc"
        self.twitter_description = "Contact Justice Ndou for help in Web Development experienced in Python, " \
                                   "Javascript, Node.js, and etc"
        self.og_description = "Contact Justice Ndou for help in Web Development experienced in Python, " \
                              "Javascript, Node.js, and etc"
        self.page = "main.contact"
        self.path = ""
        self.image_filename = "imgs/contact-justice-ndou.png"
        self.image_alt = "Contact Justice Ndou"

        return self

    def set_blog(self):

        self.title = "Blog by Justice Ndou About Web Development, Freelancing, Bitcoin, and Dogecoin"
        self.twitter_title = "About Justice Ndou a Freelancer and Web Developer, Supporter of #Bitcoin and #Dogecoin"
        self.og_title = "A Blog by Justice Ndou on Web Development, Freelancing, Python and Crypto Currencies"
        self.description = "Justice Ndou Blogs About Web Development, Freelancing, Bitcoin, Dogecoin, Python etc"
        self.twitter_description = "Justice Ndou is a freelance website developer experienced in Google Cloud Platform " \
                                   "Applications and API's"
        self.og_description = "Justice Ndou Blogs about Web Development, Freelancing, Python, Node.js, " \
                              "Bitcoin and Dogecoin"
        self.page = "blog.blog"
        self.path = ""
        self.image_filename = "imgs/blog-by-justice-ndou.png"
        self.image_alt = "A Blog by Justice Ndou"

        return self

    def set_about(self):
        self.title = "About Justice Ndou - Web Development - Freelancer"
        self.description = "More Information on Justice Ndou life as a freelancer and web developer"
        self.twitter_title = "About Justice Ndou a Freelancer and Web Developer, Supporter of #Bitcoin and #Dogecoin"
        self.twitter_description = "Justice Ndou is a freelance website developer experienced in " \
                                   "Google Cloud Platform Applications and API's"
        self.og_title = "About Justice Ndou a Freelancer and Web Developer, Supporter of #Bitcoin and #Dogecoin"
        self.og_description = "About Justice Ndou a Freelancer, Web Developer, #Bitcoin and #Dogecoin Supporter"
        self.page = "main.about"
        self.path = ""
        self.image_filename = "imgs/about-justice-ndou.png"
        self.image_alt = "About Justice Ndou"

        return self

    def set_projects(self):
        self.title = "Justice Ndou Github Projects and Freelance Profiles"
        self.description = "Justice Ndou Github Projects and active freelance profiles"
        self.twitter_title = "Justice Ndou Github Projects"
        self.twitter_description = "Justice Ndou Github Projects and active freelance profiles"
        self.og_title = "Justice Ndou Github Projects"
        self.og_description = "Justice Ndou Github Projects and active freelance profiles"
        self.page = "projects.projects"
        self.path = ""
        self.image_filename = "imgs/github-projects-justice-ndou.png"
        self.image_alt = "Justice Ndou Github Projects"

        return self

    def set_freelancer(self):
        self.title = "Freelance - Hire Justice Ndou for Web Development- Javascript, Node.js, Python, GCP. React.js"
        self.description = "Freelance - Hire Justice Ndou for Web Development- Javascript, Node.js, Python," \
                           " GCP. React.js"
        self.twitter_title = "Freelance - Hire Justice Ndou for Web Development"
        self.twitter_description = "Experienced with React.js, Node.js, Python 3.x, GCP, Jinja2, Flask, and etc"
        self.og_title = "Freelance - Hire Justice Ndou for Web Development- Javascript, Node.js, Python, GCP. React.js "
        self.og_description = "You can Hire Justice Ndou for freelance web development i can work with react.js " \
                              " Node.js python and etc"
        self.page = "hireme.freelancer"
        self.path = ""
        self.image_filename = "imgs/hire-freelancer.png"
        self.image_alt = "Hire Justice Ndou as a freelancer"

        return self

    def set_learn_backend(self):
        # TODO- Update learn backend metatags to be relevant
        self.title = "Back End Development With Python and Node.js"
        self.twitter_title = "#Back End Development with Python and Node.js"
        self.og_title = "Back End Development with Python and Node.js"
        self.description = "Articles on Back End Development using Python 3.x and Node.js from basic to advanced"
        self.twitter_description = "Articles on Back End Development using Python 3.x and Node.js from basic to advanced"
        self.og_description = "Articles on Back End Development using Python 3.x and Node.js from basic to advanced"
        self.page = "blog.learn_more"
        self.path = "backend-development"
        self.image_filename = "imgs/learn-more/backend.png"
        self.image_alt = "Back End Web Development"

        return self

    def set_learn_frontend(self):
        # TODO - update learn frontend metatags to be relevant
        self.title = "Front End Website Development- React.JS - Vanilla JS - Jinja2-HTML-CSS"
        self.twitter_title = "Front End Website Development- React.JS - Vanilla JS - Jinja2-HTML-CSS"
        self.og_title = "Front End Website Development- React.JS - Vanilla JS - Jinja2-HTML-CSS"
        self.description = "Front End Web Development using React.JS Frameworks, LitHTML, and Vanilla Javascript with HTMl, CSS"
        self.twitter_description = "Front End Web Development using React.JS Frameworks, LitHTML, and Vanilla Javascript with HTMl, CSS"
        self.og_description = "Front End Web Development using React.JS Frameworks, LitHTML, and Vanilla Javascript with HTMl, CSS"
        self.page = "blog.learn_more"
        self.path = "frontend-development"
        self.image_filename = "imgs/learn-more/frontend.png"
        self.image_alt = "Front End Web Development"
        return self

    def set_login(self):
        # TODO - update login frontend metatags to be relevant
        self.title = "Login- Professional & Freelance Profile of Justice Ndou"
        self.twitter_title = "Login- Professional & Freelance Profile of Justice Ndou"
        self.og_title = "Login- Professional & Freelance Profile of Justice Ndou"
        self.description = "Login Page of Justice Ndou Freelance Profile Web App-Login to submit and manage your freelance jobs"
        self.twitter_description = "Login Page of Justice Ndou Freelance Profile Web App-Login to submit and manage your freelance jobs"
        self.og_description = "Login Page of Justice Ndou Freelance Profile Web App-Login to submit and manage your freelance jobs"
        self.page = "users.login"
        self.path = ""
        self.image_filename = "imgs/login.png"
        self.image_alt = "Login Page Freelance Profile Justice Ndou"

        return self

    def set_logout(self):
        # TODO - update login frontend metatags to be relevant
        self.title = "Logout- Professional & Freelance Profile of Justice Ndou"
        self.twitter_title = "Logout- Professional & Freelance Profile of Justice Ndou"
        self.og_title = "Logout- Professional & Freelance Profile of Justice Ndou"
        self.description = "Logout Page of Justice Ndou Web Development and Freelance Profile"
        self.twitter_description = "Logout Page of Justice Ndou Web Development and Freelance Profile"
        self.og_description = "Logout Page of Justice Ndou Web Development and Freelance Profile"
        self.page = "users.logout"
        self.path = ""
        self.image_filename = "imgs/logout.png"
        self.image_alt = "Logout Page Freelance Profile of Justice Ndou"

        return self

    def set_register(self):
        # TODO - update login frontend metatags to be relevant
        self.title = "Register New Account, Professional & Freelance Profile of Justice Ndou"
        self.twitter_title = "Register New Account, Professional & Freelance Profile of Justice Ndou"
        self.og_title = "Register New Account, Professional & Freelance Profile of Justice Ndou"
        self.description = "Register or Create New Account in order to Submit Freelance Jobs to Justice Ndou Personal Freelancing Site"
        self.twitter_description = "Register or Create New Account in order to Submit Freelance Jobs to Justice Ndou Personal Freelancing Site"
        self.og_description = "Register or Create New Account in order to Submit Freelance Jobs to Justice Ndou Personal Freelancing Site"
        self.page = "users.register"
        self.path = ""
        self.image_filename = "imgs/register.png"
        self.image_alt = "Create Account - Freelance Profile"

        return self
