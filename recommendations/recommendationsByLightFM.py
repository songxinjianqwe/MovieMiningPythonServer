import numpy as np
from lightfm import LightFM
from scipy import sparse
import pandas as pd

header = ['userId', 'movieId', 'rating', 'timestamp']
rating_data = pd.read_csv("/Users/xutianze/Downloads/ml-20m/ratings.csv", sep=",", names=header)
movie_header = ['movieId', 'movieName', 'genre']
movie_data = pd.read_csv("/Users/xutianze/Downloads/ml-20m/movies.csv", sep=",", names=movie_header)
data = pd.merge(rating_data, movie_data, on='movieId', how='left')

n_users = data['userId'].max()
n_items = data['movieId'].max()

train_data_matrix = np.zeros((n_users, n_items))

for line in data.itertuples():
    train_data_matrix[int(line[1]) - 1, int(line[2]) - 1] = float(line[3])

model = LightFM(loss="bpr", learning_rate=0.05)
model.fit(sparse.coo_matrix(train_data_matrix), epochs=30, num_threads=2)

def sample_recommendation(model, train_data, user_id):
    n_items=train_data['movieId'].max()

    scores = model.predict(user_ids=user_id, item_ids=np.arange(n_items),num_threads=2)
    top_items = movie_data['movieName'][np.argsort(-scores)]

    print("User %s" % user_id)
    print("Recommended:")

    for x in top_items[:3]:
        print("        %s" % x)


while(True):
    str = input("Enter your input: ")
    sample_recommendation(model,data,int(str))