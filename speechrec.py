
    # This script uses speech recognition to execute commands based on voice input.

import subprocess
import os

def install_module(module_name):
    
    # Install a Python module using pip.
    # Args:
    #     module_name (str): The name of the module to install.
    
    try:
        subprocess.run(["pip", "install", module_name], check=True)
        print(f"Successfully installed the '{module_name}' module.")
    except subprocess.CalledProcessError as error:
        print(f"Error installing the '{module_name}' module: {error}")

try:
    import speech_recognition as sr
except ModuleNotFoundError:
    print("The 'speech_recognition' module is not installed. Installing it now...")
    install_module("speech_recognition")
    import speech_recognition as sr

def get_audio():
    
    # Record audio from the microphone and convert it to text using Google's speech recognition.
    
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something")
        try:
            audio_text = recognizer.listen(source)
            recognized_text = recognizer.recognize_google(audio_text, show_all=False)
            if recognized_text:
                return recognized_text
            print("Sorry, I could not understand what you said.")
        except sr.WaitTimeoutError:
            print("No speech detected. Please try again.")
        except sr.UnknownValueError:
            print("Sorry, I could not understand what you said.")
        return 

def execute_command(recognized_text, commands):
    
    # Execute a command based on recognized text.
    # Args:
    #     recognized_text (str): The text recognized from speech input.
    #     commands (dict): A dictionary of recognized text and corresponding actions.
    # Returns:
    #     bool: True if a command was successfully executed, False otherwise.
    
    for keyword, action in commands.items():
        if keyword in recognized_text:
            try:
                if "open" in keyword:
                    subprocess.Popen(action, shell=True)
                    print(f"Opening: {action}")
                    return True
                else:
                    subprocess.run(action, shell=True, check=True)
                    print(f"Command executed: {action}")
                    return True
            except subprocess.CalledProcessError as error:
                print(f"Error executing command: {error}")
    print("Command not recognized or could not be executed.")
    return False

def close_program(program_name):
    
    # Close a program with the specified name if it's running.
    
    try:
        os.system(f"pkill -f {program_name}")
        print(f"Closed {program_name}")
    except Exception as error:
        print(f"Error closing {program_name}: {error}")

def run_terminal_command(command):
    
    # Run a command in the terminal.
    # Args:
    #     command (str): The command to run in the terminal.
    
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Command executed in the terminal: {command}")
    except subprocess.CalledProcessError as error:
        print(f"Error executing command in the terminal: {error}")

def read_commands_from_file(filename):
    
    # Read and parse commands from a file.
    # Args:
    #     filename (str): The name of the file containing commands.
    # Returns:
    #     dict: A dictionary of recognized text and corresponding actions.
    
    commands = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split(':', 1)
                if len(parts) == 2:
                    command, action = parts
                    commands[command] = action
                else:
                    print(f"Invalid line in the file: {line.strip()}. Skipping.")
        return commands
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return {}
    
def main():
    
    # The main function to run the speech recognition and command execution loop.
    
    command_file = "commands.txt"
    commands = read_commands_from_file(command_file)
    opened_command = None

    while True:
        audio_text = get_audio()

        if audio_text:
            print("You said: " + audio_text)
        if "close" in audio_text:
            if opened_command:
                close_program(opened_command)
                opened_command = None
            else:
                print("No command is currently open.")
            break
        elif execute_command(audio_text, commands):
            opened_command = commands.get(audio_text, None)
        else:
            print("Sorry, I did not hear anything")

if __name__ == "__main__":
    main()
    

