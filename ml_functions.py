# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 10/23/17
@author: Zachary Oliver
"""

import sys
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import numpy as np
from datetime import datetime

from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

from list_functions import list_find, list_append
from df_functions import df_remove_column_by_index, df_concat, df_print_row_count

sys.path.insert(0, './')

'''********************************************
**************LINEAR REGRESSION****************
***********************************************
'''
def lin_reg_score(df, feature_columns, response_vector, numcv=10):
    # this model is for a continuous prediction vs a 1,0 or neighbors
    X = df[feature_columns]
    y = df[response_vector]
    #X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=123)
    linreg = LinearRegression()
    #linreg.fit(X, y)
    ##linreg_mse_score = cross_val_score(linreg, X, y, cv=10, scoring='neg_mean_squared_error', n_jobs=-1)

    #y_pred = linreg.predict(X_test)

    #rmse_list = []
    #rmse = np.sqrt(metrics.mean_squared_error(y_test, y_pred))
    #list_append(rmse_list, rmse)
    #return rmse_list

    ##linreg_mse_score = -linreg_mse_score
    ##linreg_rmse_scores = np.sqrt(linreg_mse_scores)
    ##return linreg_rmse_scores.mean()
    #lower RMSE the better
    return np.sqrt(-cross_val_score(linreg, X, y, cv=numcv, scoring='neg_mean_squared_error')).mean()

def lin_reg_model(df, feature_columns, response_vector):
    # this model is for a continuous prediction vs a 1,0 or neighbors
    X = df[feature_columns]
    y = df[response_vector]
    #X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=123)

    linreg = LinearRegression()
    linreg.fit(X, y)
    ##linreg_mse_score = cross_val_score(linreg, X, y, cv=10, scoring='neg_mean_squared_error', n_jobs=-1)

    #y_pred = linreg.predict(X_test)

    #rmse_list = []
    #rmse = np.sqrt(metrics.mean_squared_error(y_test, y_pred))
    #list_append(rmse_list, rmse)
    #return rmse_list

    ##linreg_mse_score = -linreg_mse_score
    ##linreg_rmse_scores = np.sqrt(linreg_mse_scores)
    ##return linreg_rmse_scores.mean()
    return linreg

def lin_reg_predict(df, list_feature_columns, lin_reg):
    # this model is for a continuous prediction vs a 1,0 or neighbors
    X = df[list_feature_columns]

    df_y_pred = lin_reg.predict(X)

    return df_y_pred

'''********************************************
************POLYNOMIAL REGRESSION**************
***********************************************
'''
def ply_reg_score(df, feature_columns, response_vector, deg=2, numcv=10):
    # create a model pipeline so X becomes polynomial and feeds it to the linear regression
    # http://scikit-learn.org/stable/auto_examples/model_selection/plot_underfitting_overfitting.html#sphx-glr-auto-examples-model-selection-plot-underfitting-overfitting-py
    '''
    model = Pipeline([('poly', PolynomialFeatures(degree=deg)),('linear', LinearRegression(fit_intercept=False))])
    y = 3 - 2 * x + x ** 2 - x ** 3
    model = model.fit(x[:, np.newaxis], y)
    model.named_steps['linear'].coef_
        array([ 3., -2.,  1., -1.])
    '''
    # basic polynomial regression
    '''
    X = [[0.44, 0.68], [0.99, 0.23]]
    vector = [109.85, 155.72]
    predict= [0.49, 0.18]
    poly = PolynomialFeatures(degree=2)
    X_ = poly.fit_transform(X)
    predict_ = poly.fit_transform(predict)
    clf = linear_model.LinearRegression()
    clf.fit(X_, vector)
    print clf.predict(predict_)
    '''
    # this model is for a continuous prediction vs a 1,0 or neighbors
    X = df[feature_columns] #x = np.arange(5)
    y = df[response_vector]

    scores = []
    for i in range(10):
        X_train, X_test, y_train, y_test = train_test_split(X, y)

        poly = PolynomialFeatures(degree=deg)
        X_train_poly = poly.fit_transform(X_train)
        X_test_poly = poly.fit_transform(X_test)

        linreg = LinearRegression()
        linreg.fit(X_train_poly, y_train)

        y_pred = linreg.predict(X_test_poly)

        list_append(scores, np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

    #print scores
    return (sum(scores) / float(len(scores)))

def ply_reg_model(df, feature_columns, response_vector, deg=2):
    # this model is for a continuous prediction vs a 1,0 or neighbors
    X = df[feature_columns] #x = np.arange(5)
    y = df[response_vector]

    poly = PolynomialFeatures(degree=deg)
    X_poly = poly.fit_transform(X)

    linreg = LinearRegression()
    linreg.fit(X_poly, y)

    return linreg

def ply_reg_predict(df, list_feature_columns, lin_reg, deg=2):
    # polynomial regression still uses linear regression but with polynomial features
    X = df[list_feature_columns]

    poly = PolynomialFeatures(degree=deg)
    X_poly = poly.fit_transform(X)

    df_y_pred = lin_reg.predict(X_poly)

    return df_y_pred

'''********************************************
**************LOGISTIC REGRESSION****************
***********************************************
'''
def logistic_regression(df, feature_columns, response_vector, threshold=0.3):
    # this model is for predicting 1,0 not continuous or neighbors
    X = df[feature_columns]
    y = df[response_vector]
    #X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=123)

    logreg = LogisticRegression()
    #logreg.fit(X_train, y_train)
    #logreg_score = cross_val_score(logreg, X, y, cv=10, scoring='accuracy')
    # use logreg.predict_proba(X) for scenarios where result is 0 or 1
    #y_pred = logreg.predict_proba(X_test)

    # transform household_pred to 1 or 0
    # to get it into a specific class
    #y_pred_class = np.where(y_pred_prob > threshold, 1, 0)
    #metrics.accuracy_score(y_test, y_pred_class)

    return cross_val_score(logreg, X, y, cv=10, scoring='accuracy').mean()

'''********************************************
************K NEAREST NEIGHBORS****************
***********************************************
'''
def k_nearest_neighbors(X, y):
# search for an optimal value of K for KNN
    k_range = range(1, 31)
    k_scores = []
    for k in k_range:
        knn = KNeighborsClassifier(n_neighbors=k)
        k_scores = cross_val_score(knn, X, y, cv=10, scoring='accuracy')
        list_append(k_scores, scores.mean())
    # plot the value of K for KNN (x-axis) versus the cross-validated accuracy (y-axis)
    plt.plot(k_range, k_scores, grid=True, fontsize=8, figsize=(8,5))
    plt.xlabel('Value of K for KNN')
    plt.ylabel('Cross-Validated Accuracy')
    return k_scores.max(), list_find(k_scores, k_scores.max())

    print metrics.accuracy_score(y, y_pred_class)
    column_dict = {'K': k_range, 'training error rate':training_error_rate, 'testing error rate':testing_error_rate}
    df = pd.DataFrame(column_dict).set_index('K').sort_index(ascending=True)
    df.sort_values(by='testing error rate').head()

'''********************************************
*************CORRELATION MATRIX****************
***********************************************
'''
def ml_correlation_matrix(df):
    print df.corr()
    print type(sns.heatmap(df.corr()))
    print sns.heatmap(df.corr())

'''********************************************
********************CHARTS*********************
***********************************************
'''
def ml_pair_plot(df, list_feature_cols, str_response_vector):
    # multiple scatter plots in Seaborn
    print sns.pairplot(df, x_vars=list_feature_cols, y_vars=str_response_vector, kind='reg')

def ml_time_plot(df, str_title=''):
    # built from: https://stackoverflow.com/questions/41815126/plot-datetime-date-pandas
    # library: https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.plot.html
    return df.plot(style='x', use_index=True, grid=True, legend=True, rot=60, fontsize=8, figsize=(8,5), title=str_title)


def ml_time_plot_multiple_y(df, df2, str_title=''):
    if df.empty & df2.empty:
        return False
    elif df.empty:
        plot = ml_time_plot(df2, str_title)
    elif df2.empty:
        plot = ml_time_plot(df, str_title)
    else:
        fig, ax = plt.subplots(figsize=(8,5))
        ax = df2.plot(use_index=True, style='x', ax=ax)
        plot = df.plot(style='x', use_index=True, grid=True, legend=True, rot=60, fontsize=8, figsize=(8,5), ax=ax, title=str_title)

    return plot

def ml_save_plot(plot, str_path):
    figure = plot.get_figure()
    figure.savefig(str_path, format='png', dpi=400)

'''********************************************
****************CREATE DUMMIES*****************
***********************************************
'''
def ml_create_dummies(df, series, label):
    # create dummy variables
    dummies = pd.get_dummies(series, prefix=label)
    df_remove_column_by_index(dummies, 0)
    return df_concat(df, dummies)
