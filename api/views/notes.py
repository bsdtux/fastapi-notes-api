from api.schemas import NoteBaseSchema, ListNoteResponse, NoteResponse, NoteUpdateSchema
from sqlalchemy.orm import Session
from typing import List
from fastapi import Depends, HTTPException, status, APIRouter
from api.database import get_db
from api.controllers.notes import NotesController
from api.models import Note

note_router = APIRouter()


@note_router.get("/notes/")
def get_notes(session: Session = Depends(get_db), limit: int = 10, page: int = 1, search : str = ''):
    notes = NotesController(session, 1).list(limit=limit, page=page, search=search) 
    return _make_return_response("success", notes, True).dict()


@note_router.post("/notes/", status_code=status.HTTP_201_CREATED)
def add_note(payload: NoteBaseSchema, session: Session = Depends(get_db)):
    note = NotesController(session, 1).create(payload)
    return _make_return_response("success", note).dict()

@note_router.put("/notes/{note_id}")
def update_note(note_id: int, payload: NoteUpdateSchema, session: Session = Depends(get_db)):
    note = NotesController(session, 1).update(note_id, payload)
    return _make_return_response("success", note).dict()

@note_router.get("/notes/{note_id}")
def read_note(note_id: int, session: Session = Depends(get_db)):
    note = NotesController(session, 1).read(note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    
    return _make_return_response("success", note).dict()

@note_router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, session: Session = Depends(get_db)):
    NotesController(session, 1).delete(note_id)


def _make_return_response(status: str, notes: List[Note] | Note, list_route: bool = False):
    if list_route:
        return ListNoteResponse(status=status, results=len(notes), notes=notes)
    return NoteResponse(status=status, note=notes)