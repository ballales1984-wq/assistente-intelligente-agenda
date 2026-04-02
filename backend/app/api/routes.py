"""
API Routes - Assistente Intelligente v2
"""
import json
import secrets
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from typing import List

from app.core.database import get_db
from app.models.schemas import (
    UserProfile, Obiettivo, Impegno, DiarioEntry, Spesa,
    Habit, HabitCompletion, CommunityPost
)
from app.models.pydantic_models import (
    UserResponse, ObiettivoCreate, ObiettivoResponse,
    ImpegnoCreate, ImpegnoResponse, DiarioCreate, DiarioResponse,
    SpesaCreate, SpesaResponse, HabitCreate, HabitResponse,
    ChatRequest, ChatResponse, CommunityPostCreate, CommunityPostResponse,
    FingerprintRequest, AuthResponse, StatsResponse
)
from app.services.auth import get_or_create_user
from app.ai.ollama_service import chat_with_ollama

router = APIRouter()


# ─── AUTH ───
@router.post("/auth/login", response_model=AuthResponse)
def login(req: FingerprintRequest, db: Session = Depends(get_db)):
    user, is_new = get_or_create_user(db, req.fingerprint)
    return AuthResponse(success=True, user=UserResponse.model_validate(user), is_new=is_new)


# ─── OBIETTIVI ───
@router.get("/obiettivi", response_model=List[ObiettivoResponse])
def get_obiettivi(user_id: int = 1, db: Session = Depends(get_db)):
    return db.query(Obiettivo).filter(Obiettivo.user_id == user_id).all()

@router.post("/obiettivi", response_model=ObiettivoResponse)
def create_obiettivo(data: ObiettivoCreate, user_id: int = 1, db: Session = Depends(get_db)):
    obj = Obiettivo(user_id=user_id, **data.model_dump())
    if not obj.data_inizio:
        obj.data_inizio = date.today()
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.put("/obiettivi/{id}", response_model=ObiettivoResponse)
def update_obiettivo(id: int, data: dict, db: Session = Depends(get_db)):
    obj = db.query(Obiettivo).filter(Obiettivo.id == id).first()
    if not obj:
        raise HTTPException(404, "Obiettivo non trovato")
    for k, v in data.items():
        if hasattr(obj, k):
            setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/obiettivi/{id}")
def delete_obiettivo(id: int, db: Session = Depends(get_db)):
    obj = db.query(Obiettivo).filter(Obiettivo.id == id).first()
    if not obj:
        raise HTTPException(404, "Obiettivo non trovato")
    db.delete(obj)
    db.commit()
    return {"success": True}


# ─── IMPEGNI ───
@router.get("/impegni", response_model=List[ImpegnoResponse])
def get_impegni(user_id: int = 1, db: Session = Depends(get_db)):
    return db.query(Impegno).filter(Impegno.user_id == user_id).all()

@router.post("/impegni", response_model=ImpegnoResponse)
def create_impegno(data: ImpegnoCreate, user_id: int = 1, db: Session = Depends(get_db)):
    imp = Impegno(user_id=user_id, **data.model_dump())
    db.add(imp)
    db.commit()
    db.refresh(imp)
    return imp

@router.put("/impegni/{id}", response_model=ImpegnoResponse)
def update_impegno(id: int, data: dict, db: Session = Depends(get_db)):
    imp = db.query(Impegno).filter(Impegno.id == id).first()
    if not imp:
        raise HTTPException(404, "Impegno non trovato")
    for k, v in data.items():
        if hasattr(imp, k):
            setattr(imp, k, v)
    db.commit()
    db.refresh(imp)
    return imp

@router.delete("/impegni/{id}")
def delete_impegno(id: int, db: Session = Depends(get_db)):
    imp = db.query(Impegno).filter(Impegno.id == id).first()
    if not imp:
        raise HTTPException(404, "Impegno non trovato")
    db.delete(imp)
    db.commit()
    return {"success": True}

@router.get("/impegni/oggi", response_model=List[ImpegnoResponse])
def impegni_oggi(user_id: int = 1, db: Session = Depends(get_db)):
    return db.query(Impegno).filter(Impegno.user_id == user_id, Impegno.data == date.today()).all()


