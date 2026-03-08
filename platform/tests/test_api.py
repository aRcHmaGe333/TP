def register_user(client, display_name: str, password: str = "pass123") -> dict:
    response = client.post(
        "/api/register",
        json={"display_name": display_name, "password": password, "email": f"{display_name}@x.test"},
    assert response.status_code == 200, response.text
    return response.json()
def login_user(client, display_name: str, password: str = "pass123") -> dict:
    response = client.post("/api/login", json={"display_name": display_name, "password": password})
def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}
def test_register_login_and_me(client):
    reg = register_user(client, "alice")
    assert reg["display_name"] == "alice"
    assert "token" in reg
    login = login_user(client, "alice")
    me = client.get("/api/me", headers=auth_headers(login["token"]))
    assert me.status_code == 200
    data = me.json()
    assert data["display_name"] == "alice"
    assert data["is_admin"] is False
def test_idea_flow_signature_changes_and_permissions(client):
    alice = register_user(client, "alice")
    bob = register_user(client, "bob")
    create = client.post(
        "/api/ideas",
        headers=auth_headers(alice["token"]),
        json={"title": "Idea A", "body": "Body A", "tags": ["pilot"]},
    assert create.status_code == 200
    idea = create.json()
    idea_id = idea["id"]
    initial_signature = idea["signature"]
    edit = client.put(
        f"/api/ideas/{idea_id}",
        json={"title": "Idea A+", "body": "Body A+", "tags": ["pilot", "v2"]},
    assert edit.status_code == 200
    edited_signature = edit.json()["signature"]
    assert edited_signature != initial_signature
    forbidden_status = client.patch(
        f"/api/ideas/{idea_id}/status",
        headers=auth_headers(bob["token"]),
        json={"status": "acknowledged"},
    assert forbidden_status.status_code == 403
    status = client.patch(
    assert status.status_code == 200
    status_signature = status.json()["signature"]
    assert status_signature != edited_signature
    vote = client.post(
        f"/api/ideas/{idea_id}/vote",
        json={"value": 1},
    assert vote.status_code == 200
    assert vote.json()["score"] == 1
    comment = client.post(
        f"/api/ideas/{idea_id}/comments",
        json={"body": "Looks good"},
    assert comment.status_code == 200
    idea_b = client.post(
        json={"title": "Idea B", "body": "Body B", "tags": []},
    assert idea_b.status_code == 200
    idea_b_id = idea_b.json()["id"]
    merge = client.post(
        f"/api/ideas/{idea_b_id}/merge",
        json={"target_id": idea_id},
    assert merge.status_code == 200
    assert merge.json()["merged_into_id"] == idea_id
def test_status_transition_rules_and_admin_override(client):
    admin = register_user(client, "admin")
    assert admin["is_admin"] is True
    created = client.post(
        json={"title": "Status test", "body": "Body", "tags": []},
    idea_id = created.json()["id"]
    invalid_jump = client.patch(
        json={"status": "resolved"},
    assert invalid_jump.status_code == 400
    admin_override = client.patch(
        headers=auth_headers(admin["token"]),
    assert admin_override.status_code == 200
    assert admin_override.json()["status"] == "resolved"
def test_pagination_caps_and_summary(client):
    user = register_user(client, "alice")
    for idx in range(3):
        created = client.post(
            "/api/ideas",
            headers=auth_headers(user["token"]),
            json={"title": f"Idea {idx}", "body": "Body", "tags": []},
        assert created.status_code == 200
    ideas = client.get("/api/ideas?limit=50")
    assert ideas.status_code == 200
    assert len(ideas.json()) == 2
    first_idea_id = ideas.json()[0]["id"]
    for _ in range(3):
        commented = client.post(
            f"/api/ideas/{first_idea_id}/comments",
            json={"body": "Comment"},
        assert commented.status_code == 200
    comments = client.get(f"/api/ideas/{first_idea_id}/comments?limit=99")
    assert comments.status_code == 200
    assert len(comments.json()) == 2
    summary = client.get("/api/reports/summary")
    assert summary.status_code == 200
    payload = summary.json()
    assert payload["total_ideas"] == 3
    assert "counts_by_status" in payload
def test_admin_export_and_audit_protection(client):
        headers=auth_headers(user["token"]),
        json={"title": "Export test", "body": "Body", "tags": []},
    client.patch(
    denied_export = client.get("/api/reports/export.csv", headers=auth_headers(user["token"]))
    assert denied_export.status_code == 403
    export_ok = client.get("/api/reports/export.csv", headers=auth_headers(admin["token"]))
    assert export_ok.status_code == 200
    assert "row_type" in export_ok.text
    assert "status_event" in export_ok.text
    denied_audit = client.get("/api/audit-events", headers=auth_headers(user["token"]))
    assert denied_audit.status_code == 403
    audit_ok = client.get("/api/audit-events?limit=10", headers=auth_headers(admin["token"]))
    assert audit_ok.status_code == 200
    assert isinstance(audit_ok.json(), list)
    assert len(audit_ok.json()) >= 1
def test_request_size_guard(client):
    big_password = "x" * 5000
        json={"display_name": "large", "password": big_password, "email": "large@x.test"},
    assert response.status_code == 413
