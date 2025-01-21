#code to push. not tested.
import serial
import time
import serial.tools.list_ports
import asyncio
import alicat
from alicat import FlowController

class AlicatMFC:
    def __init__(self, kwargs** ,port: str, baudrate: int = 19200, timeout: float = 1.0, rtscts: bool = False, dsrdtr: bool = False, write_timeout: float = None, inter_byte_timeout: float = None, async_func=None):
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
        #which one is the more efficient the flow_controller (alicat or serial )
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
            #as before we will have to let the user choose which one he wants
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

                    try:
                        print("Please, set the number of the mix : mix_no ")
                        mix_no_user = int(input("mix_no"))
                    except ValueError:
                        print("Error: mix_no must be an integer.")
                        return

                    print("Please, set the name of your mix : mix_name_user")
                    mix_name_user = str(input("please set the name of your mix"))

                    try:
                        print("Please, choose the number of your gases for your mix")
                        mix_nb_gaz = int(input("gases_no"))
                    except ValueError:
                        print("Error: gases_no must be an integer.")
                        return

                    gases = {}
                    for i in range(mix_nb_gaz):
                        gas_type = input(f"Enter gas type for gas {i + 1}: ")
                        try:
                            gas_value = int(input(f"Enter value for {gas_type} (0-256): "))
                            if not (0 <= gas_value <= 256):
                                raise ValueError
                        except ValueError:
                            print("Error: gas value must be an integer between 0 and 256.")
                            return
                        gases[gas_type] = gas_value

                    await flow_controller.create_mix(mix_no=mix_no_user, name=mix_name_user, gases=gases)












                    #not complete : find a way to deal with the gaz,
                    #gaz is not static, it is meant to evolve according to the number defined by the user... but is it possible with alicat (without crashing)  ?
                    #this we will have to find out... .

                except Exception as e:
                    print(f"An error occurred: {e}")

        def run_sync():
            asyncio.run(async_operations())

        return run_sync

    #unit map, #sensor map, #attributes
    #design questions :
    ## locking and unlocking the front display during experiments
    #for the tare
#complete the attributes function, get_attr, capabilities

#MC series controller for gas,
#Multi-variable control: Can control mass flow, volumetric flow,
# or absolute pressure with a single device

#find ways to adapt what we had with bronkhorst to alicat .

def capabilities(self, **kwargs) -> set:
            """Returns a set of capabilities supported by this device."""
            if self.device_type == "pressure":
                caps = {"constant_pressure"}
            else:
                caps = {"constant_flow"}
            return caps

def attrs(self, **kwargs) -> dict[str, Attr] : #taken from tomato, to adapt.
    attrs_dict = {
        "temperature" : Attr(type=float, units ="Celsius"),
        "control_mode" : Attr(type=str, status=True, rw= True),
        "setpoint" : Attr(type=float,) #not complete (yet)



        #complete pressure controller or flow controller with alicat properties

    }

def get_attr(self, attr: str, **kwargs: dict) -> Any :

    #this is from bronkhorst adapt it to alicat
    if attr in self.attrs():
                dde_nr = dde_from_attr(attr)
                ret = self.instrument.readParameter(dde_nr=dde_nr)
                if attr == "control_mode":
                    ret = CONTROL_MAP[ret]
                return ret
            else:
                raise ValueError(f"Unknown attr: {attr!r}")















