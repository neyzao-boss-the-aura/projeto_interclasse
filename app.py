import time
from os import times
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import select, Time, Jogadores
from sqlalchemy.exc import SQLAlchemyError
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy.testing.pickleable import User

from database import *
from banco import tabela_partida, tabela_time, tabela_jogador, tabela_movimentacao

app = Flask(__name__)
#secret_key aqui apenas momento de criação, em produção deve ser protegida
app.secret_key = "chave-secreta-interclasse-2026"

#Configurar Flask-login
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Faça login para acessar"

#Prevenir gargalo "too many connections"
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

#Carregar informações do usuário logado
@login_manager.user_loader
def load_user(user_id):
    return db_session.get(Usuario, int(user_id))

#Interface de autenticação
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("senha", "").strip()

        usuario_sql = select(Usuario).where(Usuario.email == email)
        usuario_resultado = db_session.execute(usuario_sql).scalar()

        if not usuario_resultado:
            flash("Falha ao autenticar", "error")
            return render_template("login.html")

        if usuario_resultado and usuario_resultado.check_password(password):
            login_user(usuario_resultado)
            return redirect(url_for("dashboard"))

    return render_template(
        "login.html",
    registro= request.args.get("registro") == 'True'
    )

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "").strip()

        if not nome and not email and not senha :
            flash("PREENCHA OS CAMPOS", "error")
            return redirect (url_for("registro"))

        usuario_sql = select(Usuario).where (Usuario.email == email)
        usuario_email = db_session.execute(usuario_sql).scalars().all()

        if usuario_email:
            flash("Email já cadastrado")
            return redirect (url_for("registro"))
        try:
            novo_usuario = Usuario(
                nome=nome,
                email=email)

            novo_usuario.set_password(senha)
            db_session.add(novo_usuario)
            db_session.commit()
            flash("Usuario cadastrado com sucesso", "success")

        except SQLAlchemyError as e:
            print(f"SQLAlchemyError: {e}")
            flash("Erro no banco")
            pass
        except Exception as e:
            print(f"Erro ao registrar: {e}")
            flash("Erro ao registrar", "error")
            return redirect (url_for("registro"))
        return render_template("login.html")

@app.route("/")
@login_required
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
    jogadores_sql = select(Jogador, Time).join(Time, Jogador.time_id == Time.id)
    # 2- Executar o select
    jogadores = db_session.execute(jogadores_sql).all()
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
    tabela_jogador.salvar_jogador(db_session.execute(jogadores_sql)).scalars().all()
    tabela_jogador.salvar_jogador(nome=nome, turma=turma, responsavel=responsavel)
    # 1- Pegar os valores digitados no formulário
    times_sql = select(Time)
    # 2- Executar o select
    times = db_session.execute(times_sql).scalars().all()
    return render_template("jogadores.html", jogadores=jogadores, times=times)

@app.route("/jogadores/<id_jogador>", methods=["GET", "POST"])
def editar_jogador(id_jogador):
    #Buscar o jogador no banco
    jogador = tabela_jogador.select_um(id_jogador)
    #Salvar as alterações
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        numero_camisa = request.form.get("numero_camisa") or None
        posicao = request.form.get("posicao", "").strip()
        time_id = request.form.get("time_id") or None

        # 2- Verificar se foi digitado
        if not nome:
            flash("PREENCHA O NOME", "error")
        elif not numero_camisa:
            flash("PREENCHA O NÚMERO DA CAMISA", "error")
        elif not posicao:
            flash("PREENCHA A POSIÇÃO", "error")
        elif not time_id:
            flash("PREENCHA O TIME", "error")
        else:
            jogador.nome = nome
            jogador.numero_camisa = numero_camisa
            jogador.posicao = posicao
            jogador.time_id = int(time_id)
            db_session.commit()

    #Carregar as informações
    jogadores = tabela_jogador.select_todos()
    return render_template("jogadores.html", jogadores=jogadores, editar = editar_jogador)

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

@app.route("/time/id_time")
def detalhes_time():

    jogadores = []
    partidas = []
    return render_template("time_detalhes.html", time=time, jogadores=jogadores)

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

@app.route("/movimentacao/nova<int:id_jogador>", methods=["GET", "POST"])

@app.route("/movimentacao/nova", methods=["GET", "POST"])
def nova_movimentacao(id_jogador=None):
    if request.method == "POST":
        jogador_id = request.form.get("jogador_id")
        time_destino_id = request.form.get("time_destino_id")

        if not jogador_id:
            flash("preencha o jogador id", "error")
            return render_template("movimentacao.html")
        if not time_destino_id:
            flash("preencha o time destino id", "error")
            return render_template("movimentacao.html")

        tabela_movimentacao.salvar_movimentacao(jogador_id, time_destino_id)
        return redirect(url_for("nova_movimentacao"))
    # Carregar dados para movimentação
    movimentacoes = tabela_movimentacao.select_todos()
    jogadores = tabela_jogador.select_todos()
    times = tabela_time.select_todos()

    return render_template(
        "movimentacoes.html",
        movimentacoes=movimentacoes,
        jogadores=jogadores,
        times=times,
        jogador_selecionado_id=id_jogador)


if __name__ == "__main__":
    app.run(debug=True)
