import socket
import threading
import des

SHARED_KEY = "SECRET88" 

def receive_messages(conn):
    while True:
        try:
            encrypted_data = conn.recv(1024).decode('utf-8')
            if not encrypted_data:
                break
                
            print(f"\n[Ciphertext In] {encrypted_data}")
            
            decrypted = des.decrypt(encrypted_data, SHARED_KEY)
            print(f"[Client] {decrypted}\n> ", end="")
        except Exception as e:
            print(f"Connection closed: {e}")
            break

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 8080))
    server.listen(1)
    
    print("Waiting for client on port 8080...")
    conn, addr = server.accept()
    print(f"Connected to {addr[0]}")
    
    threading.Thread(target=receive_messages, args=(conn,), daemon=True).start()
    
    while True:
        msg = input("> ")
        if msg.lower() == 'exit':
            break

        encrypted_msg = des.encrypt(msg, SHARED_KEY)
        conn.send(encrypted_msg.encode('utf-8'))
        
    conn.close()
    server.close()

if __name__ == "__main__":
    main()