"""基本健康檢查測試。"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_generate_comic() -> None:
    response = client.post(
        "/comics/generate",
        json={"user_id": "test-user", "text": "今天去公園散步，還餵了鴿子。"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "test-user"
    assert len(data["panels"]) >= 1
    # 確認有無障礙口述內容
    assert data["narration"]
