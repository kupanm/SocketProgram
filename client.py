import socket
from socket import gaierror
import select
def main():
    try:
        date_time = input("Enter 'date' or 'time': ")
        ip_num = input("IP: ")
        port = int(input("Enter port number: "))
        
        if date_time != "date" and date_time != "time":
            print("ERROR: Please input string 'date' or 'time'")
        elif port < 1024 or port > 64000:
            print("ERROR: Please enter port number in range 1024 to 64000")
        else:
            address = socket.getaddrinfo(ip_num, port)
            sock = socket.socket(socket.AF_INET, 
                                 socket.SOCK_DGRAM)
            
            packet = createPacket(date_time)
            address = address[0][4]
            sock.sendto(packet.to_bytes(6, 'big'), address)
            rlist = [sock]
            wlist = []
            elist = []
            rlist, wlist, elist = select.select(rlist, wlist, elist, 1)
            
            if len(rlist) == 0:
                print("ERROR: 1 second passed so unable to receive packet")
            else:
                for s in rlist:
                    dt_response, address = s.recvfrom(5000)
                    receive(dt_response)
                    magicNo = '0x' + str(hex(dt_response[0]))[2:] + str(hex(dt_response[1]))[2:]
                    packet_type = '0x000' + str(dt_response[3])
                    language_code =  '0x000' + str(dt_response[5])
                    year = '0x' + str(hex(dt_response[6]))[2:] + str(hex(dt_response[7]))[2:]
                    
                    year = int(year, 16)
                    month = dt_response[8]
                    day = dt_response[9]
                    hour = dt_response[10]
                    minute = dt_response[11]
                    length = dt_response[12]
                    text = dt_response[13:].decode('utf-8')
        
                    print(f"Magic No: {magicNo}")
                    print(f"Packet Type: {packet_type}")
                    print(f"Language Code: {language_code}")
                    print(f"Year: {year}")
                    print(f"Month: {month}")
                    print(f"Day: {day}")
                    print(f"Hour: {hour}")
                    print(f"Minute: {minute}")
                    print(f"Length: {length}")
                    print(f"Message: {text}")
                    
    except ValueError:
        print("ERROR: Port number is not an integer")
    except gaierror:
        print("ERROR: hostname does not exist or IP address is not well formed")
    except ConnectionResetError:
        print("ERROR: Port does not exist")    



def createPacket(date_time):
    """Will create the dt-request packet"""
    packet = 0
    packet = (packet)|(0x497E << 32)
    packet = (packet)|(0x0001 << 16)
    if date_time == 'date':
        packet = (packet)|(0x0001)
    else:
        packet = (packet)|(0x0002)
    return packet

def receive(packet):
    """Will recieve the dt-response packet from the client and check its correctness"""
    if len(packet) < 13:
        print("ERROR: Packet is not at least 13 bytes of data as required")
        return
    elif packet[0] != 73 and packet[1] != 126:
        print("ERROR: Packet MagicNo field does not equal '0x497E'")
        return
    elif packet[2] != 0 and packet[3] != 2:
        print("ERROR: Packet type is incorrect as it doesn't equal '0x0002'")
        return
    elif packet[4] != 0 and (packet[5] != 1 or packet[5] != 2 or packet[5] != 3):
        print("ERROR: Packet Language type is incorrect as it doesn't equal '0x0001' or '0x0002' or '0x0003'")
        return
    elif (packet[6]+packet[7]) > 2100 or (packet[6]+packet[7]) < 0:
        print("ERROR: Packet year is either larger than 2100 or negative")
        return
    elif packet[8] < 1 or packet[8] > 12:
        print("ERROR: Packet month is out of range (1 to 12)")
        return
    elif packet[9] < 1 or packet[9] > 31:
        print("ERROR: Packet day is out of range (1 to 31)")
        return
    elif packet[10] < 0 or packet[10] > 23:
        print("ERROR: Packet hour is out of range (0 to 23)")
        return
    elif packet[11] < 0 or packet[11] > 59:
        print("ERROR: Packet minute is out of range (0 to 59)")
        return
    elif len(packet) != (13 + packet[12]):
        print("ERROR: Packet length inconsistent")
        return
        

main()



    