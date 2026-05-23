import sys
import os
import time
import subprocess
import signal
import requests
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.security import create_access_token
from app.usuarios.repository.usuario_repo import UserRepository

BASE_URL = "http://127.0.0.1:8000"
ADMIN_TOKEN = None
CREATED_USER_ID = None


def _seed_admin():
    UserRepository.clear()

    from app.usuarios.domain.schemas import UserCreate
    from app.core.security import hash_password

    admin_data = UserCreate(
        nombre="Admin Test",
        correo="admin_test@correo.uts.edu.co",
        password="admin123",
        rol="ADMINISTRADOR",
    )
    admin = UserRepository().create(admin_data, hash_password("admin123"))
    global ADMIN_TOKEN
    ADMIN_TOKEN = create_access_token(
        {"id": admin.id, "correo": admin.correo, "rol": admin.rol}
    )


def _wait_for_server(timeout=15):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(f"{BASE_URL}/", timeout=2)
            if r.status_code == 200:
                return True
        except requests.ConnectionError:
            time.sleep(0.5)
    return False


@pytest.fixture(scope="module", autouse=True)
def uvicorn_server():
    _seed_admin()

    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    ready = _wait_for_server()
    assert ready, "Uvicorn no arrancó a tiempo"

    yield

    proc.send_signal(signal.CTRL_C_EVENT if sys.platform == "win32" else signal.SIGINT)
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()

    UserRepository.clear()


def test_crear_y_eliminar_usuario():
    headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}

    payload = {
        "nombre": "Test Uvicorn",
        "correo": "test_uvicorn@correo.uts.edu.co",
        "password": "pass123",
        "rol": "ESTUDIANTE",
    }

    create_resp = requests.post(
        f"{BASE_URL}/api/v1/usuarios", json=payload, headers=headers, timeout=5
    )
    assert create_resp.status_code == 201
    create_data = create_resp.json()
    assert create_data["success"] is True
    assert create_data["data"]["correo"] == payload["correo"]
    assert create_data["data"]["rol"] == payload["rol"]

    user_id = create_data["data"]["id"]
    global CREATED_USER_ID
    CREATED_USER_ID = user_id

    delete_resp = requests.delete(
        f"{BASE_URL}/api/v1/usuarios/{user_id}", headers=headers, timeout=5
    )
    assert delete_resp.status_code == 200
    delete_data = delete_resp.json()
    assert delete_data["success"] is True
    assert delete_data["message"] == "Usuario eliminado correctamente"

    verify_resp = requests.delete(
        f"{BASE_URL}/api/v1/usuarios/{user_id}", headers=headers, timeout=5
    )
    assert verify_resp.status_code == 404
