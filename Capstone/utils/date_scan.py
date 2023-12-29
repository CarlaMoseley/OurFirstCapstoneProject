from ..models import Payment
from datetime import datetime, date
from .email_processor import compose_email
from ..db import db

def scan_units(landlord):
    today = date.today()
    units = landlord.units

    for unit in units:
        if not unit.rent_due:
            continue
        due_date = generate_due_date(unit, today)
        check_for_late_payments(unit, due_date)
        warn_of_future_payments(unit, due_date, today)

def check_for_late_payments(unit, due_date):
    for payment in unit.payments:
        if payment.due_date >= due_date:
            return
    for tenant in unit.tenants:
        new_payment = Payment(
            landlord_id = unit.landlord.id,
            unit_id = unit.id,
            tenant_id = tenant.id,
            amount = unit.rent,
            paid = False,
            due_date = due_date,
            date = None
        )
        db.session.add(new_payment)
    db.session.commit()

def warn_of_future_payments(unit, due_date, today):
    if (due_date - today).days == 7:
        for tenant in unit.tenants:
            compose_email(tenant, 'rent_reminder', due_date=due_date)


def generate_due_date(unit, today):
    if unit.rent_due >= today.day:
        due_date = date(year=today.year, month=today.month, day=unit.rent_due)
    elif today.month == 12:
        due_date = date(year=today.year+1, month=1, day=unit.rent_due) 
    else:
        due_date = date(year=today.year, month=today.month+1, day=unit.rent_due)
    return due_date