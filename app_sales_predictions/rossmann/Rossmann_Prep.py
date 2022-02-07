import pickle
import inflection
import pandas as pd
import numpy as np
import math
import datetime


class Rossmann_Prep(object):
    def __init__(self):
        self.home_path = ''
        self.rescaling_competition_distance = pickle.load(open(self.home_path + 'parameters/rescaling_competition_distance_c02.pkl', 'rb'))
        self.rescaling_competition_open_timeinmonths = pickle.load(open(self.home_path + 'parameters/rescaling_competition_open_timeinmonths_c02.pkl', 'rb'))
        self.rescaling_promo2_since_timeinweeks = pickle.load(open(self.home_path + 'parameters/rescaling_promo2_since_timeinweeks_c02.pkl', 'rb'))
        self.rescaling_year = pickle.load(open(self.home_path + 'parameters/rescaling_year_c02.pkl', 'rb'))
        self.encoding_store_type = pickle.load(open(self.home_path + 'parameters/encoding_store_type_c02.pkl', 'rb'))


    def data_cleaning(self, df1):
        # === RENAME COLUMNS
        cols_old = ['Store', 'DayOfWeek', 'Date', 'Open', 'Promo', 'StateHoliday', 'SchoolHoliday',
                    'StoreType', 'Assortment', 'CompetitionDistance', 'CompetitionOpenSinceMonth',
                    'CompetitionOpenSinceYear', 'Promo2', 'Promo2SinceWeek', 'Promo2SinceYear', 'PromoInterval']

        # changing the name of the columns
        snakecase = lambda x: inflection.underscore(x)
        cols_new = list(map(snakecase, cols_old))

        # renaming dataset columns
        df1.columns = cols_new
        df1.rename(columns={'promo_interval': 'promo2_interval'}, inplace=True)

        # === FILLING OUT NA

        # competition_distance
        df1['competition_distance'].fillna(0, inplace=True)

        # creating date infos
        new_min_date = datetime.date(pd.Timestamp.min.year + 1, pd.Timestamp.min.month, pd.Timestamp.min.day)
        min_day = new_min_date.day
        min_month = new_min_date.month
        min_year = new_min_date.year
        min_week = new_min_date.isocalendar()[1]

        #  competition_open_since_month
        df1['competition_open_since_month'].fillna(min_month, inplace=True)

        #  competition_open_since_year
        df1['competition_open_since_year'].fillna(min_year, inplace=True)

        # promo2_since_week
        df1['promo2_since_week'].fillna(min_week, inplace=True)

        # promo2_since_year
        df1['promo2_since_year'].fillna(min_year, inplace=True)

        # promo2_interval
        df1['promo2_interval'].fillna(0, inplace=True)

        # == Change Variables Types

        df1['date'] = pd.to_datetime(df1['date'])

        df1['competition_distance'] = df1['competition_distance'].astype(np.int64)
        df1['competition_open_since_month'] = df1['competition_open_since_month'].astype(np.int64)
        df1['competition_open_since_year'] = df1['competition_open_since_year'].astype(np.int64)

        df1['promo2_since_week'] = df1['promo2_since_week'].astype(np.int64)
        df1['promo2_since_year'] = df1['promo2_since_year'].astype(np.int64)


        return df1

    def feature_engineering(self, df2):
        # === FEATURE ENGINEERING

        # creating 'year' from 'date'
        df2['year'] = df2['date'].dt.year

        # creating 'month' from 'date'
        df2['month'] = df2['date'].dt.month

        # creating 'day' from 'date'
        df2['day'] = df2['date'].dt.day

        # creating 'week_of_year' from 'date'
        df2['week_of_year'] = df2['date'].dt.isocalendar().week.astype(np.int64)

        # creating 'year_week' from 'date'
        df2['year_week'] = df2['date'].dt.strftime('%Y-%W')

        # creating 'season' from 'date'
        def season_from_date(date):
            year = str(date.year)
            seasons = {'spring': pd.date_range(start='01/03/' + year, end='31/05/' + year),
                       'summer': pd.date_range(start='01/06/' + year, end='30/09/' + year),
                       'autumn': pd.date_range(start='01/09/' + year, end='30/11/' + year)}
            if date in seasons['spring']:
                return 'spring'
            if date in seasons['summer']:
                return 'summer'
            if date in seasons['autumn']:
                return 'autumn'
            else:
                return 'winter'
        df2['season'] = df2['date'].map(season_from_date)

        # changing 'sate_holiday' attribute by given classification
        df2['state_holiday'] = df2['state_holiday'].apply(lambda x: 'public_holiday' if x == 'a'
                                                                else 'easter_holiday' if x == 'b'
                                                                else 'christmas' if x == 'c'
                                                                else 'regular_day')

        # changing 'assortment' attribute by given classification
        df2['assortment'] = df2['assortment'].apply(lambda x: 'basic' if x == 'a'
                                                         else 'extra' if x == 'b'
                                                         else 'extended')

        # creating 'competition_open_since' by combining 'competition_open_since_year and 'competition_open_since_month'
        df2['competition_open_since'] = df2.apply(lambda x: datetime.datetime(year=x['competition_open_since_year'],
                                                                              month=x['competition_open_since_month'],
                                                                              day=1), axis=1)

        # creating 'competition_open_timeinmonths' by calculating the difference between 'date' and 'competition_open_since':
        df2['competition_open_timeinmonths'] = ((pd.to_datetime(df2['date']).dt.date -
                                                 pd.to_datetime(df2['competition_open_since']).dt.date) / 30).apply(lambda x: x.days).astype('int64')

        # creating 'promo2_since' by combining 'promo2_since_year' and 'promo2_since_week'
        df2['promo2_since'] = df2['promo2_since_year'].astype(str) + '-' + df2['promo2_since_week'].astype(str)  # string type (year-week, ex: 2015-31)
        df2['promo2_since'] = df2['promo2_since'].apply(lambda x: datetime.datetime.strptime(x + '-1', '%Y-%W-%w') - datetime.timedelta(days=7))  # date type (yyyy-mm-dd)

        # creating 'promo2_since_timeinweeks' by calculating the difference between 'date' and 'promo2_since':
        df2['promo2_since_timeinweeks'] = ((pd.to_datetime(df2['date']).dt.date -
                                            pd.to_datetime(df2['promo2_since']).dt.date) / 7).apply(lambda x: x.days).astype(np.int64)

        # creating 'is_promo2' to check if the purchase was during a promotion ('promo2')
        month_map = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                     7: 'Jul', 8: 'Ago', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

        # finding the month name given month number by mapping the "month_map" dictionary
        df2['month_map'] = df2['date'].dt.month.map(month_map)

        df2['is_promo2'] = df2[['promo2_interval', 'month_map']].apply(lambda x: 0 if x['promo2_interval'] == 0
                                                                            else 1 if x['month_map'] in x['promo2_interval'].split(',')
                                                                            else 0, axis=1)
        # reordering columns
        df2 = df2[['store', 'date', 'day_of_week', 'open', 'state_holiday', 'school_holiday', 'store_type', 'assortment',
                   'competition_distance', 'competition_open_since_month', 'competition_open_since_year',
                   'competition_open_since', 'competition_open_timeinmonths',
                   'promo', 'promo2', 'promo2_since_week', 'promo2_since_year', 'promo2_interval',
                   'promo2_since', 'promo2_since_timeinweeks', 'month_map', 'is_promo2',
                   'year', 'month', 'day', 'week_of_year', 'year_week', 'season']]

        # === Variable Filtering
        df2 = df2[(df2['open'] != 0)]
        cols_drop = ['open', 'promo2_interval', 'month_map']
        df2 = df2.drop(cols_drop, axis=1)

        return df2

    def data_preparation(self, df5):
        # === RESCALING

        # competition_distance
        df5['competition_distance'] = self.rescaling_competition_distance.transform(df5[['competition_distance']].values)

        # competition_open_timeinmonths
        df5['competition_open_timeinmonths'] = self.rescaling_competition_open_timeinmonths.transform(df5[['competition_open_timeinmonths']].values)

        # promo2_since_timeinweeks
        df5['promo2_since_timeinweeks'] = self.rescaling_promo2_since_timeinweeks.transform(df5[['promo2_since_timeinweeks']].values)

        # year
        df5['year'] = self.rescaling_year.transform(df5[['year']].values)

        # === ENCONDING

        # state_holiday - one hot enconding (each holiday becomes a column)
        df5 = pd.get_dummies(df5, prefix=['state_holiday'], columns=['state_holiday'])

        # store_type - label enconding (each type becomes a value in a range)
        df5['store_type'] = self.encoding_store_type.fit_transform(df5['store_type'])

        # assortment - ordinal enconding (each assortment becomes a value in a hierarchy)
        assortment_dict = {'basic': 1, 'extra': 2, 'extended': 3}
        df5['assortment'] = df5['assortment'].map(assortment_dict)

        # season - ordinal enconding (each assortment becomes a value in a hierarchy)
        season_dict = {'winter': 1, 'spring': 2, 'summer': 3, 'autumn': 4}
        df5['season'] = df5['season'].map(season_dict)

        # === NATURE TRANSFORMATION

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

        cols_selected_boruta = ['store', 'store_type', 'assortment', 'competition_distance', 'competition_open_since_month',
                                'competition_open_since_year', 'competition_open_timeinmonths',
                                'promo', 'promo2', 'promo2_since_week', 'promo2_since_year', 'promo2_since_timeinweeks',
                                'year', 'season', 'month_cos', 'month_sin', 'week_of_year_cos', 'week_of_year_sin',
                                'day_sin', 'day_cos', 'day_of_week_sin', 'day_of_week_cos']

        return df5[cols_selected_boruta]

    def get_prediction(self, model, original_data, test_data):
        # prediction
        pred = model.predict(test_data)

        # joining prediction into the original data
        original_data['predictions'] = np.expm1(pred)

        return original_data.to_json(orient='records', date_format='iso')