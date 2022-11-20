"""
    Temp docstring
"""
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

import time

import pyvisa as visa
import pyvisa.constants as pyconst

import VISA_Communictions_Tools as comms

# CONSIDER ADDING TOOLTIPS WITH THE CLASS FOUND HERE:
# https://code.activestate.com/recipes/576688-tooltip-for-tkinter/


class InstrumentConfigurationTools:
    """
    Temp docstring
    """
    def __init__(self):
        # =============================================================
        # Place our main UI definition here
        # =============================================================

        self.root = Tk()
        self.root.title("Keithley Remote Programming Learning Tool 2.0")
        self.root.columnconfigure(0, weight=1)   # for frame/app resizing on the fly
        self.root.rowconfigure(0, weight=1)      # for frame/app resizing on the fly
        # We define a geometry instead of independent height & width because
        # tkinter base behavior of widgets appears to override the intended
        # behavior, meaning our sizes appear to get ignored after the widgets
        # are gridded up.
        self.root.geometry("778x555")

        self.mycomms = None
        self.mycomms = comms.VisaCommunications()
        if self.mycomms.resource_manager is None:
            self.mycomms.resource_manager = visa.ResourceManager()

        self.resources_tuple = self.mycomms.resource_manager.list_resources()
        self.my_instr = self.mycomms.instrument_object

        # ============================================================
        # Place VISA function utilities here
        # ============================================================
        self.echo_cmds = 0
        self.do_simulate = 1
        self.mycomms.simulate = 1

        self.is_connected = BooleanVar()
        self.is_connected.set(False)
        self.cbo_instr_variable = StringVar()
        self.instr_resource_string = StringVar()
        self.cbo_single_cmd_variable = StringVar()
        self.single_command_string = StringVar()
        self.seconds = StringVar()
        self.seconds.set("1")
        # variables for managing the radio buttons in the multi-command
        # exceution group
        self.var1 = IntVar()
        self.var1.set(1)
        self.my_text_var1 = StringVar()
        self.my_text_var1.set("Default")

        self.chk_a_val = IntVar()
        self.chk_a_val.set(1)

        self.cbo_baud_rate_variable = StringVar()
        self.cbo_parity_variable = StringVar()
        self.cbo_stop_bits_variable = StringVar()
        self.cbo_flow_ctrl_variable = StringVar()
        self.cbo_term_char_variable = StringVar()

        self.in_step_mode = IntVar()

        # Created a main frame (within the root GUI) on which to place
        # controls. This allows for adding padding to be added as needed
        # around the perimeter of the UI and provide a more appealing
        # appearance.
        self.main_frame = ttk.Frame(self.root,
                                    padding="5 5 5 5", 
                                    height=300, 
                                    width=600)
        # anchors to the root at the default position
        self.main_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.main_frame.columnconfigure(0, weight=1)

        # Create a group box (aka Labelframe) to hold the instrument detect,
        # select, connect/disconnect controls
        self.grp_instruments = ttk.Labelframe(self.main_frame,
                                              text='Instrument Select',
                                              pad=(5, 5, 5, 5),
                                              height=300,
                                              width=150)
        txtalt = self.cbo_instr_variable
        self.cbo_instruments = ttk.Combobox(self.grp_instruments,
                                            textvariable=txtalt,
                                            width=48)
        self.cbo_instruments.bind('<<ComboboxSelected>>',
                                  self.cbo_changed_instruments)
        self.cbo_instruments['values'] = self.resources_tuple
        # leave blank so that we can force the operator to select from 
        # available options
        self.cbo_instruments.current()

        cmdalt = self.button_connect_disconnect_press
        self.btn_connect = ttk.Button(self.grp_instruments,
                                      text="Connect",
                                      command=cmdalt,
                                      width=23)
        self.btn_refresh = ttk.Button(self.grp_instruments,
                                      text="Refresh",
                                      command=self.button_instruments_refresh)

        self.grp_sockets_utils = ttk.Labelframe(self.grp_instruments,
                                                text="Sockets")
        # lbl_enable_term = ttk.Label(grp_sockets_utils, text="Enable Term")
        self.chk_enable_term = ttk.Checkbutton(self.grp_sockets_utils,
                                               text="Enable Term Char",
                                               command=self.chk_a_action,
                                               variable=self.chk_a_val)

        self.grp_serial_utils = ttk.Labelframe(self.grp_instruments,
                                               text="RS-232")
        self.lbl_baud = ttk.Label(self.grp_serial_utils, text="Baud", width=10)
        self.cbo_baud = ttk.Combobox(self.grp_serial_utils,
                                     textvariable=self.cbo_baud_rate_variable,
                                     width=10)
        self.cbo_baud['values'] = ['9600', '115200']
        self.cbo_baud.current(0)

        self.lbl_parity = ttk.Label(self.grp_serial_utils,
                                    text="Parity",
                                    width=10)
        self.cbo_parity = ttk.Combobox(self.grp_serial_utils,
                                       textvariable=self.cbo_parity_variable,
                                       width=10)
        self.cbo_parity['values'] = ['None', 'Odd', 'Even']
        self.cbo_parity.current(0)

        self.lbl_stop_bits = ttk.Label(self.grp_serial_utils,
                                       text="Stop Bits",
                                       width=10)
        txtalt = self.cbo_stop_bits_variable
        self.cbo_stop_bits = ttk.Combobox(self.grp_serial_utils,
                                          textvariable=txtalt,
                                          width=10)
        self.cbo_stop_bits['values'] = ['0', '1', '2']
        self.cbo_stop_bits.current(1)

        self.lbl_flow_ctrl = ttk.Label(self.grp_serial_utils,
                                       text="Flow Ctrl",
                                       width=10)
        ctrlvar = self.cbo_flow_ctrl_variable
        self.cbo_flow_ctrl = ttk.Combobox(self.grp_serial_utils,
                                          textvariable=ctrlvar,
                                          width=10)
        self.cbo_flow_ctrl['values'] = ['None',
                                        'XON/XOFF',
                                        'RTS/CTS',
                                        'DTR/DSR']
        self.cbo_flow_ctrl.current(0)

        self.lbl_term_char = ttk.Label(self.grp_serial_utils,
                                       text="Term Char",
                                       width=10)
        txtalt = self.cbo_term_char_variable
        self.cbo_term_char = ttk.Combobox(self.grp_serial_utils,
                                          textvariable=txtalt,
                                          width=10)
        self.cbo_term_char['values'] = ['\\n', '\\r']
        self.cbo_term_char.current(0)

        # Create a group box (aka Labelframe) to hold the single command
        # operation tools....
        txtalt = "Single Command Operations"
        self.grp_single_command_ops = ttk.Labelframe(self.main_frame,
                                                     text=txtalt,
                                                     pad=(5, 5, 5, 5),
                                                     height=300,
                                                     width=200)
        txtalt = self.cbo_single_cmd_variable
        self.cbo_single_commands = ttk.Combobox(self.grp_single_command_ops,
                                                textvariable=txtalt,
                                                width=48)

        self.cbo_single_commands.bind('<<ComboboxSelected>>',
                                      self.cbo_single_command_changed)
        self.cbo_single_commands['values'] = ['*IDN?', '*RST', '*TRG']
        self.btn_cmd_write = ttk.Button(self.grp_single_command_ops,
                                        text="Write",
                                        command=self.button_write_press)
        self.btn_cmd_query = ttk.Button(self.grp_single_command_ops,
                                        text="Query",
                                        command=self.button_query_press)
        cmdalt = self.button_clear_list_press
        self.btn_clear_command_list = ttk.Button(self.grp_single_command_ops,
                                                 text="Clear List",
                                                 command=cmdalt)

        # Create a group box (aka Labelframe) to hold the multi command
        # operation tools....
        txtalt = "Multi-command Operations"
        self.grp_multi_command_ops = ttk.Labelframe(self.main_frame,
                                                    text=txtalt,
                                                    pad=(5, 5, 5, 5),
                                                    height=350,
                                                    width=350)
        self.txt_multi_command_text = Text(self.grp_multi_command_ops,
                                           height=15,
                                           width=40)
        self.s = ttk.Scrollbar(self.grp_multi_command_ops,
                               orient=VERTICAL,
                               command=self.txt_multi_command_text.yview)

        # reference the scrollbar action to the list box scroll command
        self.txt_multi_command_text['yscrollcommand'] = self.s.set
        cmdalt = self.button_send_commands_press
        self.btn_send_commands = ttk.Button(self.grp_multi_command_ops,
                                            text="Send\nCommands",
                                            command=cmdalt)
        cmdalt = self.button_clear_all_commands_press
        self.btn_clear_commands = ttk.Button(self.grp_multi_command_ops,
                                             text="Clear All\nCommands",
                                             command=cmdalt)
        cmdalt = self.button_save_commands_press
        self.btn_save_commands = ttk.Button(self.grp_multi_command_ops,
                                            text="Save\nCommands",
                                            command=cmdalt)
        cmdalt = self.button_load_commands_press
        self.btn_load_commands = ttk.Button(self.grp_multi_command_ops,
                                            text="Load\nCommands",
                                            command=cmdalt)
        txtalt = "Multi-command Execution Mode"
        self.grp_execution_mode = ttk.Labelframe(self.grp_multi_command_ops,
                                                 text=txtalt,
                                                 pad=(5, 5, 5, 5))
        self.btn_temp = ttk.Button(self.grp_execution_mode, text="temp")
        self.rdo_option_1 = ttk.Radiobutton(self.grp_execution_mode,
                                            text="Normal",
                                            pad=(5, 5, 5, 5),
                                            variable=self.var1,
                                            value=1,
                                            command=self.frame_a_rdo_click)
        self.rdo_option_2 = ttk.Radiobutton(self.grp_execution_mode,
                                            text="Timed",
                                            pad=(5, 5, 5, 5),
                                            variable=self.var1,
                                            value=2,
                                            command=self.frame_a_rdo_click)
        self.rdo_option_3 = ttk.Radiobutton(self.grp_execution_mode,
                                            text="Step",
                                            pad=(5, 5, 5, 5),
                                            variable=self.var1,
                                            value=3,
                                            command=self.frame_a_rdo_click)
        self.lbl_rdo1_buffer = ttk.Label(self.grp_execution_mode, text="",
                                         state='disabled',
                                         width=24)
        self.txt_timed_s = ttk.Entry(self.grp_execution_mode,
                                     textvariable=self.seconds,
                                     state='disabled',
                                     width=8)
        self.lbl_timed_s = ttk.Label(self.grp_execution_mode,
                                     text=" s",
                                     state='disabled',
                                     width=16)
        self.btn_stepper = ttk.Button(self.grp_execution_mode,
                                      text="Step",
                                      state='disabled',
                                      command=self.button_step_press)

        # add a text control where commands and responses can be dumped as the
        # user communicates with the instrument
        self.grp_command_logging_tools = ttk.Labelframe(self.main_frame,
                                                        text="Command Logging",
                                                        pad=(5, 5, 5, 5),
                                                        height=15,
                                                        width=250)
        self.txt_command_logger = Text(self.grp_command_logging_tools,
                                       height=10,
                                       width=75)
        self.s_cmd = ttk.Scrollbar(self.grp_command_logging_tools,
                                   orient=VERTICAL,
                                   command=self.txt_command_logger.yview)

        # reference the scrollbar action to the list box scroll command
        self.txt_command_logger['yscrollcommand'] = self.s_cmd.set
        self.clcftw_alt = self.clear_logging_commands_from_text_widget
        self.btn_clear_logging_commands =\
            ttk.Button(self.grp_command_logging_tools,
                       text="Clear Log\nCommands",
                       command=self.clcftw_alt)
        self.btn_save_logging_commands =\
            ttk.Button(self.grp_command_logging_tools,
                       text="Save Log\nCommands",
                       command=self.clcftw_alt)

        # grid up our controls on the main GUI....
        # instruments group controls
        self.grp_instruments.grid(column=0, row=0, sticky=(N, S, W, E))
        self.cbo_instruments.grid(column=0, row=0, columnspan=2, sticky=(W, E))
        self.btn_connect.grid(column=0, row=1, sticky=(W, E))
        self.btn_refresh.grid(column=1, row=1, sticky=(W, E))

        self.grp_sockets_utils.grid(column=0, row=2, sticky=(N, S, W, E))
        # lbl_enable_term.grid(column=0, row=0)
        self.chk_enable_term.grid(column=0, row=0)

        self.grp_serial_utils.grid(column=1, row=2, sticky=(N, S, W, E))
        self.lbl_baud.grid(column=0, row=0, sticky=W)
        self.lbl_parity.grid(column=0, row=1, sticky=W)
        self.lbl_stop_bits.grid(column=0, row=2, sticky=W)
        self.lbl_flow_ctrl.grid(column=0, row=3, sticky=W)
        self.lbl_term_char.grid(column=0, row=4, sticky=W)
        self.cbo_baud.grid(column=1, row=0, sticky=E)
        self.cbo_parity.grid(column=1, row=1, sticky=E)
        self.cbo_stop_bits.grid(column=1, row=2, sticky=E)
        self.cbo_flow_ctrl.grid(column=1, row=3, sticky=E)
        self.cbo_term_char.grid(column=1, row=4, sticky=E)

        self.cbo_changed_instruments()

        # next group single command controls on the main GUI....
        self.grp_single_command_ops.grid(column=0, row=1, sticky=(N, S, W, E))
        self.cbo_single_commands.grid(column=0, row=0, columnspan=3)
        self.btn_cmd_write.grid(column=0, row=1, sticky=(W, E))
        self.btn_cmd_query.grid(column=1, row=1, sticky=(W, E))
        self.btn_clear_command_list.grid(column=2, row=1, sticky=(W, E))

        # next multi-command controls group controls on the main GUI....
        self.grp_multi_command_ops.grid(column=1,
                                        row=0,
                                        rowspan=2,
                                        sticky=(N, S, W, E))
        self.txt_multi_command_text.grid(column=0,
                                         row=0,
                                         sticky=(N, S, W, E),
                                         rowspan=4)
        self.s.grid(column=1, row=0, sticky=(N, S), rowspan=4)
        self.btn_send_commands.grid(column=2, row=0, sticky=N)
        self.btn_clear_commands.grid(column=2, row=1, sticky=N)
        self.btn_save_commands.grid(column=2, row=2, sticky=N)
        self.btn_load_commands.grid(column=2, row=3, sticky=N)
        self.grp_execution_mode.grid(column=0,
                                     row=4,
                                     sticky=(W, E),
                                     columnspan=3)

        self.rdo_option_1.grid(column=0, row=0, sticky=(W, E))
        self.lbl_rdo1_buffer.grid(column=0, row=1)

        self.rdo_option_2.grid(column=1, row=0, sticky=(W, E))
        self.txt_timed_s.grid(column=1, row=1)
        self.lbl_timed_s.grid(column=2, row=1)

        self.rdo_option_3.grid(column=3, row=0, sticky=(W, E))
        self.btn_stepper.grid(column=3, row=1)

        # group the command logging tools on the main GUI....
        self.grp_command_logging_tools.grid(column=0,
                                            row=2,
                                            columnspan=2,
                                            sticky=(N, S, W, E))
        self.txt_command_logger.grid(column=0, row=0, rowspan=2,)
        self.s_cmd.grid(column=1, row=0, sticky=(N, S), rowspan=2)
        self.btn_clear_logging_commands.grid(column=2, row=0, sticky=(N, E))
        self.btn_save_logging_commands.grid(column=2, row=1, sticky=(N, E))

        # While the expected initial connected state will truly be false, we
        # set to True here then invoke the connect/disconnect function so that
        # it sets the state of the controls.
        self.is_connected.set(True)
        self.btn_connect.invoke()

    # ==========================================================================================
    # Place widget function utilities here
    # ==========================================================================================

    def cbo_changed_instruments(self):
        """
        Used to handle response to the change of the combo box listing.
        """
        self.instr_resource_string.set(self.cbo_instr_variable.get())

        if "ASRL" in self.instr_resource_string.get():
            for child2 in self.grp_serial_utils.winfo_children():
                if isinstance(child2, ttk.Button):
                    child2.config(state='enabled')
                elif isinstance(child2, ttk.Radiobutton):
                    child2.config(state='enabled')
                elif isinstance(child2, ttk.Entry):
                    child2.config(state='enabled')
                elif isinstance(child2, Text):
                    child2.config(state='normal')
                elif isinstance(child2, ttk.Combobox):
                    child2.config(state='enabled')
        else:
            for child2 in self.grp_serial_utils.winfo_children():
                if isinstance(child2, ttk.Button):
                    child2.config(state='disabled')
                elif isinstance(child2, ttk.Radiobutton):
                    child2.config(state='disabled')
                elif isinstance(child2, ttk.Entry):
                    child2.config(state='disabled')
                elif isinstance(child2, Text):
                    child2.config(state='disabled')
                elif isinstance(child2, ttk.Combobox):
                    child2.config(state='disabled')

        if "SOCKET" in self.instr_resource_string.get():
            for child in self.grp_sockets_utils.winfo_children():
                if isinstance(child, ttk.Button):
                    child.config(state='enabled')
                elif isinstance(child, ttk.Radiobutton):
                    child.config(state='enabled')
                elif isinstance(child, ttk.Entry):
                    child.config(state='enabled')
                elif isinstance(child, Text):
                    child.config(state='normal')
                elif isinstance(child, ttk.Combobox):
                    child.config(state='enabled')
                elif isinstance(child, ttk.Checkbutton):
                    child.config(state='enabled')
        else:
            for child in self.grp_sockets_utils.winfo_children():
                if isinstance(child, ttk.Button):
                    child.config(state='disabled')
                elif isinstance(child, ttk.Radiobutton):
                    child.config(state='disabled')
                elif isinstance(child, ttk.Entry):
                    child.config(state='disabled')
                elif isinstance(child, Text):
                    child.config(state='disabled')
                elif isinstance(child, ttk.Combobox):
                    child.config(state='disabled')
                elif isinstance(child, ttk.Checkbutton):
                    child.config(state='disabled')

    def cbo_single_command_changed(self):
        """
        Method to handle when the drop-down control for single command
        entry is changed by the operator.
        """
        self.single_command_string.set(self.cbo_single_cmd_variable.get())

    def frame_a_rdo_click(self):
        """
        This method handles modifying the state of other controls in
        response to the option the operator selects from the group of
        radio buttons provided.
        """
        if self.var1.get() == 1:
            self.my_text_var1.set("Option 1")
            # disable the time Entry and Label for timed and disable the step
            # button
            self.txt_timed_s.config(state='disabled')
            self.lbl_timed_s.config(state='disabled')
            self.btn_stepper.config(state='disabled')
        elif self.var1.get() == 2:
            self.my_text_var1.set("Option 2")
            # enable the Entry and Label for the timed and disable the step
            # button
            self.txt_timed_s.config(state='enabled')
            self.lbl_timed_s.config(state='enabled')
            self.btn_stepper.config(state='disabled')
        elif self.var1.get() == 3:
            self.my_text_var1.set("Option 3")
            # disable the Entry and Label for the timed and enable the step
            # button
            self.txt_timed_s.config(state='disabled')
            self.lbl_timed_s.config(state='disabled')
            self.btn_stepper.config(state='enabled')

    def button_connect_disconnect_press(self):
        """
        This method handles the response/state of a broad set of controls once
        the operator either connects or disconnects to an instrument resource.
        """
        instrsrc = self.instr_resource_string.get()
        bdrt = self.cbo_baud_rate_variable.get()
        if not self.is_connected.get():
            try:
                # Attempt to connect to the VISA resource
                if "ASRL" in self.instr_resource_string.get():
                    if "None" in self.cbo_parity_variable.get():
                        _parity = pyconst.Parity.none
                    elif "Odd" in self.cbo_parity_variable.get():
                        _parity = pyconst.Parity.odd
                    elif "Even" in self.cbo_parity_variable.get():
                        _parity = pyconst.Parity.even

                    if "1" in self.cbo_stop_bits_variable.get():
                        _stop = pyconst.StopBits.one
                    elif "2" in self.cbo_stop_bits_variable.get():
                        _stop = pyconst.StopBits.two
                    else:
                        _stop = pyconst.StopBits.one_and_a_half

                    if "None" in self.cbo_flow_ctrl_variable.get():
                        _flow = pyconst.ControlFlow.none
                    elif "RTS" in self.cbo_flow_ctrl_variable.get():
                        _flow = pyconst.ControlFlow.rts_cts
                    elif "XON" in self.cbo_flow_ctrl_variable.get():
                        _flow = pyconst.ControlFlow.xon_xoff
                    elif "DTR" in self.cbo_flow_ctrl_variable.get():
                        _flow = pyconst.ControlFlow.dtr_dsr

                    if "n" in self.cbo_term_char_variable.get():
                        _term = '\n'
                    else:
                        _term = '\r'

                    self.mycomms.instrument_connect(
                        instrument_resource_string=instrsrc,
                        timeout=20000,
                        do_id_query=1,
                        do_reset=0,
                        do_clear=0,
                        baud_rate=int(bdrt),
                        parity=_parity,
                        stop_bits=_stop,
                        flow_control=_flow,
                        read_terminator=_term
                        )
                else:
                    self.mycomms.instrument_connect(
                        instrument_resource_string=instrsrc,
                        timeout=20000,
                        do_id_query=1,
                        do_reset=0,
                        do_clear=0, )

                # A successful connection should change the state of the
                # connect button
                self.btn_connect.config(text="Disconnect")
                self.is_connected.set(True)

                for child in self.grp_single_command_ops.winfo_children():
                    child.config(state='enabled')
                for child2 in self.grp_multi_command_ops.winfo_children():
                    if isinstance(child2, ttk.Button):
                        child2.config(state='enabled')
                    elif isinstance(child2, ttk.Radiobutton):
                        child2.config(state='enabled')
                    elif isinstance(child2, ttk.Entry):
                        child2.config(state='enabled')
                    elif isinstance(child2, Text):
                        child2.config(state='normal')
                for child3 in self.grp_execution_mode.winfo_children():
                    if isinstance(child3, ttk.Button):
                        child3.config(state='enabled')
                    elif isinstance(child3, ttk.Radiobutton):
                        child3.config(state='enabled')
                    elif isinstance(child3, ttk.Entry):
                        child3.config(state='enabled')
                    elif isinstance(child3, Text):
                        child3.config(state='normal')
                self.var1.set(1)
                self.rdo_option_1.invoke()

            except visa.errors.VisaIOError:
                print("VISA error occurred")

        else:
            self.btn_connect.config(text="Connect")

            if self.mycomms.instrument_object is not None:
                self.mycomms.instrument_disconnect()

            self.is_connected.set(False)
            for child in self.grp_single_command_ops.winfo_children():
                child.config(state='disabled')
            for child2 in self.grp_multi_command_ops.winfo_children():
                if isinstance(child2, ttk.Button):
                    child2.config(state='disabled')
                elif isinstance(child2, ttk.Radiobutton):
                    child2.config(state='disabled')
                elif isinstance(child2, ttk.Entry):
                    child2.config(state='disabled')
                elif isinstance(child2, Text):
                    child2.config(state='disabled')
            for child3 in self.grp_execution_mode.winfo_children():
                if isinstance(child3, ttk.Button):
                    child3.config(state='disabled')
                elif isinstance(child3, ttk.Radiobutton):
                    child3.config(state='disabled')
                elif isinstance(child3, ttk.Entry):
                    child3.config(state='disabled')
                elif isinstance(child3, Text):
                    child3.config(state='disabled')

    def button_instruments_refresh(self):
        """
        This method handles the response to the click of the Refresh button,
        clearing the combo box text, polling the resource manager for all
        available instrument resources, then populating the combo options
        accordingly.
        """
        # Clear the Combobox text and, knowing it'll be clear invoke the combo
        # action to disable controls
        self.cbo_instruments.set("")
        self.cbo_changed_instruments()

        # scan for available resources then populate
        alt_resources_tuple = self.mycomms.resource_manager.list_resources()
        self.cbo_instruments['values'] = alt_resources_tuple
        return

    def chk_a_action(self):
        """
        This method handles the state of the check box associated with the
        sockets implementaion for the LAN options.
        """
        if self.chk_a_val.get() == 1:
            print(1)        # dud = 1   # commenting out until future use found
        else:
            print(2)        # dud = 2
        return

    def button_write_press(self):
        """
        This method is used in response to a user click on the 'Write' button
        in the UI, issuing the command of focus to the instrument resource.
        """
        # get the text from the combo box...
        self.single_command_string.set(self.cbo_single_cmd_variable.get())

        # then write the command to the instrument
        self.mycomms.instrument_write(self.single_command_string.get())

        # append the written command to the combo box list...
        self.cbo_single_commands['values'] = tuple(list(
            self.cbo_single_commands['values'])
            +
            [self.single_command_string.get()])

        # add the command(s) to the end of the logging Text widget
        self.txt_command_logger.insert(END,
                                       self.single_command_string.get() + "\n")

    def button_query_press(self):
        """
        This method is used in response to a user click on the 'Query' button
        in the UI, first writing the command of focus then immediately
        attempting to read back a response.
        """
        # get the text from the combo box...
        self.single_command_string.set(self.cbo_single_cmd_variable.get())

        # add the command(s) to the end of the logging Text widget
        self.txt_command_logger.insert(END,
                                       self.single_command_string.get() + "\n")

        # issue the query command to the instrument
        temp_qury_var = self.mycomms.instrument_query(
            self.single_command_string.get())

        # Add the output or return content to the end of the logging
        # Text widget
        self.txt_command_logger.insert(END, temp_qury_var + "\n")

        # append the written command to the combo box list...
        self.cbo_single_commands['values'] = tuple(list(
            self.cbo_single_commands['values'])
            +
            [self.single_command_string.get()])

    def button_clear_list_press(self):
        """
        This method handles the clearing of the single command
        """
        # remove all the contents of the combo box
        self.cbo_single_commands.delete(0, END)
        self.cbo_single_cmd_variable.set("")
        self.single_command_string.set(self.cbo_single_cmd_variable.get())
        # reinitialize with the starting values
        self.cbo_single_commands['values'] = ['*IDN?', '*RST', '*TRG']

    def button_send_commands_press(self):
        """
        This method handles the retreival of each command provided in the list
        control and placing them into a list that
        """
        # Read in all text from the Text control and split by line feed
        # character into a list then promotes the communications exchanges
        # based on the selection provided via the associated radio buttons.
        temp_container = self.txt_multi_command_text.get(1.0, END).split('\n')

        self.enable_disable_multi_cmd_buttons(False)

        # Issue the commands depending on the setting of the selected execution
        # mode
        if self.var1.get() == 1:
            # Do normal command at a time send
            self.sequential_iterative_send_commands(temp_container)
        elif self.var1.get() == 2:
            # Do timed command sending
            # Get the time from the Entry widget associated with the timed
            # radio option
            delay_time = float(self.seconds.get())
            self.sequential_iterative_send_commands(temp_container,
                                                    do_timed=1,
                                                    delay_s=delay_time)
        elif self.var1.get() == 3:
            # Do step-wise command sending
            self.step_wise_iterative_send_commands(temp_container)

        self.enable_disable_multi_cmd_buttons(True)

    def sequential_iterative_send_commands(self,
                                           command_list,
                                           do_timed=0,
                                           delay_s=1.0):
        """
        This method accepts a command list then loops over each index to issue
        either a write or query command, and returning data for the latter case
        """
        response = ""
        # Start with assuming the command is a write since this is the typical
        # majority
        is_query = False

        for i, cmd in enumerate(command_list):
            # add the command(s) to the end of the logging Text widget
            self.txt_command_logger.insert(END, cmd + "\n")
            # refresh at least the text widget so that commands are updated as
            # they are issued
            self.txt_command_logger.update_idletasks()
            if "?" in cmd:
                response = self.mycomms.instrument_query(cmd)
                is_query = True
            elif "print(" in cmd:
                response = self.mycomms.instrument_query(cmd)
                is_query = True
            elif "printbuffer(" in cmd:
                response = self.mycomms.instrument_query(cmd)
                is_query = True
            else:
                self.mycomms.instrument_write(cmd)

            if is_query:
                # Add the output or return content to the end of the logging
                # Text widget
                self.txt_command_logger.insert(END, response + "\n")
                is_query = False
                # refresh at least the text widget so that responses are
                # updated as they are received
                self.txt_command_logger.update_idletasks()

            # if set to include a delay time, implement a sleep time in seconds
            if do_timed == 1:
                time.sleep(delay_s)

    def button_step_press(self):
        """
        This method handles the stepping through the commands in the list.
        """
        # First click on the button should set a flag to note we're in step
        # mode so the Load Commands button can be altered accordingly.
        if self.in_step_mode.get() == 0:
            # set the flag
            self.in_step_mode.set(1)
            # disable other mulit-line command buttons....
            self.btn_send_commands.config(state='disabled')
            self.btn_clear_commands.config(state='disabled')
            self.btn_save_commands.config(state='disabled')

            # Change the text on the Load Commands button because I'm lazy and
            # don't want to add another button to the UI. Also, during the
            # stepping (or other) process this button shouldn't be used anyway.
            self.btn_load_commands.config(text="Stop\nStepping")

            # Fetch commands out of the multi-line text area and initially put
            # into a list for evaluation
            temp_container = self.txt_multi_command_text.get(1.0,
                                                             END).split('\n')

            # Determine start stop points of each command line which (ideally)
            # should be separated by the line feed character
            for i, cmd in enumerate(temp_container):
                print(cmd)

        else:
            # if commands have not already been fetched from the Text widget,
            # get them
            print("step")
            # how do we stop the stepping activity? - I have an idea
            # what do we do with the other buttons? is it okay to change the
            # Load Commands buttontext to "Stop Stepping"? - yes
            # Perhaps set a flag (or flags) to help control this.... yeah,
            # yeah, yeah

            # Will also want/need to track or break apart commands
            # Is there a way to highlight commands in the Text widget as the
            # user steps over them? See the link:
            # https://stackoverflow.com/questions/3781670/how-to-highlight-\
            # text-in-a-tkinter-text-widget#3781773 as well as
            # chapter 14 in Modern Tkinter for Busy Python Developers.

    def step_wise_iterative_send_commands(self, command_list):
        """
        This method handles stepping.
        """
        print(command_list)

    def enable_disable_multi_cmd_buttons(self, is_enabled):
        """
        This method handles enable/disable of controls
        """
        # as of 2021-05-30 - this is a "good intentions" section of code that,
        # while it seems to be coded properlyit does not do what it is supposed
        # to (disable and enable the target buttons)
        # state_string = 'enabled'  # CONSIDER DELETING IF NO FUTURE
        #   USE DETERMINED
        if not is_enabled:
            self.btn_send_commands.config(state='disabled')
            self.btn_clear_commands.config(state='disabled')
            self.btn_load_commands.config(state='disabled')
            self.btn_save_commands.config(state='disabled')
        else:
            self.btn_send_commands.config(state='enabled')
            self.btn_clear_commands.config(state='enabled')
            self.btn_load_commands.config(state='enabled')
            self.btn_save_commands.config(state='enabled')
        return

    def button_clear_all_commands_press(self):
        """
        This method handles removing commands from the list control.
        """
        self.txt_multi_command_text.delete(1.0, END)

    def button_save_commands_press(self):
        """
        This method provides a means for an operator to save the series
        of commands entered in the list control to file.
        """
        try:
            my_file = filedialog.asksaveasfile(mode='w',
                                               defaultextension='.txt',
                                               title="Save Commands",
                                               filetypes=[('TXT', '.txt'),
                                                          ('TSP', '.tsp'),
                                                          ('LUA', '*.lua'),
                                                          ('All Files', '*')])
            # ('TSP', '.tsp'),  ('Lua', '.lua'),

            if my_file is None:
                return
            data = self.txt_multi_command_text.get(1.0, END)
            my_file.write(data)
            my_file.close()
        except FileExistsError:
            messagebox._show(title="Error Saving File",
                             message="Unable to save file",
                             _icon='error',
                             _type='okcancel',
                             encoding='udf8')

    def button_load_commands_press(self):
        """
        This method is used by the operator to recall a file from disk
        and populate its contents into the list box control.
        """
        if self.in_step_mode.get() == 0:
            try:
                # have the user navigate to and select their file....
                my_file = filedialog.askopenfile(defaultextension='.txt',
                                                 title="Save Commands",
                                                 filetypes=[('TXT', '.txt'),
                                                            ('TSP', '.tsp'),
                                                            ('LUA', '.lua'),
                                                            ('All Files', '*')
                                                            ])
                if my_file is None:
                    return

                # read the contents of the file into a temporary variable
                with open(my_file.name, encoding='utf-8') as f:
                    contents = f.read()
                    f.close()

                # populate our TextBox control with the file contents
                self.txt_multi_command_text.insert(1.0, contents)

            except FileNotFoundError:
                # tkMessageBox.showerror('Error Saving Grammar', 'Unable to 
                # open file: %r' % filename)
                messagebox._show(title="Error Loading File",
                                 message="Unable to load file",
                                 _icon='error',
                                 _type='okcancel')
        else:
            print("I'm a sexy stepper")
            # Getting here means that the button text reads "Stop Stepping",
            # so we need to revert to "Load Commands"
            self.btn_load_commands.config(text="Load\nCommands")

            # And we want the environment to know we're no longer doing
            # step-mode stuff....
            self.in_step_mode.set(0)
            # enable mult-line command buttons
            # disable other mulit-line command buttons....
            self.btn_send_commands.config(state='normal')
            self.btn_clear_commands.config(state='normal')
            self.btn_save_commands.config(state='normal')

            # clean up for any other flags...

    def clear_logging_commands_from_text_widget(self):
        """
        Method to clear logging commands from the text widget.
        """
        self.txt_command_logger.delete(1.0, END)

    def save_logging_commands_from_text_widget(self):
        """
        Method to save logging commands.
        """
        try:
            my_file = filedialog.asksaveasfile(mode='w',
                                               defaultextension='.txt',
                                               title="Save Commands",
                                               filetypes=[('TXT', '.txt'),
                                                          ('All Files', '*')])
            # ('TSP', '.tsp'), ('Lua', '.lua'),

            if my_file is None:
                return
            data = self.txt_command_logger.get(1.0, END)
            my_file.write(data)
            my_file.close()
        except FileExistsError:
            # tkMessageBox.showerror('Error Saving Grammar', 
            # 'Unable to open file: %r' % filename)
            messagebox._show(title="Error Saving File",
                             message="Unable to save file",
                             _icon='error',
                             _type='okcancel',
                             encoding='utf8')

    def launch(self):
        """
        Stuff
        """
        self.root.mainloop()


rplt = InstrumentConfigurationTools()
rplt.launch()
