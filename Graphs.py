# coding=utf-8
import pandas as pd
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import scipy.stats
import requests

r = requests.get('http://flyweight.newsong.me:8080/MovieMiningServer/movies')
df = pd.read_json(r.text)
df.drop(['gross', 'doubanReviewTime', 'doubanScore', 'directories'], axis=1)
df['year'] = pd.to_datetime(df['releaseTime']).dt.year
df['month'] = pd.to_datetime(df['releaseTime']).dt.month

df_box_office = pd.read_csv("movie_metadata.csv")
df_box_office = df_box_office[df_box_office['title_year'] > 0]
df_box_office['title_year'] = df_box_office['title_year'].astype(int)


# 返回imdb评分分布的直方图分布
def get_hist_distribution_of_imdb_score(bins=50, normed=True):
    tup = plt.hist(df['imdbScore'], bins=bins, normed=normed)
    list1 = list()
    list2 = list()
    for x in tup[1]:
        list1.append(round(x, 3))
    for x in tup[0]:
        list2.append(round(x, 3))
    hist_distribution = dict()
    hist_distribution['x_axis'] = list1
    hist_distribution['y_axis'] = list2

    return json.dumps(hist_distribution)


# 返回imdb评价人数分布的直方图分布
def get_hist_distribution_of_imdb_review_count(bins=50, normed=True):
    tup = plt.hist(df[df['imdbReviewTime'] < 250000]['imdbReviewTime'], bins=bins, normed=normed)
    list1 = list()
    list2 = list()
    for x in tup[1]:
        list1.append(round(x, 3))
    for x in tup[0]:
        list2.append(x)
    hist_distribution = dict()
    hist_distribution['x_axis'] = list1
    hist_distribution['y_axis'] = list2
    return json.dumps(hist_distribution)


# 返回imdb评分分布的概率分布函数(Cumulative distribution function函数)
def get_cdf_of_imdb_score():
    hist = np.histogram(df['imdbScore'], bins=100)
    hist_dist = scipy.stats.rv_histogram(hist)

    x = 1
    cdf_dic = dict()
    while x <= 10:
        cdf_dic[round(x, 1)] = hist_dist.cdf(x)
        x += 0.1

    return json.dumps(cdf_dic)


# 返回imdb评分分布的核密度拟合(Kernel Density Estimate函数) 参见图4
def get_kde_of_imdb_score():
    kde = scipy.stats.gaussian_kde(df['imdbScore'])

    x = 1
    kde_dic = dict()
    while x <= 10:
        kde_dic[round(x, 1)] = kde.evaluate(x)[0]
        x += 0.1

    return json.dumps(kde_dic)


# 返回imdb评价人数的核密度拟合(Kernel Density Estimate函数)
def get_kde_of_imdb_review_count():
    kde = scipy.stats.gaussian_kde(df[df['imdbReviewTime'] < 25000]['imdbReviewTime'])

    x = -5000
    kde_dic = dict()
    while x <= 30000:
        kde_dic[round(x)] = kde.evaluate(x)[0]
        x += 250

    return json.dumps(kde_dic)


# 返回区间内每年的全部评分（用于画箱线图或者提琴图）
def get_score_of_single_year(start_year=2000, end_year=2016):
    year_dic = dict()

    for year in range(start_year, end_year):
        year_dic[year] = df[df['year'] == year]['imdbScore'].values.tolist()

    return json.dumps(year_dic)


# 返回区间内每年的全部票房（用于画箱线图或者提琴图）
def get_box_office_of_single_year(start_year=2000, end_year=2016):
    year_dic = dict()

    for year in range(start_year, end_year):
        year_dic[year] = df_box_office[df_box_office['title_year'] == year]['gross'].dropna().astype(int).values.tolist()

    return json.dumps(year_dic)
