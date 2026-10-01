import socket
import threading
import des

SHARED_KEY = "SECRET88" 

def receive_messages(sock):
    while True:
        try:
            encrypted_data = sock.recv(1024).decode('utf-8')
            if not encrypted_data:
                break
                
            print(f"\n[Ciphertext In] {encrypted_data}")
            decrypted = des.decrypt(encrypted_data, SHARED_KEY)
            print(f"[Server] {decrypted}\n> ", end="")
        except:
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(('127.0.0.1', 8080))
        print("Connected securely to Server")
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()
    
    while True:
        msg = input("> ")
        if msg.lower() == 'exit':
            break
            
        encrypted_msg = des.encrypt(msg, SHARED_KEY)
        client.send(encrypted_msg.encode('utf-8'))
        
    client.close()

if __name__ == "__main__":
    main()