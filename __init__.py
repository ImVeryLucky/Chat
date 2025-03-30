from py4web import action


# example index page using session, template and vue.js
@action("index")  # the function below is exposed as a GET action
@action.uses("index.html", session)  # we use the template index.html and session
def index():
    session["counter"] = session.get("counter", 0) + 1
    session["user"] = {"id": 1}  # store a user in session
    return dict(session=session)