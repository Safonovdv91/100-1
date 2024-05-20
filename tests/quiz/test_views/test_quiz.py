from aiohttp.test_utils import TestClient

from app.quiz.models import Question


class TestQuestionAddView:
    async def test_unauthorized(self, cli: TestClient) -> None:
        response = await cli.get("/quiz.questions_add")

        assert response.status == 401, f"response = {response}"

        data = await response.json()
        assert data["status"] == "unauthorized"

    async def test_success(
        self, auth_cli: TestClient, question_1: Question
    ) -> None:
        response = await auth_cli.post(
            "/quiz.questions_add",
            json={
                "title": "Что в тяжелой коробке. что в ней?",
                "theme_id": 1,
                "answers": [
                    {"id": 0, "title": "Еду", "score": 10},
                    {"id": 0, "title": "холодильник", "score": 20},
                    {"id": 0, "title": "доллары", "score": 30},
                    {"id": 0, "title": "телевизор", "score": 40},
                ],
            },
        )
        assert response.status == 200

        data = await response.json()
        assert data == {
            "status": "ok",
            "data": {
                "id": 2,
                "title": "Что в тяжелой коробке. что в ней?",
                "theme_id": question_1.theme_id,
                "answers": [
                    {"id": 5, "title": "Еду", "score": 10},
                    {"id": 6, "title": "холодильник", "score": 20},
                    {"id": 7, "title": "доллары", "score": 30},
                    {"id": 8, "title": "телевизор", "score": 40},
                ],
            },
        }

    async def test_bad_score(
        self, auth_cli: TestClient, question_1: Question
    ) -> None:
        response = await auth_cli.post(
            "/quiz.questions_add",
            json={
                "id": 0,
                "title": "два человека тащут тяжелую коробку. что в ней?",
                "theme_id": 1,
                "answers": [
                    {"id": 0, "title": "Еду", "score": 25},
                    {"id": 0, "title": "холодильник", "score": 25},
                    {"id": 0, "title": "доллары", "score": 25},
                    {"id": 0, "title": "телевизор", "score": 26},
                ],
            },
        )
        assert response.status == 400, response.json()

        data = await response.json()
        assert (
            data.get("message") == "Сумма очков всех ответов должна "
            "быть равна 100, текущая сумма: 101"
        )

    async def test_empty_title(
        self, auth_cli: TestClient, question_1: Question
    ) -> None:
        response = await auth_cli.post(
            "/quiz.questions_add",
            json={
                "id": 0,
                "title": "",
                "theme_id": 1,
                "answers": [
                    {"id": 0, "title": "Еду", "score": 25},
                    {"id": 0, "title": "холодильник", "score": 25},
                    {"id": 0, "title": "доллары", "score": 25},
                    {"id": 0, "title": "телевизор", "score": 26},
                ],
            },
        )
        assert response.status == 400, response.json()

    async def test_empty_answers(
        self, auth_cli: TestClient, question_1: Question
    ) -> None:
        response = await auth_cli.post(
            "/quiz.questions_add",
            json={
                "id": 0,
                "title": "ЧТо в ящике?",
                "theme_id": 1,
                "answers": [
                    {"id": 0, "title": "Еду", "score": 50},
                ],
            },
        )
        assert response.status == 400, response.json()


class TestQuestionDeleteByIdView:
    async def test_unauthorized(self, cli: TestClient) -> None:
        response = await cli.get("/quiz.questions_delete_by_id")
        assert response.status == 401

        data = await response.json()
        assert data["status"] == "unauthorized"


class TestQuestionListView:
    async def test_unauthorized(self, cli: TestClient) -> None:
        response = await cli.get("/quiz.questions_list")
        assert response.status == 401

        data = await response.json()
        assert data["status"] == "unauthorized"

    async def test_success_no_questions(
        self, auth_cli: TestClient, theme_1, question_1
    ) -> None:
        response = await auth_cli.get(
            "/quiz.questions_list", params={"theme_id": 1}
        )
        assert response.status == 200

        data = await response.json()
        assert data == {
            "data": {
                "questions": [
                    {
                        "answers": [
                            {"id": 1, "score": 43, "title": "Еду"},
                            {"id": 2, "score": 27, "title": "свадьбу"},
                            {"id": 3, "score": 15, "title": "природу"},
                            {"id": 4, "score": 15, "title": "животных"},
                        ],
                        "id": 1,
                        "theme_id": 1,
                        "title": "Кого или что чаще всего снимает " "фотограф?",
                    }
                ]
            },
            "status": "ok",
        }


class TestThemeListView:
    async def test_unauthorized(self, cli: TestClient) -> None:
        response = await cli.get("/quiz.themes_list")
        assert response.status == 401

        data = await response.json()
        assert data["status"] == "unauthorized"

    async def test_success_themes_list_empty(
        self, auth_cli: TestClient
    ) -> None:
        response = await auth_cli.get("/quiz.themes_list")
        assert response.status == 200

        data = await response.json()
        assert data == {
            "status": "ok",
            "data": {"themes": []},
        }

    async def test_success_themes_list_default_theme(
        self, auth_cli: TestClient, theme_1
    ) -> None:
        response = await auth_cli.get("/quiz.themes_list")
        assert response.status == 200

        data = await response.json()
        assert data == {
            "status": "ok",
            "data": {
                "themes": [
                    {
                        "id": theme_1.id,
                        "title": theme_1.title,
                        "description": theme_1.description,
                    }
                ]
            },
        }


class TestThemeDeleteByIdView:
    async def test_unauthorized(self, cli: TestClient) -> None:
        response = await cli.get("/quiz.themes_delete_by_id")
        assert response.status == 401

        data = await response.json()
        assert data["status"] == "unauthorized"


class TestThemeAddView:
    async def test_unauthorized(self, cli: TestClient) -> None:
        response = await cli.get("/quiz.themes_add")
        assert response.status == 401

        data = await response.json()
        assert data["status"] == "unauthorized"
