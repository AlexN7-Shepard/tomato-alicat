import serial
import time
import serial.tools.list_ports

class AlicatMFC:
    def __init__(self, port: str, baudrate: int = 19200, timeout: float = 1.0, rtscts: bool = False, dsrdtr: bool = False, write_timeout: float = None, inter_byte_timeout: float = None):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.rtscts = rtscts
        self.dsrdtr = dsrdtr
        self.write_timeout = write_timeout
        self.inter_byte_timeout = inter_byte_timeout
        self.mfc = None

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

    def run_experiment(self, duration: float):
        """Run the experiment for a specified duration."""
        self.open_valve()
        print(f"Experiment running for {duration} seconds...")
        time.sleep(duration)
        self.close_valve()
        print("Experiment completed.")

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


