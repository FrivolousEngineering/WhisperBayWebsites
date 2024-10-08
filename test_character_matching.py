import pytest
from fastapi.testclient import TestClient

from Server.main import characters, app

client = TestClient(app)


@pytest.mark.parametrize("character", characters)
def test_character_matching(character):
    # Extract the character attributes for the test
    gender = character.gender_run1
    age = character.age
    profession = character.profession
    relation_status = character.relationship_status
    starsign = character.star_sign

    # Create the simulated form data for the character
    form_data = {
        "question_1_answer": str(age),
        "question_2_answer": gender,
        "question_3_answer": profession,
        "question_4_answer": relation_status,
        "question_5_answer": starsign
    }

    form_data = {
        "question_1_answer": str(age),
        "question_2_answer": gender,
        "question_3_answer": "",
        "question_4_answer": "",
        "question_5_answer": starsign
    }

    # Send the request to the endpoint
    response = client.post("/evaluateAnswers/", data=form_data)

    # Check if the response is successful
    assert response.status_code == 200
    response_data = response.json()

    # Extract the best match from the response
    best_match = response_data["match"]

    # Assert the best match is the character itself
    expected_match = f"{character.first_name} {character.last_name}"
    assert best_match == expected_match, f"Character {character.first_name} did not match correctly, they matched on {best_match} instead"
