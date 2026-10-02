import socket
import threading
import des

# Runs in parallel so the terminal can receive messages and wait for keyboard input simultaneously.
def receive_messages(conn, key):
    while True:
        try:
            encrypted_data = conn.recv(1024).decode('utf-8')
            if not encrypted_data:
                break
            # Prints raw data to prove it is encrypted before decryption happens.
            print(f"\n[Ciphertext In] {encrypted_data}")

            # Passing 'False' tells DES to apply the 16 Subkeys in reverse order.
            cipher = des.DES_Algorithm(encrypted_data, key, False)
            decrypted = cipher.DES(viewSteps=False).strip(" ")
            
            print(f"[Client] {decrypted}\n> ", end="")
        except Exception as e:
            print(f"\nConnection closed: {e}")
            break

def main():
    print("=== TERMINAL SETUP ===")

    # Users agree on the key offline. It is typed locally and never sent over the socket.   
    while True:
        shared_key = input("Enter 8-character Secret Key: ")
        if len(shared_key) == 8:
            break
        print("Error: Key must be exactly 8 characters long.")

    host = input("Enter IP (press Enter for localhost): ") or "127.0.0.1"
    port_input = input("Enter Port (press Enter for 8080): ")
    port = int(port_input) if port_input else 8080

    # Claims a port on this machine and passively listens for incoming connections.
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)

    # Pauses execution here until a client connects, then creates a dedicated 'conn' channel.
    print(f"\nWaiting for client on {host}:{port}...")
    conn, addr = server.accept()
    print(f"Connected to {addr[0]}")

    threading.Thread(target=receive_messages, args=(conn, shared_key), daemon=True).start()
    
    while True:
        msg = input("> ")
        if msg.lower() == 'exit':
            break
        if not msg:
            continue

        # Encrypts the typed plaintext using the local key before sending it to the socket.
        cipher = des.DES_Algorithm(msg, shared_key)
        encrypted_msg = cipher.DES(viewSteps=False)
        
        conn.send(encrypted_msg.encode('utf-8'))
        
    conn.close()
    server.close()

if __name__ == "__main__":
    main()