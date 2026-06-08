import json

def enviar_mensaje(sock, datos):
    """Convierte un diccionario a JSON, calcula su tamaño y lo envía."""
    payload = json.dumps(datos).encode('utf-8')
    
    sock.sendall(len(payload).to_bytes(4, byteorder='big'))
    # Enviamos el contenido real
    sock.sendall(payload)

def recibir_mensaje(sock):
    """Lee el encabezado de 4 bytes y luego lee el mensaje completo."""
    try:
        # Lee el tamaño del payload
        raw_length = sock.recv(4)
        if not raw_length:
            return None
        length = int.from_bytes(raw_length, byteorder='big')
        
        # Lee los bytes del mensaje según el tamaño especificado
        data = bytearray()
        while len(data) < length:
            packet = sock.recv(length - len(data))
            if not packet:
                return None
            data.extend(packet)
            
        return json.loads(data.decode('utf-8'))
    except (ConnectionResetError, BrokenPipeError):
        return None
        