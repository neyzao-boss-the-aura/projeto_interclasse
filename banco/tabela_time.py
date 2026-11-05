from flask import flash
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database import *

def select_todos():
    # Buscar todos os times no banco
    # 1- Montar o select
    times_sql = select(Time)
    # 2- Executar o select
    times = db_session.execute(times_sql).scalars().all()

    return times

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

def select_um(id_time):
    time_sql = select(Time).where(Time.id == id_time)
    time = db_session.execute(time_sql).scalar_one_or_none()
    return time
