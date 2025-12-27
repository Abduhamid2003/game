from fastapi import FastAPI
from database import Base, engine
from routers import auth_router, igry_router, urovni_router, dostizheniya_router, igroki_router

app = FastAPI(title="Gaming Platform API")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router.router)
app.include_router(igry_router.router)
app.include_router(urovni_router.router)
app.include_router(dostizheniya_router.router)
app.include_router(igroki_router.router)

@app.get("/")
def root():
    return {"message": "Dobro pozhalovat na API igrovoj platformy!"}