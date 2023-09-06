from flask import Flask, render_template, request
import pandas as pd
import pickle
app = Flask(__name__)
data = pd.read_csv('Cleaned_data.csv')
pipe = pickle.load(open("RFModel.pkl", 'rb'))


@app.route('/')
def index():
    locations = sorted(data['location'].unique())
    area_types = sorted(data['area_type'].unique())
    availability = sorted(data['availability'].unique())

    return render_template('index.html', locations=locations, area_types=area_types, availabilitys=availability)


@app.route('/predict', methods=['POST'])
def predict():
    location = request.form.get('location')
    bhk = request.form.get('bhk')
    bath = request.form.get('bath')
    sqft = request.form.get('total_sqft')
    balcony = request.form.get('balcony')
    area_type = request.form.get('area_type')
    availability = request.form.get('availability')

    # print(sqft)
    if sqft == '' or bath == '' or balcony == '' or bhk == '':
        return str("Enter the inputs")
    input = pd.DataFrame([[area_type, availability, location, sqft, bath, balcony, bhk]], columns=['area_type', 'availability',
                         'location', 'total_sqft', 'bath', 'balcony', 'BHK'])
    prediction = pipe.predict(input)[0]

    return str(prediction*100000)+str(" Rupees")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
