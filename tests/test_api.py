
import importlib.util
import pathlib
import json

import pytest

APP_DIR = pathlib.Path(__file__).resolve().parents[1] / "app"

# Discover Flask app version files (only those that contain Flask code we generated)
VERSION_FILES = [
    "ACEest_Fitness.py",
    "ACEest_Fitness-V1.1.py",
    "ACEest_Fitness-V1.2.py",
    "ACEest_Fitness-V1.2.1.py",
    "ACEest_Fitness-V1.2.2.py",
    "ACEest_Fitness-V1.2.3.py",
    "ACEest_Fitness-V1.3.py",
]

def _load_app(module_path: pathlib.Path):
    spec = importlib.util.spec_from_file_location("aceest_app", str(module_path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore
    return getattr(mod, "app")

@pytest.mark.parametrize("fname", VERSION_FILES)
def test_health_and_home(fname):
    mpath = APP_DIR / fname
    assert mpath.exists(), f"Missing app file: {fname}"
    app = _load_app(mpath)
    client = app.test_client()

    # /health
    res = client.get("/health")
    assert res.status_code == 200
    assert res.data.decode().strip() == "OK"

    # /
    res = client.get("/")
    assert res.status_code == 200
    data = res.get_json()
    assert "app" in data and "version" in data

@pytest.mark.parametrize("fname", VERSION_FILES[1:])  # >= v1.1 has /bmi
def test_bmi(fname):
    mpath = APP_DIR / fname
    app = _load_app(mpath)
    client = app.test_client()

    res = client.get("/bmi?height_cm=180&weight_kg=81")
    assert res.status_code == 200
    data = res.get_json()
    assert pytest.approx(data["bmi"], 0.1) == 25.0

@pytest.mark.parametrize("fname", VERSION_FILES[2:])  # >= v1.2 has workouts
def test_workouts_crud(fname):
    mpath = APP_DIR / fname
    app = _load_app(mpath)
    client = app.test_client()

    # initially empty
    res = client.get("/workouts")
    assert res.status_code == 200
    data = res.get_json()
    assert data["count"] == 0

    # add
    res = client.post("/workouts", json={"type": "Running", "minutes": 30})
    assert res.status_code in (201, 200)

    res = client.get("/workouts")
    data = res.get_json()
    assert data["count"] == 1
    assert data["items"][0]["type"] == "Running"

@pytest.mark.parametrize("fname", VERSION_FILES[4:])  # >= v1.2.2 has stats
def test_stats(fname):
    mpath = APP_DIR / fname
    app = _load_app(mpath)
    client = app.test_client()

    client.post("/workouts", json={"type": "Run", "minutes": 30})
    client.post("/workouts", json={"type": "Bike", "minutes": 20})
    res = client.get("/stats")
    assert res.status_code == 200
    data = res.get_json()
    assert data["total_minutes"] == 50
    assert data["by_type"]["Run"] == 30
