from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
from NLTKProcessor import *
from MovieCrawler import *
from Recommend import *
from Graphs import *
from Prediction import *

@Request.application
def application(request):
    # Dispatcher is dictionary {<method_name>: callable}
    dispatcher["findKeyWords"] = findKeyWords
    dispatcher["cutWords"] = cutWords
    dispatcher["calcKeyWords"] = calcKeyWords
    dispatcher['crawl'] = crawl
    dispatcher['getMovieInfo'] = getMovieInfo
    dispatcher['recommendForUser'] = recommendForUser
    dispatcher['getSimilarMovies'] = getSimilarMovies
    dispatcher['get_hist_distribution_of_imdb_score'] = get_hist_distribution_of_imdb_score
    dispatcher['get_hist_distribution_of_imdb_review_count'] = get_hist_distribution_of_imdb_review_count
    dispatcher['get_cdf_of_imdb_score'] = get_cdf_of_imdb_score
    dispatcher['get_kde_of_imdb_score'] = get_kde_of_imdb_score
    dispatcher['get_kde_of_imdb_review_count'] = get_kde_of_imdb_review_count
    dispatcher['get_score_of_single_year'] = get_score_of_single_year
    dispatcher['get_box_office_of_single_year'] = get_box_office_of_single_year
    dispatcher['predict_score'] = predict_score
    dispatcher['predict_box_office'] = predict_box_office
    dispatcher['crawlForPredication'] = crawlForPredication
    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    print("Request:", request.data)
    print("Response:", response.json)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    run_simple('localhost', 8000, application)
