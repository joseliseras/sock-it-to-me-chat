import socket
import threading

# Crear un evento para detener el hilo de recepción
detener_hilo = threading.Event()

def recibir_mensajes(sock):
    while not detener_hilo.is_set(): #si es false contunua
        try:
            mensaje = sock.recv(1024)
            if not mensaje:
                print("Conexión cerrada por el servidor")
                detener_hilo.set()
                sock.close()
                break
            print(mensaje.decode('utf-8'))
        except:
            if not detener_hilo.is_set(): #si es false imprime y cierra
                print("Error al recibir mensaje")
            sock.close()
            break

def main():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET = IPv4 SOCK_STRAM = TCP
    try:
        cliente.connect(('127.0.0.1', 12345))
        puerto_cliente = cliente.getsockname()[1]
    except:
        print("No se pudo conectar al servidor")
        return

    # Hilo para recibir mensajes
    hilo_recibir = threading.Thread(target=recibir_mensajes, args=(cliente,))
    hilo_recibir.start()

    while True:
        mensaje = input()
        if mensaje == 'salir':
            cliente.close()
            detener_hilo.set()
            print("Salió del chat")
            break
        try:
            mensaje_con_identificador = f"[{puerto_cliente}] {mensaje}"
            cliente.send(mensaje_con_identificador.encode('utf-8'))
        except:
            print("Error al enviar mensaje")
            cliente.close()
            detener_hilo.set()
            break

if __name__ == "__main__":
    main()
