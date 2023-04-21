from flask import Flask, Response
from flask import render_template
from flask import make_response
import pdfkit
from data.data import persons
from flask_odoo import Odoo
from weasyprint import HTML, CSS

app = Flask(__name__)

app.config["ODOO_URL"] = "http://localhost:8069"
app.config["ODOO_DB"] = "web"
app.config["ODOO_USERNAME"] = "Roots"
app.config["ODOO_PASSWORD"] = "Roots"
odoo = Odoo(app)

class Partner(odoo.Model):
    _name = "res.partner"
    _domain = [["active", "=", True]]
    name = odoo.StringType()
    phone = odoo.StringType()
    email = odoo.StringType()
    # def get_

@app.route("/")
def index():
    partners = Partner.search_read([])
    return render_template('index.html',partners=partners)

@app.route("/print")
def print_pdf():
    partners = Partner.search_read([])
    out = render_template('index.html', partners=partners)
    options = {
        # "orientation": "landscape",
        "page-size": "A4",
        "margin-top": "2.5cm",
        "margin-right": "2.5cm",
        "margin-bottom": "2.5cm",
        "margin-left": "2.5cm",
        "encoding": "UTF-8",
    }
    css = ['static/css/styles.css','static/bootstrap/dist/css/bootstrap.css']
    pdf = pdfkit.from_string(out,css=css, options=options)
    return Response(pdf, mimetype="application/pdf")

if __name__ == '__main__':
    app.run(debug=True)