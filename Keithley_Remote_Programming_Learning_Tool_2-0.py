from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

import pyvisa as visa
import pyvisa.constants as pyconst

import time

import VISA_Communictions_Tools as comms

# CONSIDER ADDING TOOLTIPS WITH THE CLASS FOUND HERE: https://code.activestate.com/recipes/576688-tooltip-for-tkinter/

mycomms = comms.VisaCommunications()
if mycomms.resource_manager == None:
    mycomms.resource_manager = visa.ResourceManager()

resources_tuple = mycomms.resource_manager.list_resources()
my_instr = mycomms.instrument_object

# ==========================================================================================
# Place VISA function utilities here
# ==========================================================================================
echo_commands = 0
do_simulate = 0


# ==========================================================================================
# Place widget function utilities here
# ==========================================================================================

def cbo_changed_instruments(*args):
    instr_resource_string.set(cbo_instr_variable.get())

    if "ASRL" in instr_resource_string.get():
        for child2 in grp_serial_utils.winfo_children():
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
        for child2 in grp_serial_utils.winfo_children():
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

    if "SOCKET" in instr_resource_string.get():
        for child in grp_sockets_utils.winfo_children():
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
        for child in grp_sockets_utils.winfo_children():
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
    return


def cbo_single_command_changed(*args):
    single_command_string.set(cbo_single_cmd_variable.get())
    return


def frame_a_rdo_click(*args):
    if var1.get() == 1:
        my_text_var1.set("Option 1")
        # disable the time Entry and Label for timed and disable the step button
        txt_timed_s.config(state='disabled')
        lbl_timed_s.config(state='disabled')
        btn_stepper.config(state='disabled')
    elif var1.get() == 2:
        my_text_var1.set("Option 2")
        # enable the Entry and Label for the timed and disable the step button
        txt_timed_s.config(state='enabled')
        lbl_timed_s.config(state='enabled')
        btn_stepper.config(state='disabled')
    elif var1.get() == 3:
        my_text_var1.set("Option 3")
        # disable the Entry and Label for the timed and enable the step button
        txt_timed_s.config(state='disabled')
        lbl_timed_s.config(state='disabled')
        btn_stepper.config(state='enabled')
    return


def button_connect_disconnect_press(*args):
    if not is_connected.get():
        try:
            # Attempt to connect to the VISA resource
            if "ASRL" in instr_resource_string.get():
                if "None" in cbo_parity_variable.get():
                    _parity = pyconst.Parity.none
                elif "Odd" in cbo_parity_variable.get():
                    _parity = pyconst.Parity.odd
                elif "Even" in cbo_parity_variable.get():
                    _parity = pyconst.Parity.even

                if "1" in cbo_stop_bits_variable.get():
                    _stop = pyconst.StopBits.one
                elif "2" in cbo_stop_bits_variable.get():
                    _stop = pyconst.StopBits.two
                else:
                    _stop = pyconst.StopBits.none

                if "None" in cbo_flow_ctrl_variable.get():
                    _flow = pyconst.ControlFlow.none
                elif "RTS" in cbo_flow_ctrl_variable.get():
                    _flow = pyconst.ControlFlow.rts
                elif "XON" in cbo_flow_ctrl_variable.get():
                    _flow = pyconst.ControlFlow.xon

                if "n" in cbo_term_char_variable.get():
                    _term = '\n'
                else:
                    _term = '\r'

                mycomms.instrument_connect(instrument_resource_string=instr_resource_string.get(),
                                           timeout=20000,
                                           do_id_query=1,
                                           do_reset=0,
                                           do_clear=0,
                                           baud_rate=int(cbo_baud_rate_variable.get()),
                                           parity=_parity,
                                           stop_bits=_stop,
                                           flow_control=_flow,
                                           read_terminator=_term
                                           )
            else:
                mycomms.instrument_connect(instrument_resource_string=instr_resource_string.get(),
                                           timeout=20000,
                                           do_id_query=1,
                                           do_reset=0,
                                           do_clear=0, )

            # A successful connection should change the state of the connect button
            btn_connect.config(text="Disconnect")
            is_connected.set(True)

            for child in grp_single_command_ops.winfo_children():
                child.config(state='enabled')
            for child2 in grp_multi_command_ops.winfo_children():
                if isinstance(child2, ttk.Button):
                    child2.config(state='enabled')
                elif isinstance(child2, ttk.Radiobutton):
                    child2.config(state='enabled')
                elif isinstance(child2, ttk.Entry):
                    child2.config(state='enabled')
                elif isinstance(child2, Text):
                    child2.config(state='normal')
            for child3 in grp_execution_mode.winfo_children():
                if isinstance(child3, ttk.Button):
                    child3.config(state='enabled')
                elif isinstance(child3, ttk.Radiobutton):
                    child3.config(state='enabled')
                elif isinstance(child3, ttk.Entry):
                    child3.config(state='enabled')
                elif isinstance(child3, Text):
                    child3.config(state='normal')
            var1.set(1)
            rdo_option_1.invoke()

        except visa.errors.VisaIOError:
            print("VISA error occurred")

    else:
        btn_connect.config(text="Connect")

        if mycomms.instrument_object is not None:
            mycomms.instrument_disconnect()

        is_connected.set(False)
        for child in grp_single_command_ops.winfo_children():
            child.config(state='disabled')
        for child2 in grp_multi_command_ops.winfo_children():
            if isinstance(child2, ttk.Button):
                child2.config(state='disabled')
            elif isinstance(child2, ttk.Radiobutton):
                child2.config(state='disabled')
            elif isinstance(child2, ttk.Entry):
                child2.config(state='disabled')
            elif isinstance(child2, Text):
                child2.config(state='disabled')
        for child3 in grp_execution_mode.winfo_children():
            if isinstance(child3, ttk.Button):
                child3.config(state='disabled')
            elif isinstance(child3, ttk.Radiobutton):
                child3.config(state='disabled')
            elif isinstance(child3, ttk.Entry):
                child3.config(state='disabled')
            elif isinstance(child3, Text):
                child3.config(state='disabled')


    return


