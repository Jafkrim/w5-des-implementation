import socket
import threading
import des # Imports your local des.py

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
            print(f"\nConnection closed: {e}")
            break

def main():
    print("=== RECEIVER (SERVER) SETUP ===")
    host = input("Enter IP to bind (press Enter for 0.0.0.0): ") or "0.0.0.0"
    port_input = input("Enter Port (press Enter for 8080): ")
    port = int(port_input) if port_input else 8080

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    
    print(f"\nWaiting for client on {host}:{port}...")
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