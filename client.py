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

            cipher = des.DES_Algorithm(encrypted_data, SHARED_KEY, False)
            decrypted = cipher.DES(viewSteps=False).strip(" ")
            
            print(f"[Server] {decrypted}\n> ", end="")
        except:
            break

def main():
    print("=== SENDER (CLIENT) SETUP ===")
    target_ip = input("Enter the target Server IP (e.g., 192.168.1.5): ")
    port_input = input("Enter Port (press Enter for 8080): ")
    port = int(port_input) if port_input else 8080

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((target_ip, port))
        print(f"\nConnected securely to {target_ip}:{port}")
    except Exception as e:
        print(f"\nFailed to connect: {e}")
        return

    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()
    
    while True:
        msg = input("> ")
        if msg.lower() == 'exit':
            break
        if not msg:
            continue
            
        cipher = des.DES_Algorithm(msg, SHARED_KEY)
        encrypted_msg = cipher.DES(viewSteps=False)
        
        client.send(encrypted_msg.encode('utf-8'))
        
    client.close()

if __name__ == "__main__":
    main()