def button_instruments_refresh(*args):
    # Clear the Combobox text and, knowing it'll be clear invoke the combo action to disable controls
    cbo_instruments.set("")
    cbo_changed_instruments()

    # scan for available resources then populate
    alt_resources_tuple = mycomms.resource_manager.list_resources()
    cbo_instruments['values'] = alt_resources_tuple
    return


def chk_a_action(*args):
    if chk_a_val.get() == 1:
        dud = 1
    else:
        dud = 2
    return


def button_write_press(*args):
    # get the text from the combo box...
    single_command_string.set(cbo_single_cmd_variable.get())

    # then write the command to the instrument
    mycomms.instrument_write(single_command_string.get())

    # append the written command to the combo box list...
    cbo_single_commands['values'] = tuple(list(cbo_single_commands['values']) + [single_command_string.get()])

    # add the command(s) to the end of the logging Text widget
    txt_command_logger.insert(END, single_command_string.get() + "\n")
    return


def button_query_press(*args):
    # get the text from the combo box...
    single_command_string.set(cbo_single_cmd_variable.get())

    # add the command(s) to the end of the logging Text widget
    txt_command_logger.insert(END, single_command_string.get() + "\n")

    # issue the query command to the instrument
    temp_qury_var = mycomms.instrument_query(single_command_string.get())

    # Add the output or return content to the end of the logging Text widget
    txt_command_logger.insert(END, temp_qury_var + "\n")

    # append the written command to the combo box list...
    cbo_single_commands['values'] = tuple(list(cbo_single_commands['values']) + [single_command_string.get()])
    return


def button_clear_list_press(*args):
    # remove all the contents of the combo box
    cbo_single_commands.delete(0, END)
    cbo_single_cmd_variable.set("")
    single_command_string.set(cbo_single_cmd_variable.get())
    # reinitialize with the starting values
    cbo_single_commands['values'] = ['*IDN?', '*RST', '*TRG']

    return

def button_send_commands_press(*args):
    # Read in all text from the Text control and split by line feed character into a list
    temp_container = txt_multi_command_text.get(1.0, END).split('\n')

    enable_disable_multi_cmd_buttons(False)

    # Issue the commands depending on the setting of the selected execution mode
    if var1.get() == 1:
        # Do normal command at a time send
        sequential_iterative_send_commands(temp_container)
    elif var1.get() == 2:
        # Do timed command sending
        # Get the time from the Entry widget associated with the timed radio option
        delay_time = float(seconds.get())
        sequential_iterative_send_commands(temp_container, do_timed=1, delay_s=delay_time)
    elif var1.get() == 3:
        # Do step-wise command sending
        step_wise_iterative_send_commands(temp_container)

    enable_disable_multi_cmd_buttons(True)

    return


