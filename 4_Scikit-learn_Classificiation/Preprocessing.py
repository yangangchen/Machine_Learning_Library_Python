# Preprocessing.py
# 
# Copyright (C) 2017  Yangang Chen
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
# 
# 
# 
# Preprocess the dataset "adult.data" and "adult.test" for further machine learning.

################################

import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler


def main():
    column_names = ['age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status',
                    'occupation', 'relationship', 'race', 'sex', 'capital-gain', 'capital-loss',
                    'hours-per-week', 'native-country', 'income-class']
    df_train = pd.read_csv('adult.data', header=None)
    df_train.columns = column_names
    df_test = pd.read_csv('adult.test', skiprows=1, header=None)
    df_test.columns = column_names

    print(df_train.set_index('education').groupby(level=0)['education-num'].mean())
    df_train = df_train.loc[:, (df_train.columns != 'education') & (df_train.columns != 'fnlwgt')]
    df_test = df_test.loc[:, (df_test.columns != 'education') & (df_test.columns != 'fnlwgt')]

    column_nonfloat = ['workclass', 'marital-status', 'occupation',
                       'relationship', 'race', 'sex', 'native-country', 'income-class']
    for item in column_nonfloat:
        labelencoder = LabelEncoder()
        # use the pandas.factorize function, which takes care of the nans automatically (assigns them -1)
        labelencoder.fit(df_train[item].append(df_test[item]).factorize()[0])
        df_train[item] = labelencoder.transform(df_train[item].factorize()[0])
        df_test[item] = labelencoder.transform(df_test[item].factorize()[0])

    column_float = ['age', 'capital-gain', 'capital-loss', 'hours-per-week']
    scaler = StandardScaler().fit(df_train[column_float])
    df_train[column_float] = scaler.transform(df_train[column_float])
    df_test[column_float] = scaler.transform(df_test[column_float])

    print(df_train['income-class'].mean())
    print(df_test['income-class'].mean())

    df_train.to_csv('train.csv')
    df_test.to_csv('test.csv')


if __name__ == "__main__":
    main()
