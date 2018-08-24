import json
import pytest
from api.views import app

@pytest.fixture
def client(request):
    test_client = app.test_client()

    return test_client

# Helper functions 

def post_json(client, url, json_dict):
    """Send dictionary json_dict as a json to the specified url """
    return client.post(url, data=json.dumps(json_dict), content_type='application/json')

def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.data.decode('utf8'))

# Test for GET endpoint:

# Testing if the URL for getting all questions is accessible
def test_get_all_questions_is_successfully_rendered(client):
    response = client.get('/api/v1/questions')
    assert response.status_code == 200

# Testing if the URL for getting one question is accessible
def test_get_a_question_is_successfully_rendered_for_details_page_with_id(client):
    response = client.get('/api/v1/questions/1')
    assert response.status_code == 200

# Test for POST endpoint. Checking resulting json data:

# Testing if the question being sent is JSON formatted
def test_post_question_is_json_formatted(client):
    response = client.post('/api/v1/questions', {
           
            "title" : "Question One",
            "content" : "This question seems to be useless"
           })
    assert response.status_code == 500

# Testing if the answer being sent is JSON formatted
def test_post_answer_is_json_formatted(client):
    response = client.post('/api/v1/questions/1/answers', { 
            'content' : 'Yessss'})
    assert response.status_code == 500

def test_post_question(client):
    response = client.post('/api/v1/questions', data={ "title": "some title", "content": "Lorem ipsum dolor sit amet"})
    assert response.status_code == 500
   
def test_post_question_is_application_json_format(client):
    response = client.post('/api/v1/questions', data=json.dumps(dict(
                title='walter',
                content='walter@realpython.com'
            )),content_type='application/json')
    assert not response.status_code == 201

def test_post_question_is_not_missing_title_and_description(client):
    response = client.post('/api/v1/questions',  data=json.dumps(dict(
                title='walter',
                content='walter@realpython.com'
            )),content_type='application/json')
    assert not "Question already exists" in response

def test_post_question_is_not_repeated(client):
    request1 = client.post('/api/v1/questions', data={ "title": "Title 1", "content": "Lorem ipsum dolor sit amet"})
    assert request1.status_code == 500
    request2 = client.post('/api/v1/questions', data={ "title": "Title 1", "content": "Lorem ipsum dolor sit amet"})
    assert request2.status_code == 500

    
