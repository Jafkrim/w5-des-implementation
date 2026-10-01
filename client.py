import socket
import threading
import des

def receive_messages(sock, key):
    while True:
        try:
            encrypted_data = sock.recv(1024).decode('utf-8')
            if not encrypted_data:
                break
            print(f"\n[Ciphertext In] {encrypted_data}")

            cipher = des.DES_Algorithm(encrypted_data, key, False)
            decrypted = cipher.DES(viewSteps=False).strip(" ")
            
            print(f"[Server] {decrypted}\n> ", end="")
        except:
            break

def main():
    print("=== TERMINAL SETUP ===")
    
    while True:
        shared_key = input("Enter 8-character Secret Key: ")
        if len(shared_key) == 8:
            break
        print("Error: Key must be exactly 8 characters long.")

    target_ip = input("Enter IP (press Enter for localhost): ") or "127.0.0.1"
    port_input = input("Enter Port (press Enter for 8080): ")
    port = int(port_input) if port_input else 8080

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

        cipher = des.DES_Algorithm(msg, shared_key)
        encrypted_msg = cipher.DES(viewSteps=False)
        
        client.send(encrypted_msg.encode('utf-8'))
        
    client.close()

if __name__ == "__main__":
    main()