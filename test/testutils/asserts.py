from fastapi import Response

def assert_error_response(response: Response, status_code: int):
    json = response.json()
    assert response.status_code == status_code
    assert "detail" in json and len(json["detail"]) > 0