def sequential_iterative_send_commands(command_list, do_timed=0, delay_s=1.0):
    response = ""
    is_query = False     # start with assuming the command is a write since this is the typical majority
    for i, cmd in enumerate(command_list):
        # add the command(s) to the end of the logging Text widget
        txt_command_logger.insert(END, cmd + "\n")
        # refresh at least the text widget so that commands are updated as they are issued
        txt_command_logger.update_idletasks()
        if "?" in cmd:
            response = mycomms.instrument_query(cmd)
            is_query = True
        elif "print(" in cmd:
            response = mycomms.instrument_query(cmd)
            is_query = True
        elif "printbuffer(" in cmd:
            response = mycomms.instrument_query(cmd)
            is_query = True
        else:
            mycomms.instrument_write(cmd)

        if is_query:
            # Add the output or return content to the end of the logging Text widget
            txt_command_logger.insert(END, response + "\n")
            is_query = False
            # refresh at least the text widget so that responses are updated as they are received
            txt_command_logger.update_idletasks()

        # if set to include a delay time, implement a sleep time in seconds
        if do_timed == 1:
            time.sleep(delay_s)
    return


def button_step_press(*args):
    # if commands have not already been fetched from the Text widget, get them
    print("step")
    # how do we stop the stepping activity?
    # what do we do with the other buttons? is it okay to change the Load Commands button text to "Stop Stepping"?
    # Perhaps set a flag (or flags) to help control this
    # Will also want/need to track or break apart commands
    # Is there a way to highlight commands in the Text widget as the user steps over them? See the link
    # https://stackoverflow.com/questions/3781670/how-to-highlight-text-in-a-tkinter-text-widget#3781773 as well as
    # chapter 14 in Modern Tkinter for Busy Python Developers.
    return

def step_wise_iterative_send_commands(command_list):
    return


def enable_disable_multi_cmd_buttons(is_enabled):
    # as of 2021-05-30 - this is a "good intentions" section of code that, while it seems to be coded properly
    # it does not do what it is supposed to (disable and enable the target buttons)
    state_string = 'enabled'
    if not is_enabled:
        btn_send_commands.config(state='disabled')
        btn_clear_commands.config(state='disabled')
        btn_load_commands.config(state='disabled')
        btn_save_commands.config(state='disabled')
    else:
        btn_send_commands.config(state='enabled')
        btn_clear_commands.config(state='enabled')
        btn_load_commands.config(state='enabled')
        btn_save_commands.config(state='enabled')
    return


def button_clear_all_commands_press(*args):
    txt_multi_command_text.delete(1.0, END)
    return


def button_save_commands_press(*args):
    try:
        myFile = filedialog.asksaveasfile(mode='w',
                                          defaultextension='.txt',
                                          title="Save Commands",
                                          filetypes=[('TXT', '.txt'), ('TSP', '.tsp'), ('All Files', '*')])  # ('TSP', '.tsp'), ('Lua', '.lua'),

        if myFile is None:
            return
        data = txt_multi_command_text.get(1.0, END)
        myFile.write(data)
        myFile.close()
    except Exception:
            messagebox._show(title="Error Saving File", message="Unable to save file", _icon='error', _type='okcancel', encoding='udf8')
    return


def button_load_commands_press(*args):
    try:
        # have the user navigate to and select their file....
        myFile = filedialog.askopenfile(defaultextension='.txt',
                                        title="Save Commands",
                                        filetypes=[('TXT', '.txt'), ('TSP', '.tsp'), ('All Files', '*')])
        if myFile is None:
            return

        # read the contents of the file into a temporary variable
        with open(myFile.name) as f:
            contents = f.read()
            f.close()

        # populate our TextBox control with the file contents
        txt_multi_command_text.insert(1.0, contents)

    except Exception:
        # tkMessageBox.showerror('Error Saving Grammar', 'Unable to open file: %r' % filename)
        messagebox._show(title="Error Loading File", message="Unable to load file", _icon='error', _type='okcancel')
    return


def clear_logging_commands_from_text_widget(*args):
    txt_command_logger.delete(1.0, END)
    return


