from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

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

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bullying.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        # Inserir dados iniciais se a tabela estiver vazia
        if Denuncia.query.count() == 0:
            inserir_dados_iniciais()

def inserir_dados_iniciais():
    # Denúncias de exemplo
    denuncias = [
        Denuncia(
            tipo='bullying',
            data_ocorrencia=datetime(2023, 10, 15),
            local='Escola - Pátio',
            descricao='Aluno foi empurrado e chamado por apelidos ofensivos durante o recreio',
            envolvidos='João Silva (vítima), Pedro Santos (agressor)',
            testemunhas='Maria Oliveira, Carlos Souza',
            contato='professor@escola.com',
            anonimo=False
        ),
        Denuncia(
            tipo='cyberbullying',
            data_ocorrencia=datetime(2023, 10, 20),
            local='Rede Social - Instagram',
            descricao='Criação de perfil falso com fotos constrangedoras da vítima',
            envolvidos='Ana Costa (vítima), Perfil Fake @ana_falsa (agressor)',
            testemunhas='Vários colegas da escola',
            contato='',
            anonimo=True
        )
    ]
    
    # Estatísticas iniciais
    estatisticas = [
        Estatistica(tipo='prevalencia_geral', valor=30.5, descricao='Estudantes que relatam sofrer bullying'),
        Estatistica(tipo='cyberbullying', valor=15.2, descricao='Sofrem cyberbullying regularmente'),
        Estatistica(tipo='nao_reportam', valor=64.0, descricao='Não reportam o bullying aos adultos'),
        Estatistica(tipo='problemas_saude_mental', valor=2.0, descricao='Maior risco de problemas de saúde mental')
    ]
    
    for denuncia in denuncias:
        db.session.add(denuncia)
    
    for estatistica in estatisticas:
        db.session.add(estatistica)
    
    db.session.commit()