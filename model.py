from database import db
from datetime import datetime

class Denuncia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)
    data_ocorrencia = db.Column(db.DateTime, nullable=False)
    local = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    envolvidos = db.Column(db.Text, nullable=False)
    testemunhas = db.Column(db.Text)
    contato = db.Column(db.String(100))
    anonimo = db.Column(db.Boolean, default=False)
    data_registro = db.Column(db.DateTime, default=datetime.now)

class Estatistica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(200))