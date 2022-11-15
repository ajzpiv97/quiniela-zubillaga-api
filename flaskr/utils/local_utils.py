


def get_score(actual_score, predicted_score):
    score_a = actual_score.split("-")
    score_p = predicted_score.split("-")
    score = 0
    ## rule for perfect match
    if (score_a[0] == score_p[0] and score_a[1] == score_p[1]):
        return 5
    ## rule for same winner
    if (score_p[0] > score_p[1] and score_a[0] > score_a[1]) or (score_p[1] > score_p[0] and score_a[1] > score_a[0]):
        score = score + 3
    elif (score_p[0] == score_p[1] and score_a[0] == score_a[1]):
        score = score + 3

    ##score has the correct number of goals
    if (int(score_p[0]) + int(score_p[1]) == int(score_a[0]) + int(score_a[1])):
        score = score + 2

    return score