from fastapi import FastAPI, Depends, HTTPException, Body, Query
from sqlalchemy.orm import Session
from typing import List
from .database import SessionLocal, engine
from . import models, schemas, utils

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.phone_number == user.phone_number).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/create_conversation", response_model=schemas.Conversation)
def create_conversation(conversation: schemas.ConversationCreate, db: Session = Depends(get_db)):
    db_conversation = utils.create_conversation(db, [user.id for user in conversation.users], conversation.name)
    return db_conversation

@app.post("/send_message", response_model=schemas.Message)
def send_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    db_message = utils.send_message(db, message.sender_id, message.conversation_id, message.content)
    return db_message

@app.get("/conversations", response_model=List[schemas.Conversation])
def get_conversations(db: Session = Depends(get_db)):
    return db.query(models.Conversation).all()

@app.get("/messages/{conversation_id}", response_model=List[schemas.Message])
def get_messages(conversation_id: int, db: Session = Depends(get_db)):
    return db.query(models.Message).filter(models.Message.conversation_id == conversation_id).all()
