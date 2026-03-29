from app.auth.session import login, logout, register_user, validate_credentials


def test_validate_credentials_success():
    assert validate_credentials("admin", "admin") is True


def test_validate_credentials_failure():
    assert validate_credentials("wrong", "admin") is False


def test_login_and_logout_state_transitions():
    state = {"logged_in": False, "current_user": None, "current_role": None}

    success, _ = login(state, "admin", "admin")
    assert success is True
    assert state["logged_in"] is True
    assert state["current_role"] == "admin"

    logout(state)
    assert state["logged_in"] is False
    assert state["current_user"] is None


def test_register_user_rejects_admin_name():
    success, message = register_user("admin", "password123", "password123")
    assert success is False
    assert "cannot" in message.lower()


def test_register_user_success(monkeypatch):
    monkeypatch.setattr("app.auth.session.create_user", lambda u, p: True)
    success, message = register_user("field_agent", "password123", "password123")
    assert success is True
    assert "successful" in message.lower()