# ─── DIARIO ───
@router.get("/diario", response_model=List[DiarioResponse])
def get_diario(user_id: int = 1, db: Session = Depends(get_db)):
    entries = db.query(DiarioEntry).filter(DiarioEntry.user_id == user_id).order_by(DiarioEntry.data.desc()).all()
    # Parse tags JSON
    for e in entries:
        if isinstance(e.tags, str):
            try:
                e.tags = json.loads(e.tags)
            except:
                e.tags = []
    return entries

@router.post("/diario", response_model=DiarioResponse)
def create_diario(data: DiarioCreate, user_id: int = 1, db: Session = Depends(get_db)):
    d = data.model_dump()
    if not d.get("data"):
        d["data"] = date.today()

    # Serialize tags list to JSON
    tags = d.pop("tags", None)
    tags_json = json.dumps(tags, ensure_ascii=False) if tags else None

    # Simple sentiment
    testo = d["contenuto"].lower()
    positivi = ["felice", "bene", "grande", "motivato", "contento", "successo", "bello", "fantastico"]
    negativi = ["triste", "male", "stanco", "stress", "problema", "difficile", "brutto", "ansia"]
    sp = sum(1 for w in positivi if w in testo)
    sn = sum(1 for w in negativi if w in testo)
    d["sentiment"] = "positivo" if sp > sn else ("negativo" if sn > sp else "neutro")

    entry = DiarioEntry(user_id=user_id, tags=tags_json, **d)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    # Parse back for response
    if isinstance(entry.tags, str):
        try:
            entry.tags = json.loads(entry.tags)
        except:
            entry.tags = []
    return entry

@router.delete("/diario/{id}")
def delete_diario(id: int, db: Session = Depends(get_db)):
    entry = db.query(DiarioEntry).filter(DiarioEntry.id == id).first()
    if not entry:
        raise HTTPException(404, "Entry non trovata")
    db.delete(entry)
    db.commit()
    return {"success": True}

@router.post("/diario/{id}/share")
def share_diario(id: int, db: Session = Depends(get_db)):
    entry = db.query(DiarioEntry).filter(DiarioEntry.id == id).first()
    if not entry:
        raise HTTPException(404, "Entry non trovata")
    if not entry.share_token:
        entry.share_token = secrets.token_urlsafe(32)
    entry.is_public = True
    db.commit()
    return {"share_token": entry.share_token}


# ─── SPESE ───
@router.get("/spese", response_model=List[SpesaResponse])
def get_spese(user_id: int = 1, db: Session = Depends(get_db)):
    return db.query(Spesa).filter(Spesa.user_id == user_id).order_by(Spesa.data.desc()).all()

@router.post("/spese", response_model=SpesaResponse)
def create_spesa(data: SpesaCreate, user_id: int = 1, db: Session = Depends(get_db)):
    spesa = Spesa(user_id=user_id, **data.model_dump())
    db.add(spesa)
    db.commit()
    db.refresh(spesa)
    return spesa

@router.delete("/spese/{id}")
def delete_spesa(id: int, db: Session = Depends(get_db)):
    spesa = db.query(Spesa).filter(Spesa.id == id).first()
    if not spesa:
        raise HTTPException(404, "Spesa non trovata")
    db.delete(spesa)
    db.commit()
    return {"success": True}

@router.get("/spese/oggi", response_model=List[SpesaResponse])
def spese_oggi(user_id: int = 1, db: Session = Depends(get_db)):
    return db.query(Spesa).filter(Spesa.user_id == user_id, Spesa.data == date.today()).all()

@router.get("/spese/settimana")
def spese_settimana(user_id: int = 1, db: Session = Depends(get_db)):
    start = date.today() - timedelta(days=7)
    spese = db.query(Spesa).filter(Spesa.user_id == user_id, Spesa.data >= start).all()
    return {"totale": sum(s.importo for s in spese), "count": len(spese)}

