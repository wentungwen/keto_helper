from flask import Flask, request, render_template, jsonify
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import openpyxl

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///keto.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)


class Oil(db.Model):
    __tablename__ = 'oils'
    id = db.Column(db.Integer, primary_key=True)
    name_cn = db.Column(db.String(100), nullable=True)
    name_en = db.Column(db.String(100), nullable=True)
    omega3 = db.Column(db.Numeric(precision=5, scale=1), nullable=True)
    omega6 = db.Column(db.Numeric(precision=5, scale=1), nullable=True)
    omega9 = db.Column(db.Numeric(precision=5, scale=1), nullable=True)
    omega_ratio = db.Column(db.Integer, nullable=True)
    sat_fat = db.Column(db.Numeric(precision=5, scale=1), nullable=True)
    smoky_p = db.Column(db.Integer, nullable=True)
    cooking_m = db.Column(db.String(100), nullable=True)


class Sweetener(db.Model):
    __tablename__ = 'sweeteners'
    id = db.Column(db.Integer, primary_key=True)
    name_cn = db.Column(db.String(100), nullable=True)
    name_en = db.Column(db.String(100), nullable=True)
    sweetness_min= db.Column(db.Numeric(precision=2, scale=1), nullable=True)
    sweetness_max= db.Column(db.Numeric(precision=2, scale=1), nullable=True)
    gi = db.Column(db.Integer, nullable=True)
    is_natural = db.Column(db.Boolean, nullable=True)
    aftertaste = db.Column(db.String(100), nullable=True)
    cost = db.Column(db.Integer, nullable=False)

class Powder(db.Model):
    __tablename__ = 'powders'
    id = db.Column(db.Integer, primary_key=True)
    name_cn = db.Column(db.String(100), nullable=True)
    name_en = db.Column(db.String(100), nullable=True)
    carb = db.Column(db.Integer, nullable=True)
    fat = db.Column(db.Integer, nullable=True)
    fiber = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(100), nullable=True)
    suggestion = db.Column(db.String(100), nullable=True)


@app.context_processor
def inject_nav():
    nav = [
        {
            'title': 'oil table',
            'description': 'The oil type',
            'url': 'oil-table',
            'img': 'oil.jpg'
        },
        {
            'title': 'sweetener table',
            'description': 'Sweetener table',
            'url': 'sweetener-table',
            'img': 'sweetener.jpg'
        },
        {
            'title': 'sweetener calculator',
            'description': 'Sweetener calculator',
            'url': 'sweetener-calculator',
            'img': 'sweetener-calculator.jpg'
        },
        {
            'title': 'powder table ',
            'description': 'powder calculator',
            'url': 'powder-table',
            'img': 'powder.jpg'
        }
    ]
    return {'nav': nav}


def write_to_database(item_name, item_db):
    wb = openpyxl.load_workbook('data/keto project.xlsx')
    ws = wb[item_name]
    items = [row for row in ws.values]
    item_title = items[0]

    for item_list in items[1:]:
        n_obj = item_db()  
        if n_obj.query.filter_by(name_en=item_list[1]).first():
            print(123123)
        else:
            for idx, n in enumerate(item_list):
                
                print(item_title[idx], n)
                setattr(n_obj, item_title[idx], n)
            db.session.add(n_obj)
            db.session.commit()
            db.session.close()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/oil-table')
def oil():
    oils = Oil.query.all()
    return render_template('oil.html', oils=oils)


@app.route('/sweetener-table')
def sweetener():
    sweeteners = Sweetener.query.all()
    return render_template('sweetener.html', sweeteners=sweeteners)


@app.route('/get-sweetener', methods=['POST', 'GET'])
def get_sweetener():
    if request.method == 'GET':
        sweeteners = Sweetener.query.all()
        data = [{
            'id': sweetener.id,
            'name_cn': sweetener.name_cn,
            'name_en': sweetener.name_en,
            'sweetness_max': sweetener.sweetness_max,
            'sweetness_min': sweetener.sweetness_min,
            'gi': sweetener.gi,
            'is_natural': sweetener.is_natural,
            'aftertaste': sweetener.aftertaste,
            'cost': sweetener.cost
        } for sweetener in sweeteners]
        return jsonify(data=data)


@app.route('/sweetener-calculator', methods=['POST', 'GET'])
def sweetener_calculator_page():
    sweeteners = Sweetener.query.all()
    return render_template('sweetener_calculator.html', sweeteners=sweeteners)


@app.route('/powder-table')
def powder():
    powders = Powder.query.all()
    return render_template('powder.html', powders=powders)




# with app.app_context():
#     db.create_all()
#     write_to_database('oil', item_db=Oil)
#     write_to_database('sweetener', item_db=Sweetener)
#     write_to_database('powder', item_db=Powder)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)