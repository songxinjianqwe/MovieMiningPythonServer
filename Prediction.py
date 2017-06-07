import graphlab

model_score = graphlab.load_model("rfmodel_socre")
model_box_office = graphlab.load_model("rfmodel_gross")


def predict_score(num_voted_users, budget, num_user_for_reviews, num_critic_for_reviews, duration):
    score_info = dict()
    score_info['num_voted_users'] = num_voted_users
    score_info['budget'] = budget
    score_info['num_user_for_reviews'] = num_user_for_reviews
    score_info['num_critic_for_reviews'] = num_critic_for_reviews
    score_info['duration'] = duration
    score = model_score.predict(score_info)
    return score[0]

def predict_box_office(num_critic_for_reviews, budget, num_voted_users):
    box_office_info = dict()
    box_office_info['num_critic_for_reviews'] = num_critic_for_reviews
    box_office_info['budget'] = budget
    box_office_info['title_year'] = 2017
    box_office_info['country'] = 44
    box_office_info['content_rating'] = 7
    box_office_info['num_voted_users'] = num_voted_users

    box_office = model_box_office.predict(box_office_info)
    return box_office[0]
