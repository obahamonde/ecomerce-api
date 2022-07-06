from uuid import uuid4

def tstamp(ts: int) -> float:
    return float(str(ts)[:10]+'.'+str(ts)[10:])

def id() -> str:
    return str(uuid4().hex)

def avatar()->str:
    return f"https://avatars.dicebear.com/api/avataaars/{id()}.svg"