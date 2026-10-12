import can
import time

def test_can_bus():
    print("[Michael AI Telemetry Core] Connecting to virtual CAN interface 'vcan0'...")
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')
    
    # Simulate sending a vehicle engine/telemetry frame (CAN ID: 0x123)
    msg = can.Message(arbitration_id=0x123, data=[0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08], is_extended_id=False)
    bus.send(msg)
    print(f"[CAN Bus Outbound] Sent packet: ID={hex(msg.arbitration_id)} Data={msg.data.hex()}")
    
    # Read packet back from the local loopback
    recv_msg = bus.recv(timeout=2.0)
    if recv_msg:
        print(f"[CAN Bus Inbound] Intercepted packet: ID={hex(recv_msg.arbitration_id)} Data={recv_msg.data.hex()}")
        print("[Status] Local SocketCAN interface operational!")
    else:
        print("[Status] No packet detected on vcan0.")

if __name__ == "__main__":
    test_can_bus()
