from fastapi import APIRouter, HTTPException, status

from schemas import Note, NoteCreate
from storage import NoteStorage


router = APIRouter(prefix="/notes", tags=["Работа с записями"])
storage = NoteStorage()


@router.post("/", response_model=Note, status_code=status.HTTP_201_CREATED)
async def save_note(note: NoteCreate):
    return storage.create_note(note)


@router.get("/", response_model=list[Note], status_code=status.HTTP_200_OK)
async def show_notes():
    return storage.get_all_notes()


@router.get("/{note_id}", response_model=Note, status_code=status.HTTP_200_OK)
async def give_note(note_id: str):
    note = storage.get_note(note_id)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Записи с айди: {note_id} Не найдено",
        )
    return note
