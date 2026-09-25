from os import times
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import select, Time, Jogadores
from sqlalchemy.exc import SQLAlchemyError

from database import *
from banco import tabela_partida, tabela_time, tabela_jogador

app = Flask(__name__)
app.secret_key = "chave-secreta-interclasse-2026"


@app.route("/")
def dashboard():
    # 1- Pegar os valores digitados no formulário
    times_sql = select(Time)
    jogadores_sql = select(Jogador)
    partidas_sql = select(Partida)
    # 2- Executar o select
    times = db_session.execute(times_sql).scalars().all()
    jogadores = db_session.execute(jogadores_sql).scalars().all()
    partidas = db_session.execute(partidas_sql).scalars().all()
    return render_template(
        "dashboard.html",
        total_jogadores=len(jogadores),
        total_times=len(times),
        total_partidas=len(partidas),
    )

@app.route("/jogadores")
def listar_jogadores():
    # 1- Pegar os valores digitados no formulário
    jogadores_sql = select(Jogador)
    # 2- Executar o select
    jogadores = db_session.execute(jogadores_sql).scalars().all()
    return render_template("jogadores.html", jogadores=jogadores)


@app.route("/jogadores/novo", methods=["GET", "POST"])
def novo_jogador():
    #
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        numero_camisa = request.form.get("numero_camisa") or None
        posicao = request.form.get("posicao", "").strip()
        time_id = request.form.get("time_id") or None

        # 2- Verificar se foi digitado
        if not nome:
            flash("PREENCHA O NOME", "error")
            return render_template("jogadores.html")
        if not numero_camisa:
            flash("PREENCHA O NÚMERO DA CAMISA", "error")
            return render_template("jogadores.html")
        if not posicao:
            flash("PREENCHA A POSIÇÃO", "error")
            return render_template("jogadores.html")
        if not time_id:
            flash("PREENCHA O TIME", "error")
            return render_template("jogadores.html")

        # 3- Salvar no banco de dados

    # 1- Pegar os valores digitados no formulário
    jogadores_sql = select(Jogador)
    # 2- Executar o select
    tabela_jogador.salvar(db_session.execute(jogadores_sql)).scalars().all()
    tabela_time.salvar(nome=nome, turma=turma, responsavel=responsavel)
    # 1- Pegar os valores digitados no formulário
    times_sql = select(Time)
    # 2- Executar o select
    times = db_session.execute(times_sql).scalars().all()
    return render_template("jogadores.html", jogadores=jogadores, times=times)


@app.route("/times")
def listar_times():
    # 1- Pegar os valores digitados no formulário
    times_sql = select(Time)
    # 2- Executar o select
    times = db_session.execute(times_sql).scalars().all()
    print(times)
    return render_template("times.html", times=times)


@app.route("/times/novo", methods=["GET", "POST"])
def novo_time():
    #1- Pegar os valores digitados no formulário
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()#strip corta os espaços
        turma = request.form.get("turma", "").strip()
        responsavel = request.form.get("responsavel", "").strip()

    #2- Verificar se foi digitado
        if not nome:
            flash("preencha o nome", "error")
            return render_template("times.html")
        if not turma:
            flash("preencha o turma", "error")
            return render_template("times.html")
        if not responsavel:
            flash("preencha o responsavel", "error")
            return render_template("times.html")

    #3- Salvar no banco de dados
    tabela_time.salvar_time(nome=nome, turma=turma, responsavel=responsavel)

    times = tabela_time.select_todos()
    return render_template("times.html", times=times)

@app.route("/partidas")
def listar_partidas():

    return render_template("partidas.html", partidas=[], times=[])


@app.route("/partidas/nova", methods=["GET", "POST"])
def nova_partida():

    if request.method == "POST":
        time_casa_id = request.form.get("time_casa_id")
        time_visitante_id = request.form.get("time_visitante_id")
        gols_casa = request.form.get("gols_casa") or 0
        gols_visitante = request.form.get("gols_visitante") or 0
        data_partida = request.form.get("data_partida", "").strip()

        # 2- Verificar se foi digitado
        if not time_casa_id:
            flash("preencha o time da casa", "error")
            return render_template("times.html")
        if not time_visitante_id:
            flash("preencha o time visitante", "error")
            return render_template("times.html")
        if not gols_casa:
            flash("preencha os gols da casa", "error")
            return render_template("times.html")
        if not gols_visitante:
            flash("preencha os gols do visitante", "error")
            return render_template("times.html")
        if not data_partida:
            flash("preencha a data da partida", "error")
            return render_template("times.html")

        # 3- Salvar no banco de dados
        tabela_partida.salvar_partidas(time_casa_id=time_casa_id, time_visitante_id=time_visitante_id, gols_casa=gols_casa, gols_visitante=gols_visitante, data_partida=data_partida)
    tabela_partida.select_todos()
    partidas = tabela_partida.select_todos()
    times = tabela_time.select_todos()

    return render_template("partidas.html", partidas=partidas, times=times)

if __name__ == "__main__":
    app.run(debug=True)
