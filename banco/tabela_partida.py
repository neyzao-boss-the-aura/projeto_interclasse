from flask import flash
from sqlalchemy.exc import SQLAlchemyError

from database import Partida, db_session
from sqlalchemy import select

def select_todos():
    # Buscar todos os times no banco
    # 1- Montar o select
    partidas_sql = select(Partida)
    # 2- Executar o select
    partidas = db_session.execute(partidas_sql).scalars().all()
    return partidas

def salvar_partidas(time_casa_id, time_visitante_id, gols_casa, gols_visitante, data_partida):
    try:
        nova_partida = Partida(time_casa_id=time_casa_id, time_visitante_id=time_visitante_id, gols_casa=gols_casa, gols_visitante=gols_visitante, data_partida=data_partida)
        db_session.add(nova_partida)
        db_session.commit()
        flash("Partida cadastrada com sucesso", "success")
    except SQLAlchemyError as e:
        db_session.rollback()
        flash("Ocorreu um erro, digite novamente", "error")
        print(f"Ocorreu um erro: {e}")