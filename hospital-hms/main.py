"""
Minimal FastAPI app for Hospital HMS — patient and appointment basics.
Run: `uvicorn main:app --reload --port 8000`
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

from db import get_connection, rows_to_dicts

app = FastAPI(title="Hospital HMS (minimal)")


class PatientIn(BaseModel):
    name: str
    dob: Optional[date] = None
    phone: Optional[str] = None


class PatientOut(PatientIn):
    id: int


class AppointmentIn(BaseModel):
    patient_id: int
    doctor_id: int
    scheduled_at: datetime
    reason: Optional[str] = None


@app.get("/", summary="Health")
def health():
    return {"status": "ok", "app": "hospital-hms"}


@app.get("/patients", response_model=list[PatientOut])
def list_patients():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, dob, phone FROM patients ORDER BY id DESC FETCH FIRST 100 ROWS ONLY")
    rows = rows_to_dicts(cur)
    conn.close()
    return rows


@app.get("/patients/{patient_id}", response_model=PatientOut)
def get_patient(patient_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, dob, phone FROM patients WHERE id = :id", id=patient_id)
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Patient not found")
    cols = [c[0].lower() for c in cur.description]
    return dict(zip(cols, row))


@app.post("/patients", response_model=PatientOut, status_code=201)
def create_patient(p: PatientIn):
    conn = get_connection()
    cur = conn.cursor()
    # Use Oracle RETURNING INTO to get generated ID
    new_id = cur.var(int)
    cur.execute(
        "INSERT INTO patients (name, dob, phone) VALUES (:n, :d, :p) RETURNING id INTO :id",
        n=p.name,
        d=p.dob,
        p=p.phone,
        id=new_id,
    )
    conn.commit()
    pid = new_id.getvalue()[0]
    conn.close()
    return {"id": pid, "name": p.name, "dob": p.dob, "phone": p.phone}


@app.post("/appointments", status_code=201)
def create_appointment(a: AppointmentIn):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO appointments (patient_id, doctor_id, scheduled_at, reason) VALUES (:p,:d,:s,:r)",
        p=a.patient_id,
        d=a.doctor_id,
        s=a.scheduled_at,
        r=a.reason,
    )
    conn.commit()
    conn.close()
    return {"ok": True, "patient_id": a.patient_id, "scheduled_at": a.scheduled_at}
