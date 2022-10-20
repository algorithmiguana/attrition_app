from flask import Flask, render_template, session, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import SubmitField, FloatField
import pickle
import numpy as np

app = Flask(__name__)

model = pickle.load(open("D:/Git Projects/flask_app/artifacts/model.pkl", "rb"))
app.config['SECRET_KEY'] = 'mysecretkey'

class InfoForm(FlaskForm):
    '''
    This general class gets a lot of form about puppies.
    Mainly a way to go through many of the WTForms Fields.
    '''
    SepalLengthCm = FloatField('SepalLength')
    SepalWidthCm = FloatField('SepalWidth')
    PetalLengthCm = FloatField('PetalLength')
    PetalWidthCm = FloatField('PetalWidth')

    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():

    # Create instance of the form.
    form = InfoForm()
    pred = ['Enter values']
    # If the form is valid on submission (we'll talk about validation next)
    if form.validate_on_submit():
        # Grab the data from the breed on the form.
        
        SepalLengthCm = float(form.SepalLengthCm.data)
        SepalWidthCm = float(form.SepalWidthCm.data)
        PetalLengthCm = float(form.PetalLengthCm.data)
        PetalWidthCm = float(form.PetalWidthCm.data)

        inp_features = [SepalLengthCm, SepalWidthCm, PetalLengthCm, PetalWidthCm]
        inp_features = [np.array(inp_features)]
        pred = model.predict(inp_features)[0]

        return render_template('result.html', pred = pred)

    return render_template("submit.html", form = form)
    

@app.route('/result', methods = ['GET','POST'])
def result():

    return render_template('result.html')


if __name__ == "__main__":
    app.run(debug=True)