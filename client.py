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

PORTA = 5000


def comunicar(ip_servidor, solicitacao):
    """Envia uma solicitação TCP e recebe a resposta JSON."""
    try:
        with socket.create_connection((ip_servidor, PORTA), timeout=5) as cliente:
            mensagem = json.dumps(solicitacao, ensure_ascii=False) + "\n"
            cliente.sendall(mensagem.encode("utf-8"))

            with cliente.makefile("r", encoding="utf-8", newline="\n") as entrada:
                linha = entrada.readline()

            if not linha:
                print("O servidor encerrou a conexão sem responder.")
                return None

            return json.loads(linha)

    except (OSError, json.JSONDecodeError, UnicodeDecodeError) as erro:
        print(f"Não foi possível concluir a comunicação: {erro}")
        return None


def mostrar_menu():
    print("\n===== SISTEMA DE ATENDIMENTO =====")
    print("1 - Retirar senha")
    print("2 - Consultar fila")
    print("3 - Chamar próxima senha")
    print("4 - Sair")
    return input("Escolha uma opção: ").strip()


def executar():
    ip_servidor = input(
        "Informe o IP do servidor (ex.: 127.0.0.1): "
    ).strip()

    if not ip_servidor:
        print("O IP do servidor não pode estar vazio.")
        return

    while True:
        opcao = mostrar_menu()

        if opcao == "1":
            nome = input("Nome completo: ").strip()
            if not nome:
                print("O nome não pode estar vazio.")
                continue

            resposta = comunicar(ip_servidor, {
                "acao": "retirar_senha",
                "nome": nome
            })

            if resposta is not None:
                if resposta.get("sucesso"):
                    print(f"\nSenha emitida: {resposta['senha']}")
                    print(f"Nome: {resposta['nome']}")
                else:
                    print(resposta.get("mensagem", "Operação não realizada."))

        elif opcao == "2":
            resposta = comunicar(ip_servidor, {"acao": "consultar_fila"})

            if resposta is not None:
                if not resposta.get("sucesso"):
                    print(resposta.get("mensagem", "Erro na consulta."))
                    continue

                pessoas = resposta.get("fila", [])
                print("\n===== FILA DE ESPERA =====")

                if pessoas:
                    for pessoa in pessoas:
                        print(f"Senha {pessoa['senha']} - {pessoa['nome']}")
                else:
                    print("A fila está vazia.")

                print(f"Total de pessoas aguardando: {resposta['quantidade']}")

        elif opcao == "3":
            resposta = comunicar(ip_servidor, {"acao": "chamar_proxima"})

            if resposta is not None:
                if resposta.get("sucesso"):
                    print(
                        f"\nChamando senha {resposta['senha']} - "
                        f"{resposta['nome']}"
                    )
                else:
                    print(resposta.get("mensagem", "Não foi possível chamar."))

        elif opcao == "4":
            print("Cliente encerrado.")
            break

        else:
            print("Opção inválida. Escolha uma opção de 1 a 4.")


if __name__ == "__main__":
    try:
        executar()
    except (KeyboardInterrupt, EOFError):
        print("\nCliente encerrado.")