def save_logging_commands_from_text_widget(*args):
    try:
        myFile = filedialog.asksaveasfile(mode='w',
                                          defaultextension='.txt',
                                          title="Save Commands",
                                          filetypes=[('TXT', '.txt'), ('All Files', '*')])  # ('TSP', '.tsp'), ('Lua', '.lua'),

        if myFile is None:
            return
        data = txt_command_logger.get(1.0, END)
        myFile.write(data)
        myFile.close()
    except Exception:
            #tkMessageBox.showerror('Error Saving Grammar', 'Unable to open file: %r' % filename)
            messagebox._show(title="Error Saving File", message="Unable to save file", _icon='error', _type='okcancel', encoding='udf8')
    return


# ==========================================================================================
# Place our main UI definition here
# ==========================================================================================

root = Tk()
root.title("Keithley Remote Programming Learning Tool 2.0")
root.columnconfigure(0, weight=1)   # helps with frame/app resizing on the fly
root.rowconfigure(0, weight=1)      # helps with frame/app resizing on the fly
# We define a geometry instead of independent height and width because the tkinter
# base behavior of widgets appears to override the intended behavior, meaning our
# sizes appear to get ignored after the widgets are gridded up.
root.geometry("778x555")


is_connected = BooleanVar()
is_connected.set(False)
cbo_instr_variable = StringVar()
instr_resource_string = StringVar()
cbo_single_cmd_variable = StringVar()
single_command_string = StringVar()
seconds = StringVar()
seconds.set("1")
# variables for managing the radio buttons in the multi-command exceution group
var1 = IntVar()
var1.set(1)
my_text_var1 = StringVar()
my_text_var1.set("Default")

chk_a_val = IntVar()
chk_a_val.set(1)

cbo_baud_rate_variable = StringVar()
cbo_parity_variable = StringVar()
cbo_stop_bits_variable = StringVar()
cbo_flow_ctrl_variable = StringVar()
cbo_term_char_variable = StringVar()


# Created a main frame (within the root GUI) on which to place controls. This allows for adding padding
# to be added as needed around the perimeter of the UI and provide a more appealing appearance.
main_frame = ttk.Frame(root, padding="5 5 5 5", height=300, width=600)
main_frame.grid(column=0, row=0, sticky=(N, W, E, S))    # anchors to the root at the default position
main_frame.columnconfigure(0, weight=1)


# Create a group box (aka Labelframe) to hold the instrument detect, select, connect/disconnect controls
grp_instruments = ttk.Labelframe(main_frame, text='Instrument Select', pad=(5, 5, 5, 5), height=300, width=150)

cbo_instruments = ttk.Combobox(grp_instruments, textvariable=cbo_instr_variable, width=48)
cbo_instruments.bind('<<ComboboxSelected>>', cbo_changed_instruments)
cbo_instruments['values'] = resources_tuple
cbo_instruments.current()   # leave blank so that we can force the operator to select from available options

btn_connect = ttk.Button(grp_instruments, text="Connect", command=button_connect_disconnect_press, width=23)
btn_refresh = ttk.Button(grp_instruments, text="Refresh", command=button_instruments_refresh)

grp_sockets_utils = ttk.Labelframe(grp_instruments, text="Sockets")
# lbl_enable_term = ttk.Label(grp_sockets_utils, text="Enable Term")
chk_enable_term = ttk.Checkbutton(grp_sockets_utils, text="Enable Term Char", command=chk_a_action, variable=chk_a_val)

grp_serial_utils = ttk.Labelframe(grp_instruments, text="RS-232")
lbl_baud = ttk.Label(grp_serial_utils, text="Baud", width=10)
cbo_baud = ttk.Combobox(grp_serial_utils, textvariable=cbo_baud_rate_variable, width=10)
cbo_baud['values'] = ['9600', '115200']
cbo_baud.current(0)

lbl_parity = ttk.Label(grp_serial_utils, text="Parity", width=10)
cbo_parity = ttk.Combobox(grp_serial_utils, textvariable=cbo_parity_variable, width=10)
cbo_parity['values'] = ['None', 'Odd', 'Even']
cbo_parity.current(0)

