from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///history.db'
db = SQLAlchemy(app)

class tAction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), primary_key=False, default="NEW TRANSACTION")
    content = db.Column(db.Text, primary_key=False, default="Add a note!")
    value = db.Column(db.Float, primary_key=False, default ='0')
    purch_date = db.Column(db.DateTime, primary_key=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Transaction for : ' + str(self.item)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tHistory', methods=['GET' , 'POST'])
def newAction():
    if request.method == 'POST': 

        action_item = request.form['item']
        action_con = request.form['content']
        action_val = request.form['value']
        new_action = tAction(item=action_item,content=action_con,value=action_val)
        db.session.add(new_action)
        db.session.commit()
        return redirect('/tHistory')
    else:
        all_tAction = tAction.query.order_by(tAction.purch_date).all()
        return render_template('transactions.html', history=all_tAction)
        
@app.route('/tHistory/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    newAction = tAction.query.get_or_404(id)
    print("This is the edit : ", newAction.id)
    if request.method =='POST':
        newAction.item = request.form['item']
        newAction.con = request.form['content']
        newAction.val = request.form['value']
        db.session.commit()
        return redirect('/tHistory')

    else: return render_template('edit.html',tAction=newAction)

@app.route('/tHistory/delete/<int:id>', methods=['GET'])
def delAction(id):
    dAction = tAction.query.get_or_404(id)
    db.session.delete(dAction)
    db.session.commit()
    return redirect('/tHistory')

if __name__ == "__main__":
    app.run(debug=True)