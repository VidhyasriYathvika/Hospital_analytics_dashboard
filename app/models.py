from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, Numeric, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    insurance_type = Column(String)


class Admission(Base):
    __tablename__ = "admissions"

    admission_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"))
    department = Column(String)
    admission_date = Column(TIMESTAMP)
    discharge_date = Column(TIMESTAMP)
    emergency = Column(Boolean)
    outcome = Column(String)


class Doctor(Base):
    __tablename__ = "doctors"

    doctor_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    department = Column(String)
    available_hours = Column(Integer)


class Billing(Base):
    __tablename__ = "billing"

    bill_id = Column(Integer, primary_key=True, index=True)
    admission_id = Column(Integer, ForeignKey("admissions.admission_id"))
    cost = Column(Numeric)
