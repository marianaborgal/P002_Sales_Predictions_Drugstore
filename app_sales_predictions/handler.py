import os
import pickle
import pandas           as pd
from flask              import Flask, request, Response
from rossmann.Rossmann  import Rossmann # from folder.file import class


# loading model
model = pickle.load(open('model/model_xgb_tuned.pkl', 'rb'))

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
    find_port = os.environ.get('PORT', 5000)
    app.run(host='0.0.0.0', port=find_port, debug=True)
    #app.run(host='192.168.0.16', port=find_port, debug=True)