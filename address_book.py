"""
Entrance to app
"""
from app import app, db
from app.models import Address


@app.shell_context_processor
def make_shell_context():
    """ Set up for flask shell """
    return {'db': db, 'Address': Address}
