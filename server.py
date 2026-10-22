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
PORT = 5000

# Single service queue stored in memory.
queue = []
next_ticket = 1


def process_request(request):
    """Process a received request and return a response."""
    global next_ticket

    action = request.get("action")

    if action == "request_ticket":
        name = request.get("name", "")

        if not isinstance(name, str) or not name.strip():
            return {
                "success": False,
                "message": "The name cannot be empty."
            }

        # The ticket number is defined exclusively by the server.
        person = {"ticket": next_ticket, "name": name.strip()}
        queue.append(person)
        next_ticket += 1

        return {
            "success": True,
            "message": "Ticket issued successfully.",
            "ticket": person["ticket"],
            "name": person["name"]
        }

    if action == "check_queue":
        return {
            "success": True,
            "queue": list(queue),
            "quantity": len(queue)
        }

    if action == "call_next":
        if not queue:
            return {
                "success": False,
                "message": "There are no people waiting for service."
            }

        # FIFO: remove the first person who entered the queue.
        person = queue.pop(0)
        return {
            "success": True,
            "message": "Person called for service.",
            "ticket": person["ticket"],
            "name": person["name"]
        }

    return {"success": False, "message": "Invalid operation."}


def start_server():
    """Create the TCP socket and handle one connection at a time."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()

        print(f"Server started on port {PORT}.")
        print("Waiting for connections...\n")

        while True:
            connection, address = server.accept()

            with connection:
                try:
                    with connection.makefile("r", encoding="utf-8", newline="\n") as input_file:
                        line = input_file.readline()

                    if not line:
                        print(f"{address}: connection closed without a message.")
                        continue

                    try:
                        request = json.loads(line)
                    except json.JSONDecodeError:
                        request = None
                        response = {
                            "success": False,
                            "message": "Invalid JSON message."
                        }
                    else:
                        if not isinstance(request, dict):
                            response = {
                                "success": False,
                                "message": "The request must be a JSON object."
                            }
                        else:
                            print(f"Client {address}")
                            print("Request:", request)
                            response = process_request(request)

                    message = json.dumps(response, ensure_ascii=False) + "\n"
                    connection.sendall(message.encode("utf-8"))

                    print("Response:", response)
                    print("-" * 50)

                except (OSError, UnicodeDecodeError) as error:
                    print(f"Error handling {address}: {error}")


if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("\nServer closed.")