@router.get("/spese/mese")
def spese_mese(user_id: int = 1, db: Session = Depends(get_db)):
    start = date.today() - timedelta(days=30)
    spese = db.query(Spesa).filter(Spesa.user_id == user_id, Spesa.data >= start).all()
    per_cat = {}
    for s in spese:
        per_cat[s.categoria] = per_cat.get(s.categoria, 0) + s.importo
    return {"totale": sum(s.importo for s in spese), "count": len(spese), "per_categoria": per_cat}


# ─── HABITS ───
@router.get("/habits", response_model=List[HabitResponse])
def get_habits(user_id: int = 1, db: Session = Depends(get_db)):
    return db.query(Habit).filter(Habit.user_id == user_id, Habit.attiva == True).all()

@router.post("/habits", response_model=HabitResponse)
def create_habit(data: HabitCreate, user_id: int = 1, db: Session = Depends(get_db)):
    h = Habit(user_id=user_id, **data.model_dump())
    db.add(h)
    db.commit()
    db.refresh(h)
    return h

@router.post("/habits/{id}/complete")
def complete_habit(id: int, db: Session = Depends(get_db)):
    comp = HabitCompletion(habit_id=id, data=date.today(), completato=True)
    db.add(comp)
    db.commit()
    return {"success": True}


# ─── STATISTICHE ───
@router.get("/statistiche", response_model=StatsResponse)
def get_statistiche(user_id: int = 1, db: Session = Depends(get_db)):
    today = date.today()
    start_month = today - timedelta(days=30)
    return StatsResponse(
        obiettivi_attivi=db.query(Obiettivo).filter(Obiettivo.user_id == user_id, Obiettivo.completato == False).count(),
        impegni_oggi=db.query(Impegno).filter(Impegno.user_id == user_id, Impegno.data == today).count(),
        diario_entries=db.query(DiarioEntry).filter(DiarioEntry.user_id == user_id).count(),
        spese_mese=sum(s.importo for s in db.query(Spesa).filter(Spesa.user_id == user_id, Spesa.data >= start_month).all()),
        habits_attivi=db.query(Habit).filter(Habit.user_id == user_id, Habit.attiva == True).count()
    )


# ─── COMMUNITY ───
@router.get("/community/posts", response_model=List[CommunityPostResponse])
def get_community_posts(db: Session = Depends(get_db)):
    return db.query(CommunityPost).order_by(CommunityPost.created_at.desc()).limit(50).all()

@router.post("/community/posts", response_model=CommunityPostResponse)
def create_community_post(data: CommunityPostCreate, user_id: int = 1, db: Session = Depends(get_db)):
    post = CommunityPost(user_id=user_id, **data.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.post("/community/posts/{id}/like")
def like_post(id: int, db: Session = Depends(get_db)):
    post = db.query(CommunityPost).filter(CommunityPost.id == id).first()
    if not post:
        raise HTTPException(404, "Post non trovato")
    post.likes += 1
    db.commit()
    return {"likes": post.likes}


# ─── CHAT AI ───
@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, user_id: int = 1, db: Session = Depends(get_db)):
    obiettivi = db.query(Obiettivo).filter(Obiettivo.user_id == user_id, Obiettivo.completato == False).all()
    impegni = db.query(Impegno).filter(Impegno.user_id == user_id, Impegno.data >= date.today()).limit(5).all()
    ctx = {
        "obiettivi": [{"nome": o.titolo} for o in obiettivi],
        "impegni": [{"nome": i.titolo} for i in impegni]
    }
    result = await chat_with_ollama(req.message, ctx)
    return ChatResponse(**result)


# ─── EXPORT ───
@router.get("/export/tutto")
def export_all(user_id: int = 1, db: Session = Depends(get_db)):
    return {
        "obiettivi": [{"id": o.id, "titolo": o.titolo} for o in db.query(Obiettivo).filter(Obiettivo.user_id == user_id).all()],
        "impegni": [{"id": i.id, "titolo": i.titolo} for i in db.query(Impegno).filter(Impegno.user_id == user_id).all()],
        "diario": [{"id": d.id, "contenuto": d.contenuto} for d in db.query(DiarioEntry).filter(DiarioEntry.user_id == user_id).all()],
        "spese": [{"id": s.id, "importo": s.importo} for s in db.query(Spesa).filter(Spesa.user_id == user_id).all()]
    }
