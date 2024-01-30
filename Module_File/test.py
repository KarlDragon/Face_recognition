import socket

# Địa chỉ IP của máy chủ
SERVER_IP = ""  # Thay thế bằng địa chỉ IP thực tế của máy chủ
SERVER_PORT = 12345

try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server_socket.bind((self.IP, self.port))
    self.server_socket.listen(self.amount)

    print("Server is listening on port ")

    while True:
        conn, addr = self.server_socket.accept()
	ip_address, port_number = addr
        print(f"Connection from {addr}")

    server_socket.close()

except socket.error as e:
    print(f"Lỗi khi kết nối đến {SERVER_IP}:{SERVER_PORT}: {e}")
