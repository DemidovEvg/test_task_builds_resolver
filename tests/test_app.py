from fastapi.testclient import TestClient
from pydantic import TypeAdapter

import settings
from app import app
from models import Build
from repo import repo

client = TestClient(app)

settings.settings = settings.Settings(_env_file=".test.env")


def test_get_builds():
    response = client.get("/get-builds")
    assert response.status_code == 200
    assert response.json() == TypeAdapter(list[Build]).dump_python(
        repo.builds, mode="json"
    )


def test_get_builds_names():
    response = client.get("/get-builds-names")
    assert response.status_code == 200
    assert set(response.json()) == set(repo.builds_names)


def test_get_tasks_for_not_exist_build_raise_404():
    response = client.post("/get-tasks", json=dict(build="not_exist"))
    assert response.status_code == 404


def test_get_tasks_for_buy_products_build_works_well():
    response = client.post("/get-tasks", json=dict(build="buy_products"))
    assert response.status_code == 200
    build = Build(**response.json())
    assert build.name == "buy_products"
    assert build.tasks == (
        "to_collect_ones_thoughts",
        "find_a_list",
        "get_dressed",
        "find_phone",
        "check_money",
    )


def test_get_tasks_for_cook_chicken_build_works_well():
    response = client.post("/get-tasks", json=dict(build="cook_chicken"))
    assert response.status_code == 200
    build = Build(**response.json())
    assert build.name == "cook_chicken"
    assert build.tasks == (
        "to_collect_ones_thoughts",
        "find_phone",
        "find_recipe",
    )


def test_get_tasks_for_circular_build_fail():
    response = client.post("/get-tasks", json=dict(build="circular_build"))
    assert response.status_code == 400
