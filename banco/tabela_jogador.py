from sqlalchemy import select


def select_todos():
    # 1- Pegar os valores digitados no formulário
    jogadores_sql = select(Jogador)
    # 2- Executar o select
    jogadores = db_session.execute(jogadores_sql).scalars().all()

    # 1- Pegar os valores digitados no formulário
    times_sql = select(Time)
    # 2- Executar o select
    times = db_session.execute(times_sql).scalars().all()
    return render_template("jogadores.html", jogadores=jogadores, times=times)


def salvar_jogador(nome, jogador):
    try:
        novo_jogador = Jogador(nome=nome, numero_camisa=numero_camisa, posicao=posicao, time_id=time_id)
        db_session.add(novo_jogador)
        db_session.commit()
        flash("JOGADOR CADASTRADO COM SUCESSO", "success")
        print(f'{novo_jogador}')
    except SQLAlchemyError as e:
        db_session.rollback()
        flash("OCORREU UM ERRO, DIGITE NOVAMENTE", "error")
        print(f"OCORREU UM ERRO: {e}")