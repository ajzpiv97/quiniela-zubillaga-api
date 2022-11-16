def get_score(actual_score: str, predicted_score: str) -> int:
    score_a = [int(score) for score in actual_score.strip().split("-")]
    score_p = [int(score) for score in predicted_score.strip().split("-")]
    score = 0
    # rule for perfect match
    if score_a[0] == score_p[0] and score_a[1] == score_p[1]:
        return 5
    # rule for same winner
    if (score_p[0] > score_p[1] and score_a[0] > score_a[1]) or (score_p[1] > score_p[0] and score_a[1] > score_a[0]):
        score += 3
    elif score_p[0] == score_p[1] and score_a[0] == score_a[1]:
        score += 3

    # score has the correct number of goals
    if score_p[0] + score_p[1] == score_a[0] + score_a[1]:
        score += 2

    return score
