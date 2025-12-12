from app.constants.rubric import classify_score


def test_classify_score_ranges():
    assert classify_score(1.5) == "Insuficiente"
    assert classify_score(2.5) == "Regular"
    assert classify_score(3.5) == "Bueno"
    assert classify_score(4.2) == "Muy Bueno"
    assert classify_score(4.8) == "Excelente"
