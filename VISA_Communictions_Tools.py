import pyvisa as visa
import pyvisa.constants as pyconst
import time
from datetime import datetime
import sys
import os
import time

# ======================================================================
#      DEFINE THE SMU CLASS INSTANCE HERE
# ======================================================================
class VisaCommunications:
    def __init__(self):
        self.echo_commands = 0
        self.resource_manager = None
        self.instrument_object = None
        self.pure_sockets = None
        self.simulate = 0

    """*********************************************************************************
        Function: instrument_connect(resource_mgr, instrument_object, instrument_resource_string, 
                                     timeout, do_id_query, do_reset, do_clear) 
    
        Purpose: Open an instance of an instrument object for remote communication.
    
        Parameters:
            resource_mgr (object) - Instance of a resource manager object.
    
            instrument_object (object) - Instance of an instrument object to be initialized
                                         within this function. 
    
            instrument_resource_string (string) - The VISA resource string associated with
                                                  a specific instrument defining its connection
                                                  characteristics (communications type, model,
                                                  serial number, etc.)
            timeout (int) - Time in milliseconds to wait before the communication transaction
                            with the target instrument is considered failed (timed out)
            do_id_query (int) - A flag that determines whether or not to query and print the 
                                instrument ID string. 
            do_reset (int) - A flag that determines whether or not to issue a reset command to
                             the instrument during this connection. 
            do_clear (int) - A flag that determines whether or not to issue a clear command to 
                             the instrument during this connection. 
    
        Returns:
            None
    
        Revisions:
            2019-08-07    JJB    Initial revision.
    *********************************************************************************"""


    def instrument_connect(self,
                           instrument_resource_string="",
                           timeout=2000, do_id_query=0,
                           do_reset=0,
                           do_clear=0,
                           resource_mgr=None,
                           baud_rate=9600,
                           data_bits=8,
                           parity=pyconst.Parity.none,
                           stop_bits=pyconst.StopBits.one,
                           flow_control=0,
                           read_terminator="\n",
                           simulate=0,
                           echo_commands=0):

        if resource_mgr == None:
            self.resource_manager = visa.ResourceManager()  # Opens the resource manager

        if not self.simulate:
            self.instrument_object = self.resource_manager.open_resource(instrument_resource_string)

            # Check for the SOCKET as part of the instrument ID string and set the following accordingly...
            if "SOCKET" in instrument_resource_string:
                self.instrument_object.write_termination = "\n"
                self.instrument_object.read_termination = "\n"
                self.instrument_object.send_end = True
            elif "ASRL" in instrument_resource_string:
                self.instrument_object.baud_rate = baud_rate
                self.instrument_object.data_bits = data_bits
                self.instrument_object.parity = parity   #pyconst.Parity.odd
                self.instrument_object.stop_bits = stop_bits     #pyconst.StopBits.one
                self.instrument_object.flow_control = flow_control
                self.instrument_object.write_termination = "\n"
                self.instrument_object.read_termination = read_terminator
                self.instrument_object.send_end = True
            elif "GPIB" in instrument_resource_string:
                # do nothing or something...
                print("GPIB")
                self.pure_sockets = 0
            elif "USB" in instrument_resource_string:
                # do nothing or something...
                print("USB")
                self.pure_sockets = 0
            else:
                # Assume a sockets connection; set the flag
                self.pure_sockets = 1

            if do_id_query == 1:
                print(self.instrument_query("*IDN?"))
            if do_reset == 1:
                self.instrument_write(self.instrument_object, "*RST")
            if do_clear == 1:
                self.instrument_object.clear()
            self.instrument_object.timeout = timeout

        return self.resource_manager, self.instrument_object

    """*********************************************************************************
            Function: instrument_disconnect(instrument_object)

            Purpose: Break the VISA connection between the controlling computer
                     and the target instrument.

            Parameters:
                instrument_object (object) - Instance of an instrument object.

            Returns:
                None

            Revisions:
                2019-08-21    JJB    Initial revision.
        *********************************************************************************"""

    def instrument_disconnect(self):
        if not self.simulate:
            self.instrument_object.close()
        return
    
    """*********************************************************************************
        Function: instrument_write(instrument_object, my_command)
    
        Purpose: Issue controlling commands to the target instrument.
    
        Parameters:
            instrument_object (object) - Instance of an instrument object.
    
            my_command (string) - The command issued to the instrument to make it 
                                  perform some action or service. 
        Returns:
            None
    
        Revisions:
            2019-08-21    JJB    Initial revision.
    *********************************************************************************"""


    def instrument_write(self, my_command):
        if self.echo_commands == 1:
            print(my_command + "\n")
        if self.simulate != 1:
            self.instrument_object.write(my_command)
        return


    """*********************************************************************************
        Function: instrument_read(instrument_object)
    
        Purpose: Used to read commands from the instrument.
    
        Parameters:
            instrument_object (object) - Instance of an instrument object.
    
        Returns:
            <<<reply>>> (string) - The requested information returned from the 
                        target instrument. Obtained by way of a caller
                        to instrument_read().
    
        Revisions:
            2019-08-21    JJB    Initial revision.
    *********************************************************************************"""


    def instrument_read(self):
        if self.simulate != 1:
            return self.instrument_object.read()
        else:
            return ""


    """*********************************************************************************
        Function: instrument_query(instrument_object, my_command)
    
        Purpose: Used to send commands to the instrument  and obtain an information string from the instrument.
                 Note that the information received will depend on the command sent and will be in string
                 format.
    
        Parameters:
            instrument_object (object) - Instance of an instrument object.
    
            my_command (string) - The command issued to the instrument to make it 
                          perform some action or service. 
        Returns:
            <<<reply>>> (string) - The requested information returned from the 
                        target instrument. Obtained by way of a caller
                        to instrument_read().
    
        Revisions:
            2019-08-21    JJB    Initial revision.
    *********************************************************************************"""


    def instrument_query(self, my_command):
        if self.echo_commands == 1:
            print(my_command)
        if self.simulate != 1:
            return self.instrument_object.query(my_command)
        else:
            return "Bubbles"




