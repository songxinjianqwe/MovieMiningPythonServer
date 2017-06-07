# -*- coding: utf-8 -*-
import graphlab as gl

model = gl.load_model("item_similarity_small_Model")

# 返回推荐给某一用户编号的十部电影编�?
def recommendForUser(userId):
    userList = list()
    userList.insert(0, userId)
    recommendations = list(model.recommend(users=userList)['movieId'])
    return recommendations


# 返回与某部电影相似的十部电影
def getSimilarMovies(movieId):
    print movieId
    print model
    movieList = list()
    movieList.insert(0, movieId)
    similarMovies = list(model.get_similar_items(movieList, k=10)['similar'])	   
    return similarMovies
