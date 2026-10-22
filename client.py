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

PORT = 5000


def communicate(server_ip, request):
    """Send a TCP request and receive a JSON response."""
    try:
        with socket.create_connection((server_ip, PORT), timeout=5) as client:
            message = json.dumps(request, ensure_ascii=False) + "\n"
            client.sendall(message.encode("utf-8"))

            with client.makefile("r", encoding="utf-8", newline="\n") as input_file:
                line = input_file.readline()

            if not line:
                print("The server closed the connection without responding.")
                return None

            return json.loads(line)

    except (OSError, json.JSONDecodeError, UnicodeDecodeError) as error:
        print(f"Communication could not be completed: {error}")
        return None


def show_menu():
    print("\n===== TICKET SERVICE SYSTEM =====")
    print("1 - Request a ticket")
    print("2 - Check the queue")
    print("3 - Call the next ticket")
    print("4 - Exit")
    return input("Choose an option: ").strip()


def run():
    server_ip = input(
        "Enter the server IP address (e.g. 127.0.0.1): "
    ).strip()

    if not server_ip:
        print("The server IP address cannot be empty.")
        return

    while True:
        option = show_menu()

        if option == "1":
            name = input("Full name: ").strip()
            if not name:
                print("The name cannot be empty.")
                continue

            response = communicate(server_ip, {
                "action": "request_ticket",
                "name": name
            })

            if response is not None:
                if response.get("success"):
                    print(f"\nTicket issued: {response['ticket']}")
                    print(f"Name: {response['name']}")
                else:
                    print(response.get("message", "Operation could not be completed."))

        elif option == "2":
            response = communicate(server_ip, {"action": "check_queue"})

            if response is not None:
                if not response.get("success"):
                    print(response.get("message", "Queue query failed."))
                    continue

                people = response.get("queue", [])
                print("\n===== WAITING QUEUE =====")

                if people:
                    for person in people:
                        print(f"Ticket {person['ticket']} - {person['name']}")
                else:
                    print("The queue is empty.")

                print(f"Total people waiting: {response['quantity']}")

        elif option == "3":
            response = communicate(server_ip, {"action": "call_next"})

            if response is not None:
                if response.get("success"):
                    print(
                        f"\nCalling ticket {response['ticket']} - "
                        f"{response['name']}"
                    )
                else:
                    print(response.get("message", "Ticket could not be called."))

        elif option == "4":
            print("Client closed.")
            break

        else:
            print("Invalid option. Choose an option from 1 to 4.")


if __name__ == "__main__":
    try:
        run()
    except (KeyboardInterrupt, EOFError):
        print("\nClient closed.")
