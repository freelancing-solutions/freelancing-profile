# # import unittest
# import uuid, time

#     # uid = db.Column(db.String(128),unique=False, nullable=False)
#     # project_id = db.Column(db.Integer, unique=True, primary_key=True)
#     # project_name = db.Column(db.String(1048), unique=False, nullable=False)
#     # project_category = db.Column(db.String(64), nullable=False)
#     # description = db.Column(db.String(2096), nullable=False)
#     # progress = db.Column(db.Integer, nullable=False)
#     # status = db.Column(db.String(32), nullable=False)
#     # link_details = db.Column(db.String(256), nullable=False)
#     # time_created = db.Column(db.Integer, nullable=False)
#     # est_hours_to_complete = db.Column(db.Integer, nullable=False)
#     # currency = db.Column(db.String(32), nullable=False)
#     # budget_allocated = db.Column(db.Integer, nullable=False)
#     # total_paid = db.Column(db.Integer, nullable=False)

# def test_blog_routes(self):
#     from ..blog import routes
#     pass

# def test_hireme_routes(self):
#     from ..hireme import routes
#     pass

# def test_hireme_freelance_job_model(self):
#     from ..hireme.models import FreelanceJobModel
#     uid = str(uuid.uuid4())
#     project_name = "Website Development"
#     project_category = "Website"
#     description = "Develop my website/blog based on wordpress"
#     progress = 24
#     status = "started"
#     link_details = "/website/website-development"
#     hours_to_complete = 24 * 7
#     right_now_milliseconds = int(float(time.time()) * 1000)
#     currency = "R"
#     budget_allocated = 520
#     total_paid = 100
#     freelance_job_model = FreelanceJobModel(uid=uid,project_name=project_name,project_category=project_category,
#     description=description,progress=progress,status=status,link_details=link_details,time_created=right_now_milliseconds,
#     est_hours_to_complete=hours_to_complete,currency=currency,budget_allocated=budget_allocated,total_paid=total_paid)

#     assert isinstance(freelance_job_model,FreelanceJobModel)
#     assert freelance_job_model.budget_allocated = budget_allocated
#     assert freelance_job_model.project_name = project_name





# if __name__ == '__main__':
#     # begin the unittest.main()
#     unittest.main()