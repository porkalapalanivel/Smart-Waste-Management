from flask import Blueprint

routes = Blueprint('routes', __name__)

@routes.route('/complaint')
def complaint():
    return "Complaint Registration Page"

@routes.route('/status')
def status():
    return "Complaint Status Page"
