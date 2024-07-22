from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from keycloak import KeycloakOpenID
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from .database import SessionLocal, engine
from . import models, schemas, crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

keycloak_openid = KeycloakOpenID(
    server_url="http://keycloak:8080/auth/",
    client_id="user-cli",
    realm_name="library",
    client_secret_key="zxiVm1tei3vGpmDgS0mqWEkTEIOWddct"
)

trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({"service.name": "loan-service"})
    )
)
jaeger_exporter = JaegerExporter(
    agent_host_name='jaeger',
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

FastAPIInstrumentor.instrument_app(app)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/loans/", response_model=schemas.Loan)
def create_loan(loan: schemas.LoanCreate, db: Session = Depends(get_db)):
    return crud.create_loan(db=db, loan=loan)

@app.get("/loans/", response_model=List[schemas.Loan])
def read_loans(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    loans = crud.get_loans(db, skip=skip, limit=limit)
    return loans

@app.get("/secure-data/")
def secure_data(token: str):
    try:
        userinfo = keycloak_openid.userinfo(token)
        return userinfo
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
