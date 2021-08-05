import pandas           as pd
import pickle
from flask              import Flask, request, Response
from rossmann.Rossmann  import Rossmann # from folder.file import class

# loading model
model = pickle.load(open('C:/Users/Mariana/Documents/repositories/P002_Sales_Predictions_Drugstore/model/model_xgb_tuned.pkl', 'rb')) # usar endereço completo se erro

# initalizing API
app = Flask(__name__)

@app.route("/rossmann/prediction", methods=['POST']) #endpoint
def rossmann_prediction():
    test_json = request.get_json()

    if test_json:  # if not empty

        if isinstance(test_json, dict):  # if unique json
            test_df = pd.DataFrame(test_json, index=[0])
        else:  # if multiple jsons
            test_df = pd.DataFrame(test_json, columns=test_json[0].keys())

        # instantiate Rossmann Class
        pipeline = Rossmann()

        # data cleaning
        df1 = pipeline.data_cleaning(test_df)

        # feature engineering
        df2 = pipeline.feature_engineering(df1)

        # data preparation
        df3 = pipeline.data_preparation(df2)

        # prediction
        df_response = pipeline.get_prediction(model, test_df, df3)

        return df_response

    else:  # if empty
        return Response('{}', status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run('192.168.0.7', port=5000, debug=True)
    #app.run('127.0.0.1', port=5000, debug=True)
    #app.run('0.0.0.0', debug=True)
