# TCP Queue System

A ticket queue management system developed in Python using native TCP sockets. The application allows clients to request tickets, check the waiting queue, and call the next person for service through a centralized server.

## Features

- **Ticket generation:** Assigns unique, sequential ticket numbers starting at 1.
- **Queue consultation:** Displays the waiting queue, including ticket numbers, names, and the total number of people waiting.
- **Next ticket calling:** Calls and removes the first person from the queue, following the FIFO (First In, First Out) principle.
- **Multiple clients:** Allows multiple clients to interact with the same server and share a single queue.
- **TCP communication:** Uses Python's native `socket` module for network communication.
- **JSON protocol:** Exchanges requests and responses using JSON messages terminated by a newline (`\n`).
- **Error handling:** Handles empty names, invalid menu options, empty queues, and connection failures.

## Technologies

- Python 3
- TCP sockets (`socket`)
- JSON (`json`)

No external Python packages are required.

## Project Structure

```text
tcp-queue-system/
├── server.py
├── client.py
└── README.md
```

- `server.py`: Manages the queue, generates tickets, and processes client requests.
- `client.py`: Provides a text-based interface for interacting with the server.
- `README.md`: Contains project documentation and execution instructions.

## Getting Started

### Prerequisites

- Python 3 installed on the server and client computers.
- Network connectivity between the clients and the server.
- TCP port `5000` available on the server.

### Running the Server

Open a terminal in the project directory and run:

```bash
python server.py
```

The server will start listening for incoming TCP connections on port `5000`.

### Running the Client

Open another terminal and run:

```bash
python client.py
```

When prompted, enter the server's IP address.

For testing on the same computer, use:

```text
127.0.0.1
```

For clients running on different computers, enter the server computer's local network IP address. Ensure that the firewall allows incoming TCP connections on port `5000`.

## Usage

The client provides the following menu:

```text
===== SISTEMA DE ATENDIMENTO =====
1 - Retirar senha
2 - Consultar fila
3 - Chamar próxima senha
4 - Sair
```

- **Request a ticket:** Enter the person's full name to receive the next available ticket number.
- **Check the queue:** View all people waiting for service and the current queue size.
- **Call the next person:** Call the person at the front of the queue.
- **Exit:** Close the client without shutting down the server.

Multiple client instances can connect to the same server and operate on the same queue.

## Communication Protocol

The application uses TCP sockets to exchange JSON messages. Each request and response occupies a single line terminated by `\n`.

Example request:

```json
{"acao": "retirar_senha", "nome": "Ana Silva"}
```

Example response:

```json
{
  "sucesso": true,
  "mensagem": "Senha emitida com sucesso.",
  "senha": 1,
  "nome": "Ana Silva"
}
```

Each client operation opens a new TCP connection. The server processes connections sequentially and sends a response for each validly received request.

## Testing

To verify the application:

1. Start the server.
2. Open at least two client instances.
3. Alternate between clients to request three tickets.
4. Verify that the generated ticket numbers are `1`, `2`, and `3`.
5. Check the queue from both clients.
6. Call the next person three times and verify the order: `1`, `2`, and `3`.
7. Attempt to call another person when the queue is empty.
8. Exit one client and verify that the server remains operational.

## Notes

- The server is the sole authority responsible for generating ticket numbers.
- All clients connected to the same server share a single in-memory queue.
- Queue data is not persisted and will be lost when the server shuts down.
- The server can be stopped manually with `Ctrl+C`.

## Academic Project

Developed as a practical assignment on computer networks, focusing on TCP socket communication, client-server architecture, and queue management.