lbl_stop_bits = ttk.Label(grp_serial_utils, text="Stop Bits", width=10)
cbo_stop_bits = ttk.Combobox(grp_serial_utils, textvariable=cbo_stop_bits_variable, width=10)
cbo_stop_bits['values'] = ['0', '1', '2']
cbo_stop_bits.current(1)

lbl_flow_ctrl = ttk.Label(grp_serial_utils, text="Flow Ctrl", width=10)
cbo_flow_ctrl = ttk.Combobox(grp_serial_utils, textvariable=cbo_flow_ctrl_variable, width=10)
cbo_flow_ctrl['values'] = ['None', 'XON/XOFF', 'RTS/CTS']
cbo_flow_ctrl.current(0)

lbl_term_char = ttk.Label(grp_serial_utils, text="Term Char", width=10)
cbo_term_char = ttk.Combobox(grp_serial_utils, textvariable=cbo_term_char_variable, width=10)
cbo_term_char['values'] = ['\\n', '\\r']
cbo_term_char.current(0)

# Create a group box (aka Labelframe) to hold the single command operation tools....
grp_single_command_ops = ttk.Labelframe(main_frame,
                                        text="Single Command Operations",
                                        pad=(5, 5, 5, 5),
                                        height=300,
                                        width=200)
cbo_single_commands = ttk.Combobox(grp_single_command_ops,
                                   textvariable=cbo_single_cmd_variable,
                                   width=48)

cbo_single_commands.bind('<<ComboboxSelected>>', cbo_single_command_changed)
cbo_single_commands['values'] = ['*IDN?', '*RST', '*TRG']
btn_cmd_write = ttk.Button(grp_single_command_ops, text="Write", command=button_write_press)
btn_cmd_query = ttk.Button(grp_single_command_ops, text="Query", command=button_query_press)
btn_clear_command_list = ttk.Button(grp_single_command_ops, text="Clear List", command=button_clear_list_press)


# Create a group box (aka Labelframe) to hold the multi command operation tools....
grp_multi_command_ops = ttk.Labelframe(main_frame,
                                       text="Multi-command Operations",
                                       pad=(5, 5, 5, 5),
                                       height=350,
                                       width=350)
txt_multi_command_text = Text(grp_multi_command_ops, height=15, width=40)
s = ttk.Scrollbar(grp_multi_command_ops, orient=VERTICAL, command=txt_multi_command_text.yview)

txt_multi_command_text['yscrollcommand'] = s.set         # reference the scrollbar action to the list box scroll command
btn_send_commands = ttk.Button(grp_multi_command_ops, text="Send\nCommands", command=button_send_commands_press)
btn_clear_commands = ttk.Button(grp_multi_command_ops, text="Clear All\nCommands", command=button_clear_all_commands_press)
btn_save_commands = ttk.Button(grp_multi_command_ops, text="Save\nCommands", command=button_save_commands_press)
btn_load_commands = ttk.Button(grp_multi_command_ops, text="Load\nCommands", command=button_load_commands_press)
grp_execution_mode = ttk.Labelframe(grp_multi_command_ops, text="Multi-command Execution Mode", pad=(5, 5, 5, 5))
btn_temp = ttk.Button(grp_execution_mode, text="temp")
rdo_option_1 = ttk.Radiobutton(grp_execution_mode,
                               text="Normal",
                               pad=(5, 5, 5, 5),
                               variable=var1,
                               value=1,
                               command=frame_a_rdo_click)
rdo_option_2 = ttk.Radiobutton(grp_execution_mode,
                               text="Timed",
                               pad=(5, 5, 5, 5),
                               variable=var1,
                               value=2,
                               command=frame_a_rdo_click)
rdo_option_3 = ttk.Radiobutton(grp_execution_mode,
                               text="Step",
                               pad=(5, 5, 5, 5),
                               variable=var1,
                               value=3,
                               command=frame_a_rdo_click)
lbl_rdo1_buffer = ttk.Label(grp_execution_mode, text="", state='disabled', width=24)
txt_timed_s = ttk.Entry(grp_execution_mode, textvariable=seconds, state='disabled', width=8)
lbl_timed_s = ttk.Label(grp_execution_mode, text=" s", state='disabled', width=16)
btn_stepper = ttk.Button(grp_execution_mode, text="Step", state='disabled', command=button_step_press)

# add a text control where commands and responses can be dumped as the user communicates with the instrument
grp_command_logging_tools = ttk.Labelframe(main_frame,
                                           text="Command Logging",
                                           pad=(5, 5, 5, 5),
                                           height=15,
                                           width=250)
