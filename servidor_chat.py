import socket
import select

# Crear un socket del servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(('0.0.0.0', 12345))
servidor.listen(5)

# Lista para almacenar las conexiones de los clientes
conexiones = [servidor]

print("Servidor iniciado en el puerto 12345...")

try:
    while True:
        # Usar select para manejar múltiples conexiones
        leidos, _, _ = select.select(conexiones, [], [])

        for sock in leidos:
            if sock == servidor:
                # Aceptar nuevas conexiones
                cliente, direccion = servidor.accept()
                conexiones.append(cliente)
                print(f"Cliente conectado desde {direccion}")
            else:
                try:
                    # Recibir mensajes de los clientes
                    mensaje = sock.recv(1024)
                    if mensaje:
                        # Hacer broadcast(Envia informacion) del mensaje a todos los demás clientes
                        for conexion in conexiones:
                            if conexion != servidor and conexion != sock:
                                try:
                                    conexion.send(mensaje)
                                except:
                                    conexion.close()
                                    conexiones.remove(conexion)
                    else:
                        # Eliminar la conexión si no hay mensaje (desconexión)
                        conexiones.remove(sock)
                except:
                    continue
except KeyboardInterrupt:
    print("Servidor cerrado")
    servidor.close()

