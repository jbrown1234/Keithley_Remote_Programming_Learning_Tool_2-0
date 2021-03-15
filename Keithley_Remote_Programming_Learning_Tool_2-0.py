from tkinter import *
from tkinter import ttk
import pyvisa as visa
rm = visa.ResourceManager()
resources_tuple = rm.list_resources()
# change
# Place function utilities here


def cbo_changed(*args):
    instrument_resource_string.set(cbo_instr_variable.get())

    return


def cbo_single_command_changed(*args):
    instrument_resource_string.set(cbo_single_cmd_variable.get())

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
    else:
        btn_connect.config(text="Connect")
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
    resources_tuple = rm.list_resources()
    cbo_instruments['values'] = resources_tuple
    return


# Place our main UI definition here
root = Tk()
root.title("Keithley Remote Programming Learning Tool 2.0")
#root['width'] = 600
#root['height'] = 300
root.columnconfigure(0, weight=1)   # helps with frame/app resizing on the fly
root.rowconfigure(0, weight=1)      # helps with frame/app resizing on the fly
root.geometry("778x400")    # We define a geometry instead of independent height and width because the tkinter
                            # base behavior of widgets appears to override the intended behavior, meaning our
                            # sizes appear to get ignored after the widgets are gridded up.


is_connected = BooleanVar()
is_connected.set(False)
cbo_instr_variable = StringVar()
instrument_resource_string = StringVar()
cbo_single_cmd_variable = StringVar()
seconds = StringVar()
seconds.set("1")
# variables for managing the radio buttons in the multi-command exceution group
var1 = IntVar()
var1.set(1)
my_text_var1 = StringVar()
my_text_var1.set("Default")

# Created a main frame (within the root GUI) on which to place controls. This allows for adding padding
# to be added as needed around the perimeter of the UI and provide a more appealing appearance.
main_frame = ttk.Frame(root, padding="5 5 5 5", height=300, width=600)
#main_frame.pack()  # had this in the original code, but does not appear it is needed.
main_frame.grid(column=0, row=0, sticky=(N, W, E, S))    # anchors to the root at the default position
main_frame.columnconfigure(0, weight=1)
#main_frame.columnconfigure(1, weight=2)


# Create a group box (aka Labelframe) to hold the instrument detect, select, connect/disconnect controls
grp_instruments = ttk.Labelframe(main_frame, text='Instrument Select', pad=(5, 5, 5, 5), height=300, width=150)
cbo_instruments = ttk.Combobox(grp_instruments, textvariable=cbo_instr_variable, width=48) # .grid(column=1, row=1) # PROBLEM.... see note below

cbo_instruments.bind('<<ComboboxSelected>>', cbo_changed)
cbo_instruments['values'] = resources_tuple   # the book showed how
                                                                                                # values were added with
                                                                                                # a tuple, but we can
                                                                                                # also use a list
#cbo_instruments.grid(column=1, row=1)   # NOTE - if I put the grid assignment in the same line with the combo box definition
                                        # I get an error in assigning values to the combo box in a follow-up statement;
                                        # seems to throw the scope for a loop.
cbo_instruments.current()

btn_connect = ttk.Button(grp_instruments, text="Connect", command=button_connect_disconnect_press)
btn_refresh = ttk.Button(grp_instruments, text="Refresh", command=button_instruments_refresh)


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
btn_cmd_write = ttk.Button(grp_single_command_ops, text="Write")
btn_cmd_query = ttk.Button(grp_single_command_ops, text="Query")
btn_clear_command_list = ttk.Button(grp_single_command_ops, text="Clear List")


# Create a group box (aka Labelframe) to hold the multi command operation tools....
grp_multi_command_ops = ttk.Labelframe(main_frame,
                                       text="Multi-command Operations",
                                       pad=(5, 5, 5, 5),
                                       height=350,
                                       width=350)
txt_multi_command_text = Text(grp_multi_command_ops, height=15, width=40)
s = ttk.Scrollbar(grp_multi_command_ops, orient=VERTICAL, command=txt_multi_command_text.yview)

txt_multi_command_text['yscrollcommand'] = s.set         # reference the scrollbar action to the list box scroll command
btn_send_commands = ttk.Button(grp_multi_command_ops, text="Send\nCommands")
btn_clear_commands = ttk.Button(grp_multi_command_ops, text="Clear All\nCommands")
btn_save_commands = ttk.Button(grp_multi_command_ops, text="Save\nCommands")
btn_load_commands = ttk.Button(grp_multi_command_ops, text="Load\nCommands")
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
btn_stepper = ttk.Button(grp_execution_mode, text="Step", state='disabled')

# grid up our controls on the main GUI....
# instruments group controls
grp_instruments.grid(column=0, row=0, sticky=(N, S, W, E))
cbo_instruments.grid(column=0, row=0, columnspan=2, sticky=(W, E))
btn_connect.grid(column=0, row=1, sticky=(W, E))
btn_refresh.grid(column=1, row=1, sticky=(W, E))

# next group controls on the main GUI....
grp_single_command_ops.grid(column=0, row=1, sticky=(N, S, W, E))
cbo_single_commands.grid(column=0, row=0, columnspan=3)
btn_cmd_write.grid(column=0, row=1, sticky=(W, E))
btn_cmd_query.grid(column=1, row=1, sticky=(W, E))
btn_clear_command_list.grid(column=2, row=1, sticky=(W, E))


# next group controls on the main GUI....
grp_multi_command_ops.grid(column=1, row=0, rowspan=2, sticky=(N, S, W, E))
txt_multi_command_text.grid(column=0, row=0, sticky=(N, S, W, E), rowspan=4)
s.grid(column=1, row=0, sticky=(N,S), rowspan=4)
btn_send_commands.grid(column=2, row=0, sticky=(N))
btn_clear_commands.grid(column=2, row=1, sticky=(N))
btn_save_commands.grid(column=2, row=2, sticky=(N))
btn_load_commands.grid(column=2, row=3, sticky=(N))
grp_execution_mode.grid(column=0, row=4, sticky=(W, E), columnspan=3)

rdo_option_1.grid(column=0, row=0, sticky=(W, E))
lbl_rdo1_buffer.grid(column=0, row=1)

rdo_option_2.grid(column=1, row=0, sticky=(W, E))
txt_timed_s.grid(column=1, row=1)
lbl_timed_s.grid(column=2, row=1)

rdo_option_3.grid(column=3, row=0, sticky=(W, E))
btn_stepper.grid(column=3, row=1)


# While the expected initial connected state will truly be false, we set to True here
# then invoke the connect/disconnect function so that it sets the state of the controls.
is_connected.set(True)
btn_connect.invoke()

root.mainloop()