import os
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, DateTime, func
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, scoped_session, DeclarativeBase
from sqlalchemy.sql import func
from flask_login import UserMixin

engine = create_engine("mysql+pymysql://root:senaisp@localhost:3306/interclasse_db")

db_session = scoped_session(sessionmaker(bind=engine))

#Base = declarative_base()

class Base(DeclarativeBase):
    pass

class Time(Base):
    __tablename__ = "times"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    turma = Column(String(20))
    responsavel = Column(String(100))

class Jogador(Base):
    __tablename__ = "jogadores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    numero_camisa = Column(Integer, nullable=False)
    posicao = Column(String(50), nullable=False)
    time_id = Column(Integer, ForeignKey("times.id", ondelete="CASCADE"), nullable=False)


class Partida(Base):
    __tablename__ = "partidas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    time_casa_id = Column(Integer, ForeignKey("times.id", ondelete="CASCADE"), nullable=False)
    time_visitante_id = Column(Integer, ForeignKey("times.id", ondelete="CASCADE"), nullable=False)
    gols_casa = Column(Integer, default=0)
    gols_visitante = Column(Integer, default=0)
    data_partida = Column(Date, nullable=False)

class Movimentacao(Base):
    __tablename__ = "movimentacoes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    jogador_id = Column(Integer, ForeignKey("jogadores.id", ondelete="SET NULL"))
    time_origem_id = Column(Integer, ForeignKey("times.id", ondelete="SET NULL"))
    time_destino_id = Column(Integer, ForeignKey("times.id", ondelete="SET NULL"))
    data_movimentacao = Column(DateTime)

    def __repr__(self):
        return f"<Movimentacao {self.jogador_id}>"

class Usuario(Base, UserMixin):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    atualizado_em = Column(DateTime, onupdate=func.now())
    criado_em = Column(DateTime, onupdate=func.now())

    #Senha
    def set_password(self, password):
        self.senha_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.senha_hash, password)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

