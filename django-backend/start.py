import subprocess
import signal
import sys
import os
import time

processes = []

def start_process(cmd, cwd=None):
    if os.name == 'nt':  # Windows
        # CREATE_NEW_PROCESS_GROUP makes a new process group for each subprocess
        return subprocess.Popen(
            cmd,
            shell=True,
            cwd=cwd,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )
    else:
        # On Unix, use os.setsid to start a new session/process group
        return subprocess.Popen(
            cmd,
            shell=True,
            cwd=cwd,
            preexec_fn=os.setsid
        )

def handle_exit(signum, frame):
    print("Terminating all subprocesses...")
    for p in processes:
        try:
            if os.name == 'nt':
                # On Windows, send CTRL_BREAK_EVENT to the process group.
                p.send_signal(signal.CTRL_BREAK_EVENT)
            else:
                # On Unix, send SIGTERM to the entire process group.
                os.killpg(os.getpgid(p.pid), signal.SIGTERM)
        except Exception as e:
            print(f"Error terminating process {p.pid}: {e}")
    sys.exit(0)

def main():
    # Setup signal handlers so that Ctrl+C or termination signals trigger handle_exit.
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    # Start Django server from root directory
    p_django = start_process("python manage.py runserver 0.0.0.0:8000", cwd=".")
    processes.append(p_django)

    # Start Rasa Actions server from the subdirectory
    p_actions = start_process("rasa run actions", cwd="finance/rasa")
    processes.append(p_actions)

    # Start Rasa Server from the subdirectory
    p_rasa = start_process("rasa run --enable-api --model models --debug", cwd="finance/rasa")
    processes.append(p_rasa)

    try:
        # Keep the main script running so subprocesses remain active.
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        handle_exit(None, None)

if __name__ == "__main__":
    main()
