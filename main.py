from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://pibd_user:Bruh@127.0.0.1:3306/Sistem_de_gestiune_bancara'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Banca(db.Model):
    __tablename__ = 'banci'

    idbanca = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(45), nullable=False)
    adresa = db.Column(db.String(200), nullable=False)
    telefon = db.Column(db.String(20), nullable=True)
    tip_banca = db.Column(db.String(50), nullable=False)
    
    conturi_bancare = db.relationship('ConturiBancare', back_populates='banca')

class Clienti(db.Model):
    __tablename__ = 'clienti'
    
    idclient = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(100), nullable=False)
    prenume = db.Column(db.String(100), nullable=False)
    adresa = db.Column(db.String(200), nullable=False)
    telefon = db.Column(db.String(20), nullable=True)
    tip_client = db.Column(db.String(50), nullable=False)
    
    conturi_bancare = db.relationship('ConturiBancare', back_populates='client')

class ConturiBancare(db.Model):
    __tablename__ = 'conturi_bancare'
    
    idcont = db.Column(db.Integer, primary_key=True)
    idbanca = db.Column(db.Integer, db.ForeignKey('banci.idbanca'), nullable=False)
    idclient = db.Column(db.Integer, db.ForeignKey('clienti.idclient'), nullable=False)
    tip_cont = db.Column(db.String(50), nullable=False)
    data_deschiderii = db.Column(db.Date, nullable=False)
    sold = db.Column(db.Numeric(19, 4), nullable=False)
    
    
    banca = db.relationship('Banca', back_populates='conturi_bancare')  
    
    
    client = db.relationship('Clienti', back_populates='conturi_bancare')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/banca', methods=['GET', 'POST'])
def banca():
    if request.method == 'POST':
        nume = request.form['nume']
        adresa = request.form['adresa']
        telefon = request.form['telefon']
        tip_banca = request.form['tip_banca']
        new_banca = Banca(nume=nume, adresa=adresa, telefon=telefon, tip_banca=tip_banca)
        db.session.add(new_banca)
        db.session.commit()
        return redirect(url_for('banca'))

    banci = Banca.query.all()
    return render_template('banca.html', banci=banci)

@app.route('/banca/edit_banca/<int:id>', methods=['GET', 'POST'])
def edit_banca(id):
    banca = Banca.query.get_or_404(id)
    if request.method == 'POST':
        banca.nume = request.form['nume']
        banca.adresa = request.form['adresa']
        banca.telefon = request.form['telefon']
        banca.tip_banca = request.form['tip_banca']
        db.session.commit()
        return redirect(url_for('banca'))
    return render_template('edit_banca.html', banca=banca)

@app.route('/banca/delete/<int:idbanca>')
def delete_banca(idbanca):
    banca = Banca.query.get_or_404(idbanca)
    db.session.delete(banca)
    db.session.commit()
    return redirect(url_for('banca'))


@app.route('/clienti', methods=['GET', 'POST'])
def clienti():
    if request.method == 'POST':
        nume = request.form['nume']
        prenume = request.form['prenume']
        adresa = request.form['adresa']
        telefon = request.form['telefon']
        tip_client = request.form['tip_client']
        new_client = Clienti(nume=nume, prenume=prenume, adresa=adresa, telefon=telefon, tip_client=tip_client)
        db.session.add(new_client)
        db.session.commit()
        return redirect(url_for('clienti'))

    clienti = Clienti.query.all()
    return render_template('clienti.html', clienti=clienti)

@app.route('/clienti/edit_client/<int:id>', methods=['GET', 'POST'])
def edit_clienti(id):
    clienti = Clienti.query.get_or_404(id)
    if request.method == 'POST':
        clienti.nume = request.form['nume']
        clienti.prenume = request.form['prenume']
        clienti.adresa = request.form['adresa']
        clienti.telefon = request.form['telefon']
        clienti.tip_client = request.form['tip_client']
        db.session.commit()
        return redirect(url_for('clienti'))
    return render_template('edit_client.html', clienti=clienti)

@app.route('/clienti/delete/<int:idclient>')
def delete_client(idclient):
    client = Clienti.query.get_or_404(idclient)
    db.session.delete(client)
    db.session.commit()
    return redirect(url_for('clienti'))

@app.route('/conturi', methods=['GET', 'POST'])
def conturi():
    banci = Banca.query.all()  
    clienti = Clienti.query.all()  
    if request.method == 'POST':
        idbanca = request.form['idbanca']
        idclient = request.form['idclient']
        tip_cont = request.form['tip_cont']
        data_deschiderii = request.form['data_deschiderii']
        sold = request.form['sold']
        new_cont = ConturiBancare(idbanca=idbanca, idclient=idclient, tip_cont=tip_cont, 
                                  data_deschiderii=data_deschiderii, sold=sold)
        db.session.add(new_cont)
        db.session.commit()
        return redirect(url_for('conturi'))

    conturi = ConturiBancare.query.all()  
    return render_template('conturi.html', conturi=conturi, banci=banci, clienti=clienti)

@app.route('/conturi/edit_cont/<int:id>', methods=['GET', 'POST'])
def edit_cont(id):
    conturi = ConturiBancare.query.get_or_404(id)
    if request.method == 'POST':
        conturi.tip_cont = request.form['tip_cont']
        conturi.sold = request.form['sold']
        db.session.commit()
        return redirect(url_for('conturi'))
    return render_template('edit_cont.html', conturi=conturi)

@app.route('/conturi/delete/<int:idcont>')
def delete_cont(idcont):
    cont = ConturiBancare.query.get_or_404(idcont)
    db.session.delete(cont)
    db.session.commit()
    return redirect(url_for('conturi'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)