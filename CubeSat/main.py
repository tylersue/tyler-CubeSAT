import os
import sys
import subprocess
import run

serial_commands = {}

def serial_command(name):
    def wrapped(callback):
        serial_commands[name] = callback

        return callback

    return wrapped

@serial_command("ping")
def _(_):
    print("pong")

@serial_command("open")
def _(_):
    subprocess.Popen(["open", "-a", "Terminal"]) 
    result = subprocess.run(["python3", "run.py"], capture_output=True, text=True)

    print(result.stdout)
    print("")

def process_pc_command(cmd):
    if len(cmd) < 1:
        return

    print("# Processing command:", cmd, "length", len(cmd))

    args = cmd.split(" ")
    command = args.pop(0)

    if command not in serial_commands:
        print("error: unrecognized command")
        return

    try:
        serial_commands[command](args)
    except Exception as e:
        print("error: unexpected exception while processing command:", e)


def check_for_pc_command():
    serial_data_buffer = ""

    while True:
        data = sys.stdin.read(1)

        if ord(data) == 27:
            # delete, esc, arrow keys, etc.
            # too difficult to handle, just drop the character

            continue
        elif ord(data) == 127:
            # backspace
            serial_data_buffer = serial_data_buffer[:-1]
            print(data, end="")  # keep terminal state in sync

            return

        serial_data_buffer += data

        # if serial_echo:
        #     print(data, end="")

        if data == "\n":
            # command terminator
            process_pc_command(serial_data_buffer.strip("\n").strip("\r"))
            serial_data_buffer = ""


while True:
    check_for_pc_command()