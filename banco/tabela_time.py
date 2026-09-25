from flask import flash
from sqlalchemy import select

from database import *

def select_todos():
    # Buscar todos os times no banco
    # 1- Montar o select
    partidas_sql = select(Partida)
    # 2- Executar o select
    partidas = db_session.execute(partidas_sql).scalars().all()

    return partidas

def salvar_time(nome, turma, responsavel):
    #3- Salvar no banco de dados
        try:
            novos_times = Time(nome=nome, turma=turma, responsavel=responsavel)
            db_session.add(novos_times)
            db_session.commit()
            flash("Time cadastrado com sucesso", "success")
        except SQLAlchemyError as e:
            db_session.rollback()
            flash("Ocorreu um erro, digite novamente", "error")
            print(f"Ocorreu um erro: {e}")