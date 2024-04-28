from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from fuzzywuzzy import fuzz
import pickle
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# Load the XGBoost model
with open('predict_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Load the dataset
file_path = 'phone_data.xlsx'
sheet_name = 'phone_data'
df = pd.read_excel(file_path, sheet_name=sheet_name)
def fuzzy_match(input_str, options):
    # Handle NaN or missing values
    options = [str(option) for option in options if pd.notna(option)]

    return max(options, key=lambda x: fuzz.token_set_ratio(input_str, x.lower()))
    

@app.route('/')
def home():

    # # Define a function for fuzzy string matching
    # def fuzzy_match(input_str, options):
    #     options = [str(option) for option in options if pd.notna(option)]
    #     return max(options, key=lambda x: fuzz.token_set_ratio(input_str, x.lower()))

    return render_template('index.html')

@app.route('/result',methods=['POST','GET'])
def result():
    print("redirected")
    # Get user input from the URL parameters
    brand = request.form["brand"].strip().lower()
    model = request.form["model"].strip().lower()
    color = request.form["color"].strip().lower()
    storage = request.form["storage"].strip().lower()
    price=None
    flipkart_price=None
    croma_price=None
    filtered_df = df[
    (df["Phone Name"].str.lower().str.contains(brand))
    & (df["Model"].str.lower().str.contains(model))
    & (df["Color"].str.lower().str.contains(color))
    & (df["Storage"].str.lower() == storage)
]
    if filtered_df.empty:
        string_df = df[df["Phone Name"].apply(lambda x: isinstance(x, str))]
        # Calculate the similarity score between the user input and each entry in the Phone Name column
        scores = [fuzz.ratio(brand, entry.lower()) for entry in string_df["Phone Name"]]
        # Find the index of the entry with the highest similarity score
        best_match_index = scores.index(max(scores))
        # Filter the dataframe based on the best match index
        filtered_df = df.iloc[[best_match_index]]

    # Print the prices
    if not filtered_df.empty:
        try:
            price = filtered_df['Price'].values[0]
            print(f"Price: {price}")
        except IndexError:
            print("Price not found")

        try:
            flipkart_price = filtered_df['Flipkart1.Price'].values[0]
            if flipkart_price < price:
                print(f"Flipkart1 Price: {flipkart_price}")
            else:
                print(f"Flipkart1 Price is not lower than the original price")
        except IndexError:
            print("Flipkart1 Price not found")

        try:
            croma_price = filtered_df['croma1.Price'].values[0]
            print(f"Croma1 Price: {croma_price}")
        except IndexError:
            print("Croma1 Price not found")
    else:
        print("No matching phone found")
    label=['Poorvika','Flipkart','Croma']
    p=[int(price),int(flipkart_price),int(croma_price)]
    m=min(p)
    opt=''
    for i in range(0,len(p)):
        if(m==p[i]):
            opt=label[i]
            break
    return render_template('result.html', brand=brand, model=model, color=color, storage=storage, price=price, flipkart_price=flipkart_price, croma_price=croma_price,data=p,labels=label,opt=opt)



# Route for prediction
@app.route('/predict', methods=['POST'])
def predict():
    # Get user input from the form
    brand = request.form['brand'].strip().lower()
    model = request.form['model'].strip().lower()
    color = request.form['color'].strip().lower()
    storage = request.form['storage'].strip().lower()

    # Make sure input data is not empty
    if brand and model and color and storage:
    
            # Convert string inputs to integers using label encoding
            le=LabelEncoder()
            brand_label = le.fit([brand])[0]
            model_label = le.fit([model])[0]
            color_label = le.fit([color])[0]
            storage_label = le.fit([storage])[0]

            # Create a DataFrame with the encoded values
            X_pred = pd.DataFrame({
                'Brand': [brand_label],
                'Model': [model_label],
                'Color': [color_label],
                'Storage': [storage_label]
            })

            # Perform prediction using the model
            predicted_price = model.predict(X_pred)

            # Render prediction.html with the predicted price
            return render_template('prediction.html', brand=brand, model=model, color=color, storage=storage, predicted_price=predicted_price[0])



    else:
        # Handle case where input data is empty
        return render_template('error.html', message='Please fill out all the fields')



if __name__ == '__main__':
    app.run(debug=True)
