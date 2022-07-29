from .__init__ import director
from ..extensions import db
from flask import render_template, redirect, url_for, request, session
import datetime;


@director.route('/director')
def directorLoginPage():
    line_id = request.args.get("userId")

    if line_id is None:
        session['line_id'] = None
        return render_template('director/welcome.html')