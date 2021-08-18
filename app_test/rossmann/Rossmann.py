import pickle
import inflection
import pandas as pd
import numpy as np
import math
import datetime


class Rossmann(object):
    def __init__(self):
        self.home_path = 'C:/Users/Mariana/Documents/repositories/P002_Sales_Predictions_Drugstore/'
        self.rescaling_competition_distance          = pickle.load(open(self.home_path + 'parameters/rescaling_competition_distance.pkl', 'rb'))
        self.rescaling_competition_open_timeinmonths = pickle.load(open(self.home_path + 'parameters/rescaling_competition_open_timeinmonths.pkl', 'rb'))
        self.rescaling_promo_since_timeinweeks       = pickle.load(open(self.home_path + 'parameters/rescaling_promo_since_timeinweeks.pkl', 'rb'))
        self.rescaling_year                          = pickle.load(open(self.home_path + 'parameters/rescaling_year.pkl', 'rb'))
        self.encoding_store_type                     = pickle.load(open(self.home_path + 'parameters/encoding_store_type.pkl', 'rb'))

    def data_cleaning(self, df1):
        # === Rename Columns
        cols_old = ['Store', 'DayOfWeek', 'Date', 'Open', 'Promo', 'StateHoliday', 'SchoolHoliday',
                    'StoreType', 'Assortment', 'CompetitionDistance', 'CompetitionOpenSinceMonth',
                    'CompetitionOpenSinceYear', 'Promo2', 'Promo2SinceWeek', 'Promo2SinceYear', 'PromoInterval']

        # changing the name of the columns
        snakecase = lambda x: inflection.underscore(x)
        cols_new = list(map(snakecase, cols_old))

        # renaming dataset columns
        df1.columns = cols_new

        # === Data Types
        df1['date'] = pd.to_datetime(df1['date'])

        # === Fill out NA

        # competition_distance
        df1['competition_distance'].max()  # #checking the maximum distance: 75860.0
        df1['competition_distance'] = df1['competition_distance'].apply(lambda x: 2000000.0 if math.isnan(x) else (x))

        #  competition_open_since_month
        df1['competition_open_since_month'] = df1.apply(lambda x: x['date'].month if math.isnan(x['competition_open_since_month'])
                                                             else x['competition_open_since_month'], axis=1)

        #  competition_open_since_year
        df1['competition_open_since_year'] = df1.apply(lambda x: x['date'].year if math.isnan(x['competition_open_since_year'])
                                                            else x['competition_open_since_year'], axis=1)

        # promo2_since_week
        df1['promo2_since_week'] = df1.apply(lambda x: x['date'].week if math.isnan(x['promo2_since_week']) else x['promo2_since_week'], axis=1)

        # promo2_since_year
        df1['promo2_since_year'] = df1.apply(lambda x: x['date'].year if math.isnan(x['promo2_since_year']) else x['promo2_since_year'], axis=1)

        # promo_interval
        month_map = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                     7: 'Jul', 8: 'Ago', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

        # filling Na with "0"
        df1['promo_interval'].fillna(0, inplace=True)

        # finding the month name given month number by mapping the "month_map" dictionary
        df1['month_map'] = df1['date'].dt.month.map(month_map)

        df1['is_promo'] = df1[['promo_interval', 'month_map']].apply(lambda x: 0 if x['promo_interval'] == 0
                                                                          else 1 if x['month_map'] in x['promo_interval'].split(',')
                                                                          else 0, axis=1)

        # == Change Variables Types

        df1['competition_open_since_month'] = df1['competition_open_since_month'].astype(np.int64)
        df1['competition_open_since_year'] = df1['competition_open_since_year'].to_numpy(dtype=int)
        # df1['competition_open_since_year'] = df1['competition_open_since_year'].astype(np.int64)

        # df1['promo2_since_week'] = df1['promo2_since_week'].to_numpy(dtype=int)
        # df1['promo2_since_year'] = df1['promo2_since_year'].to_numpy(dtype=int)
        df1['promo2_since_week'] = df1['promo2_since_week'].astype(np.int64)
        df1['promo2_since_year'] = df1['promo2_since_year'].astype(np.int64)

        return df1

    def feature_engineering(self, df2):
        # === Feature Engineering

        # creating 'year' from 'date'
        df2['year'] = df2['date'].dt.year

        # creating 'month' from 'date'
        df2['month'] = df2['date'].dt.month

        # creating 'day' from 'date'
        df2['day'] = df2['date'].dt.day

        # creating 'week_of_year' from 'date'
        df2['week_of_year'] = df2['date'].dt.isocalendar().week.astype('int64')

        # creating 'year_week' from 'date'
        df2['year_week'] = df2['date'].dt.strftime('%Y-%W')

        # creating 'competition_open_since' by combining 'competition_open_since_year and 'competition_open_since_month'
        df2['competition_open_since'] = df2.apply(lambda x: datetime.datetime(year=x['competition_open_since_year'],
                                                                              month=x['competition_open_since_month'],
                                                                              day=1), axis=1)

        # creating 'competition_open_timeinmonths' by calculating the difference between 'date' and 'competition_open_since':
        df2['competition_open_timeinmonths'] = ((df2['date'] - df2['competition_open_since']) / 30).apply(lambda x: x.days).astype('int64')

        # creating 'promo_since' by combining 'promo2_since_year' and 'promo2_since_week'
        df2['promo_since'] = df2['promo2_since_year'].astype(str) + '-' + df2['promo2_since_week'].astype(str)  # string type (year-week, ex: 2015-31)
        df2['promo_since'] = df2['promo_since'].apply(lambda x: datetime.datetime.strptime(x + '-1', '%Y-%W-%w') - datetime.timedelta(days=7))  # date type (yyyy-mm-dd)

        # creating 'promo_since_timeinweeks' by calculating the difference between 'date' and 'promo_since':
        df2['promo_since_timeinweeks'] = ((df2['date'] - df2['promo_since']) / 7).apply(lambda x: x.days).astype('int64')

        # changing 'assortment' attribute by given classification
        df2['assortment'] = df2['assortment'].apply(lambda x: 'basic' if x == 'a'
                                                         else 'extra' if x == 'b'
                                                         else 'extended')

        # changing 'sate_holiday' attribute by given classification
        df2['state_holiday'] = df2['state_holiday'].apply(lambda x: 'Public_holiday' if x == 'a'
                                                               else 'Easter_holiday' if x == 'b'
                                                               else 'Christmas' if x == 'c'
                                                               else 'regular_day')

        # === Variable Filtering
        df2 = df2[(df2['open'] != 0)]
        cols_drop = ['open', 'promo_interval', 'month_map']
        df2 = df2.drop(cols_drop, axis=1)

        return df2

    def data_preparation(self, df5):
        # ===  Rescaling

        # competition_distance
        df5['competition_distance'] = self.rescaling_competition_distance.transform(df5[['competition_distance']].values)

        # competition_open_timeinmonths
        df5['competition_open_timeinmonths'] = self.rescaling_competition_open_timeinmonths.transform(df5[['competition_open_timeinmonths']].values)

        # promo_since_timeinweeks
        df5['promo_since_timeinweeks'] = self.rescaling_promo_since_timeinweeks.transform(df5[['promo_since_timeinweeks']].values)

        # year
        df5['year'] = self.rescaling_year.transform(df5[['year']].values)

        # === Encoding

        # state_holiday - one hot enconding (each holiday becomes a column)
        df5 = pd.get_dummies(df5, prefix=['state_holiday'], columns=['state_holiday'])

        # store_type - label enconding (each type becomes a value in a range)
        df5['store_type'] = self.encoding_store_type.fit_transform(df5['store_type'])

        # assortment - ordinal enconding (each assortment becomes a value in a hierarchy)
        assortment_dict = {'basic': 1, 'extra': 2, 'extended': 3}
        df5['assortment'] = df5['assortment'].map(assortment_dict)

        # === Nature Transformation

        # month
        df5['month_sin'] = df5['month'].apply(lambda x: np.sin(x * (2 * np.pi / 12)))
        df5['month_cos'] = df5['month'].apply(lambda x: np.cos(x * (2 * np.pi / 12)))

        # week_of_year
        df5['week_of_year_sin'] = df5['week_of_year'].apply(lambda x: np.sin(x * (2 * np.pi / 52)))
        df5['week_of_year_cos'] = df5['week_of_year'].apply(lambda x: np.cos(x * (2 * np.pi / 52)))

        # day
        df5['day_sin'] = df5['day'].apply(lambda x: np.sin(x * (2 * np.pi / 30)))
        df5['day_cos'] = df5['day'].apply(lambda x: np.cos(x * (2 * np.pi / 30)))

        # day_of_week
        df5['day_of_week_sin'] = df5['day_of_week'].apply(lambda x: np.sin(x * (2 * np.pi / 7)))
        df5['day_of_week_cos'] = df5['day_of_week'].apply(lambda x: np.cos(x * (2 * np.pi / 7)))

        cols_selected = ['store', 'promo', 'store_type', 'assortment', 'competition_distance', 'competition_open_since_month',
                         'competition_open_since_year', 'promo2', 'promo2_since_week', 'promo2_since_year',
                         'competition_open_timeinmonths', 'promo_since_timeinweeks', 'month_sin', 'month_cos', 'week_of_year_sin',
                         'week_of_year_cos', 'day_sin', 'day_cos', 'day_of_week_sin', 'day_of_week_cos']

        return df5[cols_selected]

    def get_prediction(self, model, original_data, test_data):
        # prediction
        pred = model.predict(test_data)

        # joining prediction into the original data
        original_data['predictions'] = np.expm1(pred)

        return original_data.to_json(orient='records', date_format='iso')