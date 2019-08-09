from app import app, db
from flask import render_template

@app.route('/nas')
def list_nas():
    table_headers = ("#", "Name", "Short name", "Type", "Ports",
                     "Secret", "Server", "Community","Description")

    return render_template(
        'radius/list_nas.html',
        table_headers=table_headers,
        table_records=[]
    )