txt_command_logger = Text(grp_command_logging_tools, height=10, width=75)
s_cmd = ttk.Scrollbar(grp_command_logging_tools, orient=VERTICAL, command=txt_command_logger.yview)

txt_command_logger['yscrollcommand'] = s_cmd.set         # reference the scrollbar action to the list box scroll command
btn_clear_logging_commands = ttk.Button(grp_command_logging_tools, text="Clear Log\nCommands", command=clear_logging_commands_from_text_widget)
btn_save_logging_commands = ttk.Button(grp_command_logging_tools, text="Save Log\nCommands", command=save_logging_commands_from_text_widget)

# grid up our controls on the main GUI....
# instruments group controls
grp_instruments.grid(column=0, row=0, sticky=(N, S, W, E))
cbo_instruments.grid(column=0, row=0, columnspan=2, sticky=(W, E))
btn_connect.grid(column=0, row=1, sticky=(W, E))
btn_refresh.grid(column=1, row=1, sticky=(W, E))

grp_sockets_utils.grid(column=0, row=2, sticky=(N, S, W, E))
# lbl_enable_term.grid(column=0, row=0)
chk_enable_term.grid(column=0, row=0)

grp_serial_utils.grid(column=1, row=2, sticky=(N, S, W, E))
lbl_baud.grid(column=0, row=0, sticky=W)
lbl_parity.grid(column=0, row=1, sticky=W)
lbl_stop_bits.grid(column=0, row=2, sticky=W)
lbl_flow_ctrl.grid(column=0, row=3, sticky=W)
lbl_term_char.grid(column=0, row=4, sticky=W)
cbo_baud.grid(column=1, row=0, sticky=E)
cbo_parity.grid(column=1, row=1, sticky=E)
cbo_stop_bits.grid(column=1, row=2, sticky=E)
cbo_flow_ctrl.grid(column=1, row=3, sticky=E)
cbo_term_char.grid(column=1, row=4, sticky=E)

cbo_changed_instruments()

# next group single command controls on the main GUI....
grp_single_command_ops.grid(column=0, row=1, sticky=(N, S, W, E))
cbo_single_commands.grid(column=0, row=0, columnspan=3)
btn_cmd_write.grid(column=0, row=1, sticky=(W, E))
btn_cmd_query.grid(column=1, row=1, sticky=(W, E))
btn_clear_command_list.grid(column=2, row=1, sticky=(W, E))

# next multi-command controls group controls on the main GUI....
grp_multi_command_ops.grid(column=1, row=0, rowspan=2, sticky=(N, S, W, E))
txt_multi_command_text.grid(column=0, row=0, sticky=(N, S, W, E), rowspan=4)
s.grid(column=1, row=0, sticky=(N, S), rowspan=4)
btn_send_commands.grid(column=2, row=0, sticky=N)
btn_clear_commands.grid(column=2, row=1, sticky=N)
btn_save_commands.grid(column=2, row=2, sticky=N)
btn_load_commands.grid(column=2, row=3, sticky=N)
grp_execution_mode.grid(column=0, row=4, sticky=(W, E), columnspan=3)

rdo_option_1.grid(column=0, row=0, sticky=(W, E))
lbl_rdo1_buffer.grid(column=0, row=1)

rdo_option_2.grid(column=1, row=0, sticky=(W, E))
txt_timed_s.grid(column=1, row=1)
lbl_timed_s.grid(column=2, row=1)

rdo_option_3.grid(column=3, row=0, sticky=(W, E))
btn_stepper.grid(column=3, row=1)

# group the command logging tools on the main GUI....
grp_command_logging_tools.grid(column=0, row=2, columnspan=2, sticky=(N, S, W, E))
txt_command_logger.grid(column=0, row=0, rowspan=2,)
s_cmd.grid(column=1, row=0, sticky=(N, S), rowspan=2)
btn_clear_logging_commands.grid(column=2, row=0, sticky=(N, E))
btn_save_logging_commands.grid(column=2, row=1, sticky=(N, E))

# While the expected initial connected state will truly be false, we set to True here
# then invoke the connect/disconnect function so that it sets the state of the controls.
is_connected.set(True)
btn_connect.invoke()

root.mainloop()
