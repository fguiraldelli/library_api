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

# Cria todas as tabelas do banco de dados se não existirem
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuração do Keycloak
keycloak_openid = KeycloakOpenID(
    server_url="http://keycloak:8080/auth/",
    client_id="user-cli",
    realm_name="library",
    client_secret_key="zxiVm1tei3vGpmDgS0mqWEkTEIOWddct"
)

# Configuração do OpenTelemetry para rastreabilidade
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({"service.name": "book-service"})
    )
)
jaeger_exporter = JaegerExporter(
    agent_host_name='jaeger',
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

# Instrumentação do FastAPI com OpenTelemetry
FastAPIInstrumentor.instrument_app(app)

# Dependência de banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints do serviço de livros
@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)

@app.get("/books/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books

@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.delete("/books/{book_id}", response_model=schemas.Book)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.delete_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    db_book = crud.update_book(db, book_id=book_id, book=book)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.get("/secure-data/")
def secure_data(token: str):
    try:
        userinfo = keycloak_openid.userinfo(token)
        return userinfo
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

