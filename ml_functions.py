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
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

from list_functions import list_find, list_append, list_find_minimum_value_index
from df_functions import df_remove_column_by_index, df_concat, df_get_row_count
from dict_functions import dict_get_value

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
def ply_reg_score(df, feature_columns, response_vector, numcv=10):
    # create a model pipeline so X becomes polynomial and feeds it to the linear regression
    # http://scikit-learn.org/stable/auto_examples/model_selection/plot_underfitting_overfitting.html#sphx-glr-auto-examples-model-selection-plot-underfitting-overfitting-py
    # https://github.com/QCaudron/polynomial_regression/blob/master/polynomial_regression.ipynb

    # basic polynomial regression
    model = Pipeline([
        ("polynomial_features", PolynomialFeatures()),  # let's take linear x and make polynomial features from it
        ("linear_regression", LinearRegression(fit_intercept=True))  # then a linear regression on the polynomial features
    ])

    # Now we decide on what hyperparameters of the model we allow to vary.
    # In this case, we'll vary the degree of the polynomial.
    #Let's build the same model and grid search over the polynomial degree but also over whether we only want interaction terms or if we want to allow cross-terms. Our ground truth is a degree-3 polynomial with both cross- and interaction-terms.
    parameters = {
        "polynomial_features__degree": [1, 2, 3, 4, 5],
        "polynomial_features__interaction_only": [True, False]
    }

    # this model is for a continuous prediction vs a 1,0 or neighbors
    X = df[feature_columns] #x = np.arange(5)
    y = df[response_vector]

    gridsearch = GridSearchCV(
    model,  # our pipeline
    parameters,  # the parameters of the pipeline that we want to vary
    #n_jobs=-1,  # use all cores on our computer
    scoring="neg_mean_squared_error",  # evaluate the model using mean squared error
    cv=numcv  # and perform 5-fold cross-validation to score the model
    )

    gridsearch.fit(X, y)  # sklearn wants *observations* in the first axis and *features* in the second axis

    scores = gridsearch.cv_results_['mean_test_score']
    #print results
    scores[:] = [np.sqrt(abs(x)) for x in scores]

    #print("Best RMSE score ( lower is better ) : {}".format(gridsearch.best_score_))
    #print("Best hyperparameters : {}".format(gridsearch.best_params_))

    #best_model = gridsearch.best_estimator_
    #print(best_model)

    # Predict y_hat from our input features
    #df["yhat"] = gridsearch.best_estimator_.predict(df[["rooms", "baths", "sqft"]])

    #print results
    return [gridsearch.best_score_, dict_get_value(gridsearch.best_params_, 'polynomial_features__degree'), dict_get_value(gridsearch.best_params_, 'polynomial_features__interaction_only')]

def ply_reg_model(df, feature_columns, response_vector, numcv=10, degree=[1,2,3,4,5]):
    # https://github.com/QCaudron/polynomial_regression/blob/master/polynomial_regression.ipynb

    model = Pipeline([
        ("polynomial_features", PolynomialFeatures()),  # let's take linear x and make polynomial features from it
        ("linear_regression", LinearRegression(fit_intercept=True))  # then a linear regression on the polynomial features
    ])

    parameters = {
        "polynomial_features__degree": [degree],
        "polynomial_features__interaction_only": [True, False]
    }

    # this model is for a continuous prediction vs a 1,0 or neighbors
    X = df[feature_columns] #x = np.arange(5)
    y = df[response_vector]

    gridsearch = GridSearchCV(
    model,  # our pipeline
    parameters,  # the parameters of the pipeline that we want to vary
    #n_jobs=-1,  # use all cores on our computer
    scoring="neg_mean_squared_error",  # evaluate the model using mean squared error
    cv=numcv  # and perform 5-fold cross-validation to score the model
    )

    gridsearch.fit(X, y)  # sklearn wants *observations* in the first axis and *features* in the second axis

    return gridsearch.best_estimator_

def ply_reg_predict(df, list_feature_columns, best_estimator):
    # polynomial regression still uses linear regression but with polynomial features
    X = df[list_feature_columns]

    df_y_pred = best_estimator.predict(X)

    return df_y_pred

'''********************************************
***************DECISION TREE*******************
***********************************************
'''
def decision_tree_score(df, list_feature_columns, str_response_vector, int_cv=10):
    if len(df) < int_cv:
        int_cv = int(len(df) * .75)
    X = df[list_feature_columns]
    y = df[str_response_vector]
    treereg = DecisionTreeRegressor()
    return np.sqrt(-cross_val_score(treereg, X, y, cv=int_cv, scoring='neg_mean_squared_error')).mean()

def decision_tree_best_score_depth(df, list_feature_columns, str_response_vector, int_range=10, int_cv=10):
    if len(df) < int_cv:
        int_cv = int(len(df) * .75)

    X = df[list_feature_columns]
    y = df[str_response_vector]

    # list of values to try
    max_depth_range = range(1, int_range)

    # list to store the average RMSE for each value of max_depth
    scores = []

    # use CV with each value of max_depth
    for depth in max_depth_range:
        treereg = DecisionTreeRegressor(max_depth=depth)
        list_append(scores ,[(np.sqrt(-cross_val_score(treereg, X, y, cv=int_cv, scoring='neg_mean_squared_error')).mean()), depth])

    best_depth_index = list_find_minimum_value_index(scores)
    #print scores[best_depth_index]
    return scores[best_depth_index]

def decision_tree_model(df, list_feature_columns, str_response_vector, depth=None):
    X = df[list_feature_columns]
    y = df[str_response_vector]
    treereg = DecisionTreeRegressor(max_depth=depth)
    treereg.fit(X, y)
    return treereg

def decision_tree_predict(df, list_feature_columns, treereg):
    X = df[list_feature_columns]
    df_y_pred = treereg.predict(X)
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
