from flask import url_for


class Metatags:
    """
        Default Application Meta Tags
        # TODO find a way to intelligently add metatags
    """
    title: str = ""
    description: str = ""
    twitter_title: str = ""
    twitter_description: str = ""
    og_title: str = ""
    og_description: str = ""
    page: str = ""
    path: str = ""
    image_filename: str = ""
    image_alt: str = ""
    _url: str = ""

    def __init__(self, url=""):
        self._url = url

    # TODO - FINISH this
    def selector(self, endpoint):
        return {
            "main.home": self.set_home,
            "main.about": self.set_about,
            "main.contact": self.set_contact,
            "main.blog":  self.set_blog
        }.get(endpoint)

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

    def set_social_twitter(self):
        # TODO - update login frontend metatags to be relevant
        self.title = "Follow Freelance Profile of Justice Ndou on Twitter"
        self.twitter_title = "Follow Freelance Profile of Justice Ndou on Twitter"
        self.og_title = "Follow Freelance Profile of Justice Ndou on Twitter"
        self.description = "I use my Twitter Presence to share articles, events, and news related to Web Development Crypto Currencies and tech related stuff"
        self.twitter_description = "I use my Twitter Presence to share articles, events, and news related to Web Development Crypto Currencies and tech related stuff"
        self.og_description = "I use my Twitter Presence to share articles, events, and news related to Web Development Crypto Currencies and tech related stuff"
        self.page = "main.social"
        self.path = "twitter"
        self.image_filename = "imgs/twitter.png"
        self.image_alt = "Twitter Profile - Freelance Profile"
        return self

    def set_social_github(self):
        # TODO - update login frontend metatags to be relevant
        self.title = "Follow Github Profile of Justice Ndou- Freelance Profile"
        self.twitter_title = "Follow Github Profile of Justice Ndou- Freelance Profile"
        self.og_title = "Follow Github Profile of Justice Ndou- Freelance Profile"
        self.description = "Github Repositories for Freelance Profile of Justice Ndou"
        self.twitter_description = "Github Repositories for Freelance Profile of Justice Ndou"
        self.og_description = "Github Repositories for Freelance Profile of Justice Ndou"
        self.page = "main.social"
        self.path = "github"
        self.image_filename = "imgs/github.png"
        self.image_alt = "Github Profile - Freelance Profile"
        return self

    def set_terms(self):
        # TODO - update login frontend metatags to be relevant
        self.title = "Terms of Service, Freelance Profile of Justice Ndou"
        self.twitter_title = "Terms of Service, Freelance Profile of Justice Ndou"
        self.og_title = "Terms of Service, Freelance Profile of Justice Ndou"
        self.description = "Terms of Services Related to my services as a freelancer"
        self.twitter_description = "Terms of Services Related to my services as a freelancer"
        self.og_description = "Terms of Services Related to my services as a freelancer"
        self.page = "main.terms"
        self.path = ""
        self.image_filename = "imgs/terms.png"
        self.image_alt = "terms of service - Freelance Profile"
        return self

    def set_privacy(self):
        # TODO - update login frontend metatags to be relevant
        self.title = "Privacy Policy, Freelance Profile of Justice Ndou"
        self.twitter_title = "Privacy Policy, Freelance Profile of Justice Ndou"
        self.og_title = "Privacy Policy, Freelance Profile of Justice Ndou"
        self.description = "Privacy Policy Related to my services as a freelancer"
        self.twitter_description = "Privacy Policy Related to my services as a freelancer"
        self.og_description = "Privacy Policy Related to my services as a freelancer"
        self.page = "main.privacy"
        self.path = ""
        self.image_filename = "imgs/privacy.png"
        self.image_alt = "Privacy Policy - Freelance Profile"
        return self

    def set_how_to_create_freelancing_account(self):
        # TODO - update login frontend metatags to be relevant
        self.title = "How to create a freelancing account - Justice Ndou Freelance Profile"
        self.twitter_title = "How to create a freelancing account - Justice Ndou Freelance Profile"
        self.og_title = "How to create a freelancing account - Justice Ndou Freelance Profile"
        self.description = "a step by step guide on how to create a freelancing account on justice ndou freelancing profile website"
        self.twitter_description = "a step by step guide on how to create a freelancing account on justice ndou freelancing profile website"
        self.og_description = "a step by step guide on how to create a freelancing account on justice ndou freelancing profile website"
        self.page = "hireme.how_to_articles"
        self.path = "create-freelancing-account"
        self.image_filename = "imgs/hireme.png"
        self.image_alt = "Creating an Account - Freelance Profile"

        return self

    def set_submit_freelance_jobs(self):
        # TODO - update login frontend metatags to be relevant
        self.title = "How to submit freelance jobs - Justice Ndou Freelance Profile"
        self.twitter_title = "How to submit freelance jobs - Justice Ndou Freelance Profile"
        self.og_title = "How to submit freelance jobs - Justice Ndou Freelance Profile"
        self.description = "a step by step guide on how to submit freelance jobs on justice ndou freelancing profile website"
        self.twitter_description = "a step by step guide on how to submit freelance jobs on justice ndou freelancing profile website"
        self.og_description = "a step by step guide on how to submit freelance jobs on justice ndou freelancing profile website"
        self.page = "hireme.how_to_articles"
        self.path = "submit-freelance-jobs"
        self.image_filename = "imgs/hireme.png"
        self.image_alt = "Submitting freelancing jobs - Freelance Profile"

        return self

    def set_download_slack(self):
        # TODO - update login frontend metatags to be relevant
        self.title = "How to download and install Slack - Justice Ndou Freelance Profile"
        self.twitter_title = "How to download and install Slack - Justice Ndou Freelance Profile"
        self.og_title = "How to download and install Slack - Justice Ndou Freelance Profile"
        self.description = "a step by step guide on how to download and install slack"
        self.twitter_description = "a step by step guide on how to download and install slack"
        self.og_description = "a step by step guide on how to download and install slack"
        self.page = "hireme.how_to_articles"
        self.path = "download-install-slack"
        self.image_filename = "imgs/hireme.png"
        self.image_alt = "Download Install Slack - Freelance Profile"

        return self

    def set_download_teamviewer(self):
        # TODO - update login frontend metatags to be relevant
        self.title = "How to download and install Teamviewer - Justice Ndou Freelance Profile"
        self.twitter_title = "How to download and install Teamviewer - Justice Ndou Freelance Profile"
        self.og_title = "How to download and install Teamviewer - Justice Ndou Freelance Profile"
        self.description = "a step by step guide on how to download and install Teamviewer"
        self.twitter_description = "a step by step guide on how to download and install Teamviewer"
        self.og_description = "a step by step guide on how to download and install Teamviewer"
        self.page = "hireme.how_to_articles"
        self.path = "download-install-teamviewer"
        self.image_filename = "imgs/hireme.png"
        self.image_alt = "Download Install Teamviewer - Freelance Profile"

        return self

    def set_create_github(self):
        # TODO - update login frontend metatags to be relevant
        self.title = "How to create a Github Account - Justice Ndou Freelance Profile"
        self.twitter_title = "How to create a Github Account - Justice Ndou Freelance Profile"
        self.og_title = "How to create a Github Account - Justice Ndou Freelance Profile"
        self.description = "a step by step guide on how to create a github account, and keep updated on your website code"
        self.twitter_description = "a step by step guide on how to create a github account, and keep updated on your website code"
        self.og_description = "a step by step guide on how to create a github account, and keep updated on your website code"
        self.page = "hireme.how_to_articles"
        self.path = "create-a-github-account"
        self.image_filename = "imgs/hireme.png"
        self.image_alt = "Create Github Account - Freelance Profile"

        return self

    def set_gcp_account(self):
        # TODO - update login frontend metatags to be relevant
        self.title = "How to create a GCP Developer Account - Justice Ndou Freelance Profile"
        self.twitter_title = "How to create a GCP Developer Account - Justice Ndou Freelance Profile"
        self.og_title = "How to create a GCP Developer Account - Justice Ndou Freelance Profile"
        self.description = "a step by step guide on how to create a Google Cloud Platform Account, for hosting your website or web applications"
        self.twitter_description = "a step by step guide on how to create a Google Cloud Platform Account, for hosting your website or web applications"
        self.og_description = "a step by step guide on how to create a Google Cloud Platform Account, for hosting your website or web applications"
        self.page = "hireme.how_to_articles"
        self.path = "create-a-gcp-developer-account"
        self.image_filename = "imgs/hireme.png"
        self.image_alt = "Create a GCP Developer Account - Freelance Profile"

        return self

    def set_heroku_account(self):
        # TODO - update login frontend metatags to be relevant
        self.title = "How to create a Heroku Account - Justice Ndou Freelance Profile"
        self.twitter_title = "How to create a Heroku Developer Account - Justice Ndou Freelance Profile"
        self.og_title = "How to create a Heroku Developer Account - Justice Ndou Freelance Profile"
        self.description = "a step by step guide on how to create a Heroku Account, for hosting your website or web applications"
        self.twitter_description = "a step by step guide on how to create a Heroku Account, for hosting your website or web applications"
        self.og_description = "a step by step guide on how to create a Heroku Account, for hosting your website or web applications"
        self.page = "hireme.how_to_articles"
        self.path = "create-a-heroku-developer-account"
        self.image_filename = "imgs/hireme.png"
        self.image_alt = "Create a Heroku Developer Account - Freelance Profile"

        return self

    def set_communications(self):
        # TODO - update login frontend metatags to be relevant
        self.title = "Communication Procedures, Channels and Protocols - Justice Ndou Freelance Profile"
        self.twitter_title = "Communication Procedures, Channels and Protocols - Justice Ndou Freelance Profile"
        self.og_title = "Communication Procedures, Channels and Protocols - Justice Ndou Freelance Profile"
        self.description = "how to communicate with me as a client, channels, and procedures Justice Ndou Freelance Profile"
        self.twitter_description = "how to communicate with me as a client, channels, and procedures Justice Ndou Freelance Profile"
        self.og_description = "how to communicate with me as a client, channels, and procedures Justice Ndou Freelance Profile"
        self.page = "hireme.expectations"
        self.path = "communication-channels-procedures"
        self.image_filename = "imgs/hireme.png"
        self.image_alt = "Communication Channels and Procedures - Freelance Profile"
        return self

    def set_payments(self):
        # TODO - update login frontend metatags to be relevant
        self.title = "Payment Methods and Procedures For freelance jobs- Justice Ndou Freelancing Profile"
        self.twitter_title = "Payment Procuders For freelance jobs- Justice Ndou Freelancing Profile"
        self.og_title = "Payment Procuders For freelance jobs- Justice Ndou Freelancing Profile"
        self.description = "How to make payments for freelance jobs on Justice Ndou freelance profile"
        self.twitter_description = "How to make payments for freelance jobs on Justice Ndou freelance profile"
        self.og_description = "How to make payments for freelance jobs on Justice Ndou freelance profile"
        self.page = "hireme.expectations"
        self.path = "payments-procedures-methods"
        self.image_filename = "imgs/hireme.png"
        self.image_alt = "Payment Methods and Procedures - Freelance Profile"
        return self

    def set_diligence(self):
        # TODO - update login frontend metatags to be relevant
        self.title = "Due Diligence and Legal Expectations- Justice Ndou Freelancing Profile"
        self.twitter_title = "Due Diligence and Legal Expectations- Justice Ndou Freelancing Profile"
        self.og_title = "Due Diligence and Legal Expectations- Justice Ndou Freelancing Profile"
        self.description = "I expect that the website i am creating falls within legal boundaries in your country, state or province i also reserve the right to suspend services if otherwise"
        self.twitter_description = "I expect that the website i am creating falls within legal boundaries in your country, state or province i also reserve the right to suspend services if otherwise"
        self.og_description = "I expect that the website i am creating falls within legal boundaries in your country, state or province i also reserve the right to suspend services if otherwise"
        self.page = "hireme.expectations"
        self.path = "due-diligence"
        self.image_filename = "imgs/hireme.png"
        self.image_alt = "Due Diligence legal - Freelance Profile"
        return self

    def set_handinqover(self):
        # TODO - update login frontend metatags to be relevant
        self.title = "Handing Over Procedures and Production Servers Deployment - Justice Ndou Freelancing Profile"
        self.twitter_title = "Handing Over Procedures and Production Servers Deployment - Justice Ndou Freelancing Profile"
        self.og_title = "Handing Over Procedures and Production Servers Deployment - Justice Ndou Freelancing Profile"
        self.description = "Handing over procedures and production servers deployment"
        self.twitter_description = "Handing over procedures and production servers deployment"
        self.og_description = "Handing over procedures and production servers deployment"
        self.page = "hireme.expectations"
        self.path = "handing-over-procedures"
        self.image_filename = "imgs/hireme.png"
        self.image_alt = "Handing Over Procedures - Freelance Profile"
        return self

    def set_maintenance(self):
        # TODO - update login frontend metatags to be relevant
        self.title = "Project Maintenance Agreements and Procedures - Justice Ndou Freelancing Profile"
        self.twitter_title = "Project Maintenance Agreements and Procedures - Justice Ndou Freelancing Profile"
        self.og_title = "Project Maintenance Agreements and Procedures - Justice Ndou Freelancing Profile"
        self.description = "Maintenance Agreements expectations and Procedures for expected jobs and unplanned events"
        self.twitter_description = "Maintenance Agreements expectations and Procedures for expected jobs and unplanned events"
        self.og_description = "Maintenance Agreements expectations and Procedures for expected jobs and unplanned events"
        self.page = "hireme.expectations"
        self.path = "maintenance-procedures"
        self.image_filename = "imgs/hireme.png"
        self.image_alt = "Maintenance Procedures - Freelance Profile"
        return self


        # TODO- very important update meta tags

    def set_project_messages(self):
        self.title = "Project Maintenance Agreements and Procedures - Justice Ndou Freelancing Profile"
        self.twitter_title = "Project Maintenance Agreements and Procedures - Justice Ndou Freelancing Profile"
        self.og_title = "Project Maintenance Agreements and Procedures - Justice Ndou Freelancing Profile"
        self.description = "Maintenance Agreements expectations and Procedures for expected jobs and unplanned events"
        self.twitter_description = "Maintenance Agreements expectations and Procedures for expected jobs and unplanned events"
        self.og_description = "Maintenance Agreements expectations and Procedures for expected jobs and unplanned events"
        self.page = "hireme.expectations"
        self.path = "maintenance-procedures"
        self.image_filename = "imgs/hireme.png"
        self.image_alt = "Maintenance Procedures - Freelance Profile"
        return self

    def set_project_payments(self):
        self.title = "Project Maintenance Agreements and Procedures - Justice Ndou Freelancing Profile"
        self.twitter_title = "Project Maintenance Agreements and Procedures - Justice Ndou Freelancing Profile"
        self.og_title = "Project Maintenance Agreements and Procedures - Justice Ndou Freelancing Profile"
        self.description = "Maintenance Agreements expectations and Procedures for expected jobs and unplanned events"
        self.twitter_description = "Maintenance Agreements expectations and Procedures for expected jobs and unplanned events"
        self.og_description = "Maintenance Agreements expectations and Procedures for expected jobs and unplanned events"
        self.page = "hireme.expectations"
        self.path = "maintenance-procedures"
        self.image_filename = "imgs/hireme.png"
        self.image_alt = "Maintenance Procedures - Freelance Profile"
        return self

    def set_logger(self):
        self.title = "Server Statistics- Freelancing with AJ Ndou"
        self.twitter_title = "Server Statistics- Freelancing with AJ Ndou"
        self.og_title = "Server Statistics- Freelancing with AJ Ndou"
        self.description = "How to create a simple easy to use server statistics module for a flask app"
        self.twitter_description = "How to create a simple easy to use server statistics module for a flask app"
        self.og_description = "How to create a simple easy to use server statistics module for a flask app"
        self.page = "main.logger"
        self.path = ""
        self.image_filename = "imgs/server.png"
        self.image_alt = "Server Stats"
        return self

