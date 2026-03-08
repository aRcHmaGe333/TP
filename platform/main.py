from __future__ import annotations
import csv
import io
import json
import statistics
from pathlib import Path
from typing import Dict, List, Optional
from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, func, select
    from . import auth, config
    from .database import get_session, init_db
    from .models import AuditEvent, Comment, Idea, MergeRecord, User, Vote
    from .rate_limit import SlidingWindowRateLimiter
    from .schemas import (
        AuditEventResponse,
        CommentCreate,
        CommentResponse,
        IdeaCreate,
        IdeaResponse,
        IdeaStatus,
        IdeaStatusUpdate,
        IdeaUpdate,
        LoginRequest,
        MergeRequest,
        RegisterRequest,
        ReportSummaryResponse,
        TokenResponse,
        TopIdeaSummary,
        UserResponse,
        VoteRequest,
    import auth
    from database import get_session, init_db
    from models import AuditEvent, Comment, Idea, MergeRecord, User, Vote
    from rate_limit import SlidingWindowRateLimiter
    from schemas import (
BASE_DIR = Path(__file__).resolve().parent
STATUS_FLOW = [
    IdeaStatus.submitted.value,
    IdeaStatus.acknowledged.value,
    IdeaStatus.in_progress.value,
    IdeaStatus.resolved.value,
]
app = FastAPI(title="Innovative Feedback Platform", version="0.2.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
origins = config.get_cors_origins()
if not origins:
    origins = ["http://localhost:8000"] if config.is_dev_env() else []
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
rate_limiter = SlidingWindowRateLimiter()
@app.middleware("http")
async def request_size_guard(request: Request, call_next):
    if request.method in {"POST", "PUT", "PATCH"}:
        content_length = request.headers.get("content-length")
        if content_length:
            try:
                body_size = int(content_length)
            except ValueError:
                body_size = 0
            if body_size > config.get_max_request_bytes():
                return JSONResponse(
                    status_code=413,
                    content={"detail": "Request body exceeds PLATFORM_MAX_REQUEST_BYTES"},
    return await call_next(request)
@app.on_event("startup")
def on_startup() -> None:
    config.validate_runtime_config()
    init_db()
def get_token_from_request(request: Request) -> Optional[str]:
    header = request.headers.get("Authorization")
    if header and header.lower().startswith("bearer "):
        return header.split(" ", 1)[1]
    return None
def get_current_user(request: Request, session: Session = Depends(get_session)) -> User:
    token = get_token_from_request(request)
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    user_id = auth.load_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
def user_is_admin(user: User) -> bool:
    return bool(user.is_admin) or user.display_name.lower() in config.get_admin_display_names()
def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if not user_is_admin(current_user):
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user
def to_user_response(user: User) -> UserResponse:
    return UserResponse(
        id=user.id,
        display_name=user.display_name,
        email=user.email,
        fingerprint=user.fingerprint,
        is_admin=user_is_admin(user),
        created_at=user.created_at,
def to_comment_response(comment: Comment, author: User) -> CommentResponse:
    return CommentResponse(
        id=comment.id,
        body=comment.body,
        author=to_user_response(author),
        signature=comment.signature,
        created_at=comment.created_at,
def resolve_limit(limit: Optional[int]) -> int:
    default_page = config.get_default_page_size()
    max_page = config.get_max_page_size()
    if limit is None:
        return default_page
    return min(limit, max_page)
def get_client_ip(request: Request) -> str:
    if request.client and request.client.host:
        return request.client.host
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",", 1)[0].strip()
    return "unknown"
def enforce_rate_limit(action: str, actor_key: str, limit: int) -> None:
    limits = config.get_rate_limits()
    if not rate_limiter.allow(f"{action}:{actor_key}", limit, limits.window_seconds):
        raise HTTPException(status_code=429, detail=f"Rate limit exceeded for {action}")
def to_idea_response(idea: Idea, author: User, session: Session) -> IdeaResponse:
    score = session.exec(
        select(func.coalesce(func.sum(Vote.value), 0)).where(Vote.idea_id == idea.id)
    ).one()
    comment_count = session.exec(
        select(func.count()).select_from(Comment).where(Comment.idea_id == idea.id)
    tags = [tag for tag in idea.tags.split(",") if tag]
    return IdeaResponse(
        id=idea.id,
        title=idea.title,
        body=idea.body,
        tags=tags,
        merged_into_id=idea.merged_into_id,
        status=IdeaStatus(idea.status),
        status_updated_at=idea.status_updated_at,
        status_updated_by=idea.status_updated_by,
        signature=idea.signature,
        score=score,
        created_at=idea.created_at,
        updated_at=idea.updated_at,
        comment_count=comment_count,
def sign_idea(idea: Idea, actor: User) -> str:
    payload = {
        "title": idea.title,
        "body": idea.body,
        "tags": idea.tags,
        "merged_into_id": idea.merged_into_id,
        "status": idea.status,
        "actor": actor.fingerprint,
        "ts": idea.updated_at.isoformat(),
    return auth.make_signature(payload, actor.signing_key)
def sign_comment(comment: Comment, author: User) -> str:
        "body": comment.body,
        "author": author.fingerprint,
        "ts": comment.created_at.isoformat(),
        "idea": comment.idea_id,
    return auth.make_signature(payload, author.signing_key)
def parse_audit_details(details_json: str) -> Dict[str, object]:
        parsed = json.loads(details_json)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass
    return {}
def to_audit_event_response(event: AuditEvent) -> AuditEventResponse:
    return AuditEventResponse(
        id=event.id,
        event_type=event.event_type,
        user_id=event.user_id,
        target_type=event.target_type,
        target_id=event.target_id,
        ip_address=event.ip_address,
        details=parse_audit_details(event.details_json),
        created_at=event.created_at,
def record_audit_event(
    session: Session,
    request: Request,
    *,
    event_type: str,
    user_id: Optional[int] = None,
    target_type: Optional[str] = None,
    target_id: Optional[int] = None,
    details: Optional[Dict[str, object]] = None,
) -> None:
    session.add(
        AuditEvent(
            event_type=event_type,
            user_id=user_id,
            target_type=target_type,
            target_id=target_id,
            ip_address=get_client_ip(request),
            details_json=json.dumps(details or {}, separators=(",", ":"), sort_keys=True),
def validate_status_transition(current: str, new: str, is_admin: bool) -> None:
    if current == new:
    if current not in STATUS_FLOW or new not in STATUS_FLOW:
        raise HTTPException(status_code=400, detail="Invalid status value")
    if is_admin:
    current_idx = STATUS_FLOW.index(current)
    new_idx = STATUS_FLOW.index(new)
    if new_idx < current_idx:
        raise HTTPException(status_code=400, detail="Cannot move status backwards")
    if new_idx > current_idx + 1:
        raise HTTPException(status_code=400, detail="Status transition is too large")
@app.get("/", response_class=HTMLResponse)
def read_root() -> str:
    index_path = BASE_DIR / "static" / "index.html"
    return index_path.read_text(encoding="utf-8")
@app.get("/api/spec")
def read_spec() -> Dict[str, str]:
    spec_path = BASE_DIR / "segment_000.md"
    if not spec_path.exists():
        raise HTTPException(status_code=404, detail="Spec document not found")
    return {"body": spec_path.read_text(encoding="utf-8")}
@app.post("/api/register", response_model=TokenResponse)
def register(
    payload: RegisterRequest,
    session: Session = Depends(get_session),
):
    client_ip = get_client_ip(request)
    enforce_rate_limit("register_ip", client_ip, limits.register_per_ip)
    existing = session.exec(select(User).where(User.display_name == payload.display_name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Display name already taken")
    salt_b64, hash_b64 = auth.hash_password(payload.password)
    signing_key = auth.build_signing_key()
    user = User(
        display_name=payload.display_name,
        email=payload.email,
        password_hash=hash_b64,
        password_salt=salt_b64,
        signing_key=signing_key,
        fingerprint=auth.fingerprint(signing_key),
        is_admin=payload.display_name.lower() in config.get_admin_display_names(),
    session.add(user)
    session.commit()
    session.refresh(user)
    record_audit_event(
        session,
        request,
        event_type="user_register",
        user_id=user.id,
        target_type="user",
        target_id=user.id,
        details={"display_name": user.display_name},
    token = auth.create_token(user.id)
    return TokenResponse(**to_user_response(user).dict(), token=token)
@app.post("/api/login", response_model=TokenResponse)
def login(
    payload: LoginRequest,
    enforce_rate_limit("login_ip", client_ip, limits.login_per_ip)
    user = session.exec(select(User).where(User.display_name == payload.display_name)).first()
    if not user or not auth.verify_password(payload.password, user.password_salt, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if payload.display_name.lower() in config.get_admin_display_names() and not user.is_admin:
        user.is_admin = True
        session.add(user)
        event_type="user_login",
@app.get("/api/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)) -> UserResponse:
    return to_user_response(current_user)
@app.post("/api/ideas", response_model=IdeaResponse)
def create_idea(
    payload: IdeaCreate,
    current_user: User = Depends(get_current_user),
    enforce_rate_limit("idea_ip", client_ip, limits.idea_per_ip)
    enforce_rate_limit("idea_user", str(current_user.id), limits.idea_per_user)
    now = dt.datetime.utcnow()
    idea = Idea(
        title=payload.title,
        body=payload.body,
        tags=",".join(tag.strip() for tag in payload.tags if tag.strip()),
        author_id=current_user.id,
        merged_into_id=payload.merged_into_id,
        status=IdeaStatus.submitted.value,
        status_updated_at=now,
        status_updated_by=current_user.id,
        created_at=now,
        updated_at=now,
        signature="",
    idea.signature = sign_idea(idea, current_user)
    session.add(idea)
    session.refresh(idea)
        event_type="idea_create",
        user_id=current_user.id,
        target_type="idea",
        target_id=idea.id,
        details={"status": idea.status},
    author = session.get(User, idea.author_id)
    return to_idea_response(idea, author, session)
@app.get("/api/ideas", response_model=List[IdeaResponse])
def list_ideas(
    limit: Optional[int] = Query(default=None, ge=1),
    offset: int = Query(default=0, ge=0),
    page_size = resolve_limit(limit)
    ideas = session.exec(
        select(Idea).order_by(Idea.created_at.desc()).offset(offset).limit(page_size)
    ).all()
    users = {u.id: u for u in session.exec(select(User)).all()}
    return [to_idea_response(idea, users[idea.author_id], session) for idea in ideas]
@app.get("/api/ideas/{idea_id}", response_model=IdeaResponse)
def get_idea(idea_id: int, session: Session = Depends(get_session)):
    idea = session.get(Idea, idea_id)
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
@app.put("/api/ideas/{idea_id}", response_model=IdeaResponse)
def update_idea(
    idea_id: int,
    payload: IdeaUpdate,
    if idea.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the author can edit")
    if payload.title is not None:
        idea.title = payload.title
    if payload.body is not None:
        idea.body = payload.body
    if payload.tags is not None:
        idea.tags = ",".join(tag.strip() for tag in payload.tags if tag.strip())
    idea.merged_into_id = payload.merged_into_id
    idea.updated_at = dt.datetime.utcnow()
        event_type="idea_update",
@app.patch("/api/ideas/{idea_id}/status", response_model=IdeaResponse)
def update_idea_status(
    payload: IdeaStatusUpdate,
    can_update = user_is_admin(current_user) or idea.author_id == current_user.id
    if not can_update:
        raise HTTPException(status_code=403, detail="Only author or admin can update status")
    old_status = idea.status
    validate_status_transition(old_status, payload.status.value, user_is_admin(current_user))
    idea.status = payload.status.value
    idea.status_updated_at = dt.datetime.utcnow()
    idea.status_updated_by = current_user.id
        event_type="status_change",
        details={"old_status": old_status, "new_status": payload.status.value},
@app.post("/api/ideas/{idea_id}/merge", response_model=IdeaResponse)
def merge_idea(
    payload: MergeRequest,
    target = session.get(Idea, payload.target_id)
    if not idea or not target:
    idea.merged_into_id = target.id
    merge_record = MergeRecord(source_id=idea.id, target_id=target.id, author_id=current_user.id)
    session.add_all([idea, merge_record])
        event_type="idea_merge",
        details={"target_id": target.id},
@app.post("/api/ideas/{idea_id}/vote")
def vote(
    payload: VoteRequest,
    enforce_rate_limit("vote_ip", client_ip, limits.vote_per_ip)
    enforce_rate_limit("vote_user", str(current_user.id), limits.vote_per_user)
    existing = session.exec(
        select(Vote).where(Vote.idea_id == idea_id, Vote.user_id == current_user.id)
    ).first()
        existing.value = payload.value
        vote_obj = existing
    else:
        vote_obj = Vote(idea_id=idea_id, user_id=current_user.id, value=payload.value)
    session.add(vote_obj)
        event_type="idea_vote",
        target_id=idea_id,
        details={"value": payload.value},
        select(func.coalesce(func.sum(Vote.value), 0)).where(Vote.idea_id == idea_id)
    return {"score": score}
@app.post("/api/ideas/{idea_id}/comments", response_model=CommentResponse)
def add_comment(
    payload: CommentCreate,
    enforce_rate_limit("comment_ip", client_ip, limits.comment_per_ip)
    enforce_rate_limit("comment_user", str(current_user.id), limits.comment_per_user)
    comment = Comment(
        idea_id=idea_id,
    comment.signature = sign_comment(comment, current_user)
    session.add(comment)
    session.refresh(comment)
        event_type="idea_comment",
        details={"comment_id": comment.id},
    return to_comment_response(comment, current_user)
@app.get("/api/ideas/{idea_id}/comments", response_model=List[CommentResponse])
def list_comments(
    comments = session.exec(
        select(Comment)
        .where(Comment.idea_id == idea_id)
        .order_by(Comment.created_at)
        .offset(offset)
        .limit(page_size)
    return [to_comment_response(c, users[c.author_id]) for c in comments]
@app.get("/api/reports/summary", response_model=ReportSummaryResponse)
def report_summary(session: Session = Depends(get_session)) -> ReportSummaryResponse:
    ideas = session.exec(select(Idea)).all()
    counts = {status: 0 for status in STATUS_FLOW}
    scored_ideas = []
    response_durations = []
    for idea in ideas:
        counts.setdefault(idea.status, 0)
        counts[idea.status] += 1
        score = session.exec(
            select(func.coalesce(func.sum(Vote.value), 0)).where(Vote.idea_id == idea.id)
        ).one()
        scored_ideas.append((score, idea.created_at, idea))
        if idea.status != IdeaStatus.submitted.value and idea.status_updated_at:
            hours = (idea.status_updated_at - idea.created_at).total_seconds() / 3600
            if hours >= 0:
                response_durations.append(hours)
    scored_ideas.sort(key=lambda row: (row[0], row[1]), reverse=True)
    top = [
        TopIdeaSummary(
            id=idea.id,
            title=idea.title,
            status=IdeaStatus(idea.status),
            score=score,
        for score, _, idea in scored_ideas[:5]
    ]
    median_response = None
    if response_durations:
        median_response = round(float(statistics.median(response_durations)), 2)
    return ReportSummaryResponse(
        generated_at=dt.datetime.utcnow(),
        total_ideas=len(ideas),
        counts_by_status=counts,
        top_ideas=top,
        median_response_hours=median_response,
@app.get("/api/reports/export.csv")
def export_report_csv(
    _: User = Depends(get_admin_user),
) -> Response:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(
            "row_type",
            "idea_id",
            "title",
            "status",
            "score",
            "comment_count",
            "author_id",
            "status_updated_by",
            "created_at",
            "updated_at",
            "status_updated_at",
        ]
    ideas = session.exec(select(Idea).order_by(Idea.id)).all()
        comment_count = session.exec(
            select(func.count()).select_from(Comment).where(Comment.idea_id == idea.id)
        writer.writerow(
            [
                "idea",
                idea.id,
                idea.title,
                idea.status,
                score,
                comment_count,
                idea.author_id,
                idea.status_updated_by,
                idea.created_at.isoformat(),
                idea.updated_at.isoformat(),
                idea.status_updated_at.isoformat() if idea.status_updated_at else "",
            ]
    writer.writerow([])
            "audit_id",
            "old_status",
            "new_status",
            "changed_by",
            "ip_address",
    events = session.exec(
        select(AuditEvent)
        .where(AuditEvent.event_type == "status_change")
        .order_by(AuditEvent.created_at)
    for event in events:
        details = parse_audit_details(event.details_json)
                "status_event",
                event.id,
                event.target_id,
                details.get("old_status", ""),
                details.get("new_status", ""),
                event.user_id,
                event.ip_address or "",
                event.created_at.isoformat(),
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=platform-export.csv"},
@app.get("/api/audit-events", response_model=List[AuditEventResponse])
def list_audit_events(
) -> List[AuditEventResponse]:
        .order_by(AuditEvent.created_at.desc())
    return [to_audit_event_response(event) for event in events]
@app.get("/segment_000.md")
def serve_spec_file():
        raise HTTPException(status_code=404, detail="Spec document missing")
    return FileResponse(spec_path)
