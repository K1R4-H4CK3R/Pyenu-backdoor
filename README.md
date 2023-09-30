# Backdoor Interativo

Este é um script Python para criar uma backdoor interativa que permite coletar informações do servidor alvo, executar comandos e transferir arquivos.

## Funcionalidades
- **collect_server_info(host, port):** Coleta informações do servidor alvo.
- **send_file_to_server(socket, file_path):** Envia um arquivo para o servidor.
- **backdoor(host, port):** Inicia uma backdoor interativa para interagir com o servidor.
- **add_custom_command(args, function):** Adiciona um novo comando associado a uma função.
- **ping_server():** Realiza um ping ao servidor alvo.
- **download_file(file_name, socket):** Baixa um arquivo do servidor.
- **view_files():** Visualiza os arquivos no servidor e permite o download.

## Uso
1. Certifique-se de ter Python 3.x instalado no seu sistema.
2. Execute o script usando o comando:
   ```bash
   python Fsec-backdoor.py <host> [--port <port>] [--upload <file_path>] [--destination <host:port>]
   ```

   ## Exemplos de Uso
   Iniciar uma backdoor interativa:
   ```bash
   python Fsec-backdoor.py<host> [--port <port>]
   ```
   Enviar um arquivo para o servidor:
   ```bash
   python Fsec-backdoor.py <host> --upload <file_path> [--port <port>]
   ```
   Iniciar uma backdoor interativa com um destino (site ou IP:porta):
   ```bash
   python Fsec-backdoor.py <host> --destination <host:port>
   ```
   Lembre-se de usar este script de forma ética e em conformidade com todas as leis e regulamentos aplicáveis.
