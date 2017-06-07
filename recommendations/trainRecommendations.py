# -*- coding: utf-8 -*-
import graphlab as gl

# 通过csv文件读取数据
items = gl.SFrame.read_csv("/Users/xutianze/Downloads/ml-20m/movies.csv")
actions = gl.SFrame.read_csv("/Users/xutianze/Downloads/ml-20m/ratings.csv")

# 清洗数据，删减过于稀疏的数据
# 此过程中删去评价次数少于5次的电影

rare_items = actions.groupby(key_columns='movieId', operations=gl.aggregate.COUNT).sort('Count')
rare_items = rare_items[rare_items['Count'] <= 5]

items = items.filter_by(rare_items['movieId'], 'movieId', exclude=True)

actions = actions[actions['rating'] >= 4]
actions = actions.filter_by(rare_items['movieId'], 'movieId', exclude=True)

items['year'] = items['title'].apply(lambda x: x[-5:-1])
items['title'] = items['title'].apply(lambda x: x[:-7])
items['genres'] = items['genres'].apply(lambda x: x.split('|'))

urls = gl.SFrame.read_csv("/Users/xutianze/Downloads/ml-20m/movie_urls.csv")
items = items.join(urls, on='movieId')
users = gl.SFrame.read_csv("/Users/xutianze/Downloads/ml-20m/user_names.csv")

training_data, validation_data = gl.recommender.util.random_split_by_user(actions, 'userId', 'movieId')

# "猜你喜欢"  推荐用户可能给出高评分的电影
# model = gl.recommender.factorization_recommender.create(observation_data=training_data, user_id='userId',
#                                                         item_id='movieId', target='rating')

model = gl.load_model("/Users/xutianze/Desktop/ranking_factorization_model")
view = model.views.overview(observation_data=training_data,
                            validation_set=validation_data,
                            user_data=users,
                            user_name_column='name',
                            item_data=items,
                            item_name_column='title',
                            item_url_column='url')
view.show()

# model.save("/Users/xutianze/Desktop/factorization_model")

# "喜欢这部电影的人也喜欢" 推荐与某部电影相似的电影
# "热门排行榜"
