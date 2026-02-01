from fastapi import APIRouter
from sqlalchemy import text
from app.database import engine

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/alos")
def get_alos():
    with engine.connect() as connection:
        query = text("""
        SELECT 
            ROUND(
                AVG(EXTRACT(EPOCH FROM (discharge_date - admission_date)) / 86400),
                2
            ) AS alos_days
        FROM admissions
        WHERE discharge_date IS NOT NULL
        """)
        result = connection.execute(query).fetchone()

    return {"Average Length of Stay (days)": float(result[0])}


@router.get("/admissions-by-department")
def admissions_by_department():
    with engine.connect() as connection:
        query = text("""
        SELECT department, COUNT(*) AS total_admissions
        FROM admissions
        GROUP BY department
        """)
        result = connection.execute(query).fetchall()

    return [{"department": r[0], "total_admissions": r[1]} for r in result]

@router.get("/emergency-vs-scheduled")
def emergency_vs_scheduled():
    with engine.connect() as connection:
        query = text("""
        SELECT
            CASE WHEN emergency = true THEN 'Emergency' ELSE 'Scheduled' END AS case_type,
            COUNT(*) AS total_cases
        FROM admissions
        GROUP BY emergency
        """)
        result = connection.execute(query).fetchall()

    return [{"case_type": r[0], "total_cases": r[1]} for r in result]

@router.get("/patient-outcomes")
def patient_outcomes():
    with engine.connect() as connection:
        query = text("""
        SELECT outcome, COUNT(*) AS total
        FROM admissions
        GROUP BY outcome
        """)
        result = connection.execute(query).fetchall()

    return [{"outcome": r[0], "total": r[1]} for r in result]
@router.get("/cost-by-department")
def cost_by_department():
    with engine.connect() as connection:
        query = text("""
        SELECT a.department, SUM(b.cost) AS total_cost
        FROM admissions a
        JOIN billing b ON a.admission_id = b.admission_id
        GROUP BY a.department
        """)
        result = connection.execute(query).fetchall()

    return [{"department": r[0], "total_cost": float(r[1])} for r in result]
@router.get("/admission-trends")
def admission_trends():
    with engine.connect() as connection:
        query = text("""
        SELECT 
            DATE(admission_date) AS admission_day,
            COUNT(*) AS total_admissions
        FROM admissions
        GROUP BY admission_day
        ORDER BY admission_day
        """)
        result = connection.execute(query).fetchall()

    return [{"date": str(r[0]), "total_admissions": r[1]} for r in result]

@router.get("/financial-kpis")
def financial_kpis():
    with engine.connect() as connection:
        query = text("""
        SELECT
            SUM(b.cost) AS total_revenue,
            ROUND(AVG(b.cost), 2) AS avg_cost_per_admission,
            MAX(b.cost) AS max_cost,
            MIN(b.cost) AS min_cost
        FROM billing b
        """)
        r = connection.execute(query).fetchone()

    return [
        {"KPI": "Total Revenue", "Value": float(r[0])},
        {"KPI": "Average Cost per Admission", "Value": float(r[1])},
        {"KPI": "Highest Admission Cost", "Value": float(r[2])},
        {"KPI": "Lowest Admission Cost", "Value": float(r[3])}
    ]
@router.get("/revenue-by-department")
def revenue_by_department():
    with engine.connect() as connection:
        query = text("""
        SELECT
            a.department,
            SUM(b.cost) AS total_revenue
        FROM admissions a
        JOIN billing b
        ON a.admission_id = b.admission_id
        GROUP BY a.department
        ORDER BY total_revenue DESC
        """)
        result = connection.execute(query).fetchall()

    return [
        {"Department": r[0], "Total Revenue": float(r[1])}
        for r in result
    ]
@router.get("/billing-details")
def billing_details():
    with engine.connect() as connection:
        query = text("""
        SELECT
            b.bill_id,
            a.department,
            a.admission_date,
            b.cost
        FROM billing b
        JOIN admissions a
        ON b.admission_id = a.admission_id
        ORDER BY a.admission_date
        """)
        result = connection.execute(query).fetchall()

    return [
        {
            "Bill ID": r[0],
            "Department": r[1],
            "Admission Date": str(r[2]),
            "Cost": float(r[3])
        }
        for r in result
    ]
