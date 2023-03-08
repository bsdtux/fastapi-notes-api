from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from api.database import get_db
from api.models import Note
from api.schemas import NoteBaseSchema

class NotesController:
    def __init__(self, db_session: Session, user_id: int):
        self.db_session = db_session or get_db()
        self.user_id = user_id
    
    def list(self, limit: int = 10, page: int = 1, search: str = ""):
        skip = (page - 1) * limit
        
        notes = self.db_session.query(Note)

        if search:
            notes.filter(Note.title.contains(search))

        notes = notes.limit(limit).offset(skip).all() 
        return notes
    
    def create(self, payload: NoteBaseSchema):
        new_note = Note(**payload.dict())
        self.db_session.add(new_note)
        self.db_session.commit()
        self.db_session.refresh(new_note)
        return new_note

    def update(self, note_id: int, payload: NoteBaseSchema):
        note_query = self.db_session.query(Note).filter(Note.id==note_id)
        note_item = note_query.first()
        if not note_item:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        
        updated_note = payload.dict(exclude_unset=True)
        if not updated_note:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="No udpateable field sent")
        note_query.update(updated_note)
        self.db_session.commit()
        self.db_session.refresh(note_item)
        return note_item
    
    def read(self, note_id: int):
        note_query = self.db_session.query(Note).filter(Note.id==note_id)
        note_item = note_query.first()
        if not note_item:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note note found")
        return note_item
    
    def delete(self, note_id: int):
        note_query = self.db_session.query(Note).filter(Note.id==note_id)
        note_item = note_query.first()

        if note_item:
            self.db_session.delete(note_item)
            self.db_session.commit()
