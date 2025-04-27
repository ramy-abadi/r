import random
import hashlib
import secrets
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from .models import User, Conversation, Message

def generate_session_token() -> str:
    return secrets.token_hex(32)

def verify_otp(db: Session, phone_number: str, otp_code: str) -> Optional[User]:
    user = db.query(User).filter(User.phone_number == phone_number).first()
    if user:
        # Assuming OTP verification logic here
        return user
    return None

def create_conversation(db: Session, user_ids: list, name: str) -> Conversation:
    users = db.query(User).filter(User.id.in_(user_ids)).all()
    conversation = Conversation(name=name, users=users)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

def send_message(db: Session, sender_id: int, conversation_id: int, content: str) -> Message:
    message = Message(sender_id=sender_id, conversation_id=conversation_id, content=content)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message
