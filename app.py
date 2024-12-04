from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///company.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Officer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    area = db.Column(db.String(100), nullable=False)
    territory = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def home():
    search_query = request.args.get('search', '')  # Get search query from URL

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        area = request.form['area']
        territory = request.form['territory']
        district = request.form['district']

        new_officer = Officer(name=name, phone=phone, area=area, territory=territory, district=district)
        db.session.add(new_officer)
        db.session.commit()

        return redirect(url_for('home'))

    # If search query is provided, filter officers
    if search_query:
        officers = Officer.query.filter(
            Officer.name.ilike(f'%{search_query}%') |
            Officer.phone.ilike(f'%{search_query}%') |
            Officer.area.ilike(f'%{search_query}%') |
            Officer.territory.ilike(f'%{search_query}%') |
            Officer.district.ilike(f'%{search_query}%')
        ).all()
    else:
        officers = Officer.query.all()

    return render_template('index.html', officers=officers)


    officers = Officer.query.all()
    return render_template('index.html', officers=officers)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    officer = Officer.query.get_or_404(id)

    if request.method == 'POST':
        officer.name = request.form['name']
        officer.phone = request.form['phone']
        officer.area = request.form['area']
        officer.territory = request.form['territory']
        officer.district = request.form['district']

        db.session.commit()
        return redirect(url_for('home'))

    return render_template('edit.html', officer=officer)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    officer = Officer.query.get_or_404(id)
    db.session.delete(officer)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
