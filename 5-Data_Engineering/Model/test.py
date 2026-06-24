import requests

def test_predict_endpoint():
    url = 'http://localhost:8000/predict'  
    data = {'data': [[100, 100, 200]]} 
    
    response = requests.get(url, json=data)
    assert response.status_code == 200
    assert 'prediction' in response.json()
