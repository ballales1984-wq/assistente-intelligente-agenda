from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime


# ===== USER =====
class UserResponse(BaseModel):
    id: int
    nome: str
    fingerprint: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ===== OBIETTIVO (allineato con Angular) =====
class ObiettivoCreate(BaseModel):
    titolo: str
    descrizione: Optional[str] = None
    categoria: str = "personale"
    frequenza: str = "settimanale"
    ore_necessarie: float = 0
    ore_completate: float = 0
    progresso: float = 0
    data_inizio: Optional[date] = None
    data_scadenza: Optional[date] = None
    completato: bool = False

class ObiettivoResponse(ObiettivoCreate):
    id: int
    user_id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ===== IMPEGNO (allineato con Angular) =====
class ImpegnoCreate(BaseModel):
    titolo: str
    descrizione: Optional[str] = None
    data: date
    ora_inizio: str = "09:00"
    ora_fine: str = "10:00"
    categoria: str = "altro"
    completato: bool = False
    promemoria: bool = False

class ImpegnoResponse(ImpegnoCreate):
    id: int
    user_id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ===== DIARIO (allineato con Angular) =====
class DiarioCreate(BaseModel):
    contenuto: str
    data: Optional[date] = None
    umore: Optional[str] = None
    tags: Optional[List[str]] = None

class DiarioResponse(BaseModel):
    id: int
    user_id: int
    data: Optional[date] = None
    contenuto: str
    umore: Optional[str] = None
    tags: Optional[List[str]] = None
    sentiment: Optional[str] = None
    share_token: Optional[str] = None
    is_public: bool = False
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ===== SPESA (allineato con Angular) =====
class SpesaCreate(BaseModel):
    importo: float
    descrizione: str
    categoria: str
    data: date
    necessaria: bool = True

class SpesaResponse(SpesaCreate):
    id: int
    user_id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ===== HABIT =====
class HabitCreate(BaseModel):
    nome: str
    descrizione: Optional[str] = None
    icona: str = "✅"
    colore: str = "#667eea"
    frequenza: str = "daily"
    obiettivo_numero: int = 1
    unita_misura: str = "volte"

class HabitResponse(HabitCreate):
    id: int
    user_id: int
    attiva: bool = True
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ===== CHAT =====
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    suggestions: Optional[List[str]] = None


# ===== COMMUNITY =====
class CommunityPostCreate(BaseModel):
    tipo: str
    contenuto: str
    tags: Optional[str] = None

class CommunityPostResponse(CommunityPostCreate):
    id: int
    user_id: int
    likes: int = 0
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ===== AUTH =====
class FingerprintRequest(BaseModel):
    fingerprint: str
    timezone: Optional[str] = None
    language: Optional[str] = None

class AuthResponse(BaseModel):
    success: bool
    user: Optional[UserResponse] = None
    is_new: bool = False


# ===== STATS =====
class StatsResponse(BaseModel):
    obiettivi_attivi: int
    impegni_oggi: int
    diario_entries: int
    spese_mese: float
    habits_attivi: int
