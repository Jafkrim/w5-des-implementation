import socket
import threading
import des

# Runs in parallel so the terminal can receive messages and wait for keyboard input simultaneously.
def receive_messages(sock, key):
    while True:
        try:
            encrypted_data = sock.recv(1024).decode('utf-8')
            if not encrypted_data:
                break
            # Prints raw data to prove it is encrypted before decryption happens.
            print(f"\n[Ciphertext In] {encrypted_data}")

            # Passing 'False' tells DES to apply the 16 Subkeys in reverse order.
            cipher = des.DES_Algorithm(encrypted_data, key, False)
            decrypted = cipher.DES(viewSteps=False).strip(" ")
            
            print(f"[Server] {decrypted}\n> ", end="")
        except:
            break

def main():
    print("=== TERMINAL SETUP ===")

    # Users agree on the key offline. It is typed locally and never sent over the socket.
    while True:
        shared_key = input("Enter 8-character Secret Key: ")
        if len(shared_key) == 8:
            break
        print("Error: Key must be exactly 8 characters long.")

    target_ip = input("Enter IP (press Enter for localhost): ") or "127.0.0.1"
    port_input = input("Enter Port (press Enter for 8080): ")
    port = int(port_input) if port_input else 8080

    # Actively reaches out across the network to connect to the Server's IP.
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((target_ip, port))
        print(f"\nConnected securely to {target_ip}:{port}")
    except Exception as e:
        print(f"\nFailed to connect: {e}")
        return

    threading.Thread(target=receive_messages, args=(client, shared_key), daemon=True).start()
    
    while True:
        msg = input("> ")
        if msg.lower() == 'exit':
            break
        if not msg:
            continue

        # Encrypts the typed plaintext using the local key before sending it to the socket.
        cipher = des.DES_Algorithm(msg, shared_key)
        encrypted_msg = cipher.DES(viewSteps=False)
        
        client.send(encrypted_msg.encode('utf-8'))
        
    client.close()

if __name__ == "__main__":
    main()