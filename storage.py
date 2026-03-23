import json
from pathlib import Path
from threading import Lock
from uuid import uuid4

from schemas import Note, NoteCreate


class NoteStorage:
    def __init__(self, file_path: str = "free-db.json") -> None:
        self.file_path = Path(file_path)
        self._lock = Lock()
        self._notes: dict[str, Note] = {}
        self._load()

    def _load(self) -> None:
        if not self.file_path.exists():
            return

        raw = self.file_path.read_text(encoding="utf-8").strip()
        if not raw:
            return

        data = json.loads(raw)
        self._notes = {
            item["note_id"]: Note(**item)
            for item in data
        }

    def _save(self) -> None:
        temp_path = self.file_path.with_suffix(".tmp")
        payload = [note.model_dump() for note in self._notes.values()]
        temp_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        temp_path.replace(self.file_path)

    def create_note(self, payload: NoteCreate) -> Note:
        with self._lock:
            note = Note(note_id=uuid4().hex, data=payload.data)
            self._notes[note.note_id] = note
            self._save()
            return note

    def get_all_notes(self) -> list[Note]:
        with self._lock:
            return list(self._notes.values())

    def get_note(self, note_id: str) -> Note | None:
        with self._lock:
            return self._notes.get(note_id)
