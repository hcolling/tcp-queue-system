###############################################################################
# Developed by: Gabriel Pires de Farias & Henrique Colling
# Semester: 2026/2
#
# Discipline: Computer Networks: Application and Transport
# Course: Computer Science
# Institution: Universidade do Vale do Rio dos Sinos (UNISINOS)
###############################################################################

import socket
import json

HOST = "0.0.0.0"
PORTA = 5000

# Fila única de atendimento, mantida em memória.
fila = []
proxima_senha = 1


def processar_solicitacao(solicitacao):
    """Processa uma solicitação recebida e devolve uma resposta."""
    global proxima_senha

    acao = solicitacao.get("acao")

    if acao == "retirar_senha":
        nome = solicitacao.get("nome", "")

        if not isinstance(nome, str) or not nome.strip():
            return {
                "sucesso": False,
                "mensagem": "O nome não pode estar vazio."
            }

        # O número é definido exclusivamente pelo servidor.
        pessoa = {"senha": proxima_senha, "nome": nome.strip()}
        fila.append(pessoa)
        proxima_senha += 1

        return {
            "sucesso": True,
            "mensagem": "Senha emitida com sucesso.",
            "senha": pessoa["senha"],
            "nome": pessoa["nome"]
        }

    if acao == "consultar_fila":
        return {
            "sucesso": True,
            "fila": list(fila),
            "quantidade": len(fila)
        }

    if acao == "chamar_proxima":
        if not fila:
            return {
                "sucesso": False,
                "mensagem": "Não há pessoas aguardando atendimento."
            }

        # FIFO: remove a primeira pessoa que entrou na fila.
        pessoa = fila.pop(0)
        return {
            "sucesso": True,
            "mensagem": "Pessoa chamada para atendimento.",
            "senha": pessoa["senha"],
            "nome": pessoa["nome"]
        }

    return {"sucesso": False, "mensagem": "Operação inválida."}


def iniciar_servidor():
    """Cria o socket TCP e atende uma conexão por vez."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PORTA))
        servidor.listen()

        print(f"Servidor iniciado na porta {PORTA}.")
        print("Aguardando conexões...\n")

        while True:
            conexao, endereco = servidor.accept()

            with conexao:
                try:
                    with conexao.makefile("r", encoding="utf-8", newline="\n") as entrada:
                        linha = entrada.readline()

                    if not linha:
                        print(f"{endereco}: conexão encerrada sem mensagem.")
                        continue

                    try:
                        solicitacao = json.loads(linha)
                    except json.JSONDecodeError:
                        solicitacao = None
                        resposta = {
                            "sucesso": False,
                            "mensagem": "Mensagem JSON inválida."
                        }
                    else:
                        if not isinstance(solicitacao, dict):
                            resposta = {
                                "sucesso": False,
                                "mensagem": "A solicitação deve ser um objeto JSON."
                            }
                        else:
                            print(f"Cliente {endereco}")
                            print("Solicitação:", solicitacao)
                            resposta = processar_solicitacao(solicitacao)

                    mensagem = json.dumps(resposta, ensure_ascii=False) + "\n"
                    conexao.sendall(mensagem.encode("utf-8"))

                    print("Resposta:", resposta)
                    print("-" * 50)

                except (OSError, UnicodeDecodeError) as erro:
                    print(f"Erro ao atender {endereco}: {erro}")


if __name__ == "__main__":
    try:
        iniciar_servidor()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
