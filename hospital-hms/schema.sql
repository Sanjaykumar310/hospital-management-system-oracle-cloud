-- Minimal Oracle schema for Hospital HMS (Autonomous DB compatible)
-- Run as a privileged user or as schema owner

CREATE TABLE patients (
  id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name VARCHAR2(200) NOT NULL,
  dob DATE,
  phone VARCHAR2(32)
);

CREATE TABLE doctors (
  id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name VARCHAR2(200) NOT NULL,
  specialization VARCHAR2(128),
  phone VARCHAR2(32)
);

CREATE TABLE appointments (
  id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  patient_id NUMBER NOT NULL,
  doctor_id NUMBER NOT NULL,
  scheduled_at TIMESTAMP NOT NULL,
  reason VARCHAR2(1024),
  status VARCHAR2(32) DEFAULT 'SCHEDULED',
  CONSTRAINT fk_appt_patient FOREIGN KEY (patient_id) REFERENCES patients(id),
  CONSTRAINT fk_appt_doctor FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);

CREATE TABLE admin_users (
  id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  username VARCHAR2(64) UNIQUE NOT NULL,
  password_hash VARCHAR2(256) NOT NULL,
  role VARCHAR2(32) DEFAULT 'admin'
);

-- Small helper index
CREATE INDEX idx_appt_sched ON appointments(scheduled_at);
