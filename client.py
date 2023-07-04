import socket
import struct

def receive_market_data():
    host = '127.0.0.1'  # Server IP address
    port = 9053  # Server port

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            print(f"Connected to Market Data Server at {host}:{port}")
            packet_data = client_socket.recv(130)
            process_market_data_packet(packet_data)
            client_socket.close()
            print("Client disconnected")
    except ConnectionRefusedError:
        print(f"Connection refused: Unable to connect to {host}:{port}")
    except OSError as e:
        print(f"Error occurred: {str(e)}")


def process_market_data_packet(packet_data):
    packet_length = struct.unpack('>I', packet_data[:4])[0]
    trading_symbol = packet_data[4:34].decode('ascii').strip()
    sequence_number = struct.unpack('>Q', packet_data[34:42])[0]
    timestamp = struct.unpack('>Q', packet_data[42:50])[0]
    ltp = struct.unpack('>Q', packet_data[50:58])[0]
    ltq = struct.unpack('>Q', packet_data[58:66])[0]
    volume = struct.unpack('>Q', packet_data[66:74])[0]
    bid_price = struct.unpack('>Q', packet_data[74:82])[0]
    bid_quantity = struct.unpack('>Q', packet_data[82:90])[0]
    ask_price = struct.unpack('>Q', packet_data[90:98])[0]
    ask_quantity = struct.unpack('>Q', packet_data[98:106])[0]
    open_interest = struct.unpack('>Q', packet_data[106:114])[0]
    prev_close_price = struct.unpack('>Q', packet_data[114:122])[0]
    prev_open_interest = struct.unpack('>Q', packet_data[122:130])[0]

    # Print the received data
    print("Packet Length:", packet_length)
    print("Trading Symbol:", trading_symbol)
    print("Sequence Number:", sequence_number)
    print("Timestamp:", timestamp)
    print("Last Traded Price (LTP):", ltp)
    print("Last Traded Quantity:", ltq)
    print("Volume:", volume)
    print("Bid Price:", bid_price)
    print("Bid Quantity:", bid_quantity)
    print("Ask Price:", ask_price)
    print("Ask Quantity:", ask_quantity)
    print("Open Interest (OI):", open_interest)
    print("Previous Close Price:", prev_close_price)
    print("Previous Open Interest:", prev_open_interest)
    print()


if __name__ == '__main__':
    receive_market_data()
