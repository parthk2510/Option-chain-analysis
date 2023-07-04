import socket
import struct
import time

def publish_market_data():
    host = '127.0.0.1'  # Server IP address
    port = 9053  # Server port

    # Example data
    trading_symbol = "MAINIDX"
    sequence_number = 1
    timestamp = int(time.time() * 1000)
    ltp = 1854880
    ltq = 0
    volume = 0
    bid_price = 0
    bid_quantity = 0
    ask_price = 0
    ask_quantity = 0
    open_interest = 0
    prev_close_price = 1848775
    prev_open_interest = 0

    
    packet_data = struct.pack(
        '>I30sQQQQQQQQQQQQ',
        130,
        trading_symbol.encode('ascii'),
        sequence_number,
        timestamp,
        ltp,
        ltq,
        volume,
        bid_price,
        bid_quantity,
        ask_price,
        ask_quantity,
        open_interest,
        prev_close_price,
        prev_open_interest
    )

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((host, port))
            server_socket.listen(1)
            print(f"Server listening on {host}:{port}")

            while True:
                client_socket, client_address = server_socket.accept()
                print(f"Client connected: {client_address}")
                client_socket.sendall(packet_data)
                print("Market data packet sent successfully")
                client_socket.close()
                print("Client disconnected")
    except OSError as e:
        print(f"Error occurred: {str(e)}")


if __name__ == '__main__':
    publish_market_data()
