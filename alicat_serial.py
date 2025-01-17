#code to push. not tested.
import serial
import time
import serial.tools.list_ports
import asyncio
import alicat
from alicat import FlowController

class AlicatMFC:
    def __init__(self, port: str, baudrate: int = 19200, timeout: float = 1.0, rtscts: bool = False, dsrdtr: bool = False, write_timeout: float = None, inter_byte_timeout: float = None, async_func=None):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.rtscts = rtscts
        self.dsrdtr = dsrdtr
        self.write_timeout = write_timeout
        self.inter_byte_timeout = inter_byte_timeout
        self.mfc = None


    @staticmethod
    def list_available_ports():
        """List all available serial ports."""
        ports = list(serial.tools.list_ports.comports())
        if not ports:
            print("No available serial ports detected.")
            return []
        print("Available Ports:")
        for i, port in enumerate(ports):
            print(f"{i + 1}: {port.device}")
        return [port.device for port in ports]

    def connect(self):
        """Initialize the serial connection to the MFC."""
        self.mfc = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            timeout=self.timeout,
            rtscts=self.rtscts,
            dsrdtr=self.dsrdtr,
            write_timeout=self.write_timeout,
            inter_byte_timeout=self.inter_byte_timeout
        )
        print(f"Connected to {self.port}.")

    def close(self):
        """Close the serial connection."""
        if self.mfc and self.mfc.is_open:
            self.mfc.close()
            print("Connection closed.")

    def open_valve(self):
        """Send command to open the valve."""
        if self.mfc and self.mfc.is_open:
            self.mfc.write(b'VALVE OPEN\n')
            print("Valve opened.")

    def close_valve(self):
        """Send command to close the valve."""
        if self.mfc and self.mfc.is_open:
            self.mfc.write(b'VALVE CLOSE\n')
            print("Valve closed.")

    def set_flow(self, flow_rate: float):
        """Set the flow rate."""
        if self.mfc and self.mfc.is_open:
            command = f'FLOW {flow_rate}\n'.encode('utf-8')
            self.mfc.write(command)
            print(f"Flow rate set to {flow_rate}.")

    def wrapper_alicat(self, *args, **kwargs):
        async def async_operations():
            async with FlowController('COM3', 'A') as flow_controller:
                try:
                    status = await flow_controller.get()
                    print(f"Device Status: {status}")

                    flow_rate = float(input("Enter flow rate (L/min): "))
                    await flow_controller.set_flow_rate(flow_rate)
                    print(f"Flow rate set to {flow_rate} L/min.")

                    pressure = float(input("Enter pressure (bar): "))
                    await flow_controller.set_pressure(pressure)
                    print(f"Pressure set to {pressure} bar.")

                    gas_type = input("Enter gas type (N2/O2/CO2/Ar): ")
                    await flow_controller.set_gas(gas_type)
                    print(f"Gas set to {gas_type}.")

                except Exception as e:
                    print(f"An error occurred: {e}")

        def run_sync():
            asyncio.run(async_operations())

        return run_sync









