from flask import Flask, flash, jsonify, Response, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql
from .custom_json_encoder import CustomJSONEncoder

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://vdrkvhwmqplhdl:8356aaca74d20d83834993f62e6d67a89ec738e93850333e42b3dd666bf5124f@ec2-3-221-243-122.compute-1.amazonaws.com:5432/dai0k1egvf2bcu'
app.secret_key = b'\x19\x15\xb9\xa5\x8e\xa7\xb5b\x08\x1d\xb1g\x0cne\x0f'

db = SQLAlchemy(app)


class Analytic(db.Model):
    analytic_id = db.Column('analytic_id', db.Integer, primary_key=True)
    original_date = db.Column('original_date', postgresql.TIMESTAMP)
    taken_date = db.Column('taken_date', postgresql.TIMESTAMP)
    completed = db.Column('completed', db.Boolean)
    pill_names = db.Column('pill_names', postgresql.ARRAY(postgresql.TEXT))
    pill_quantities = db.Column(
        'pill_quantities', postgresql.ARRAY(postgresql.INTEGER))

    def __init__(self, original_date, taken_date, completed, pill_names, pill_quantities):
        self.original_date = original_date
        self.taken_date = taken_date
        self.completed = completed
        self.pill_names = pill_names
        self.pill_quantities = pill_quantities

    def to_dict(self):
        return {
            'analytic_id': self.analytic_id,
            'original_date': self.original_date,
            'taken_date': self.taken_date,
            'completed': self.completed,
            'pill_names': self.pill_names,
            'pill_quantities': self.pill_quantities
        }


@app.route('/')
def greet():
    return "APD - JWSM Tech"


@app.route('/api/analytics', methods=["GET", "POST"])
def get_all_analytics():
    if request.method == "GET":
        if not request.args:
            analytics = Analytic.query.all()
            result = analytics.to_dict() if isinstance(analytics, Analytic) else [
                x.to_dict() for x in analytics]
            return jsonify(result), 200
        else:  # GET by date range
            pass
    elif request.method == "POST":
        data = request.json
        try:
            original_date = data["original_date"]
            taken_date = data["taken_date"]
            completed = data["completed"]
            pill_names = data["pill_names"]
            pill_quantities = data["pill_quantities"]
        except KeyError:
            flash('Please enter all fields', 'error')

        if original_date and taken_date and completed and pill_names and pill_quantities:
            analytic = Analytic(original_date, taken_date,
                                completed, pill_names, pill_quantities)
            db.session.add(analytic)
            db.session.commit()
            flash("OK")
            return Response(status=201)
        else:
            flash('Please enter all fields', 'error')


@app.route('/api/analytics/<int:analytic_id>', methods=["GET"])
def get_analytic_by_id(analytic_id):
    if request.method == "GET":
        pass
