import paramiko
import argparse
import time
import os

# Define SSH connection profiles
profiles = {
    'cryptonaut-ai': {'host': '188.166.152.224', 'username': 'root', 'password': 'rajesh@Rijwan24Ai'},
}

def ssh_connect(profile_key):
    profile = profiles.get(profile_key)
    
    if not profile:
        print(f"Profile '{profile_key}' not found.")
        return
    
    host = profile['host']
    username = profile['username']
    password = profile['password']
    
    # Initialize SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Connect to the SSH server
        client.connect(hostname=host, username=username, password=password)
        print(f"Connected to {host} as {username}")
        
        # Open an interactive shell session
        shell = client.invoke_shell()
        print("Interactive shell session opened. Type 'exit' to close the session.")
        
        while True:
            # Display current working directory with color
            shell.send('pwd\n')  # Request the current directory
            time.sleep(1)  # Wait a short time to ensure command execution
            
            # Read the output of the 'pwd' command
            output = ""
            while shell.recv_ready():
                output += shell.recv(1024).decode()
                if len(output) > 0 and output[-1] == '\n':
                    break
            
            # Print the current working directory with colors
            cwd = output.strip()
            colored_prompt = f"\033[42;31m{cwd}\033[0m "  # Green background, Red text
            command = input(f"{colored_prompt}Enter command: ")
            if command.lower() == 'exit':
                break
            
            # Send the command to the shell
            shell.send(command + '\n')
            
            # Wait for the command to complete and receive the output
            time.sleep(1)  # Wait a short time to ensure command execution
            output = ""
            while shell.recv_ready():
                output += shell.recv(1024).decode()
                # Continue reading until all output is received
                if len(output) > 0 and output[-1] == '\n':
                    break
            
            print(output)
        
        # Close the connection
        client.close()
        print("Connection closed.")
    except paramiko.AuthenticationException:
        print("Authentication failed. Please check your credentials.")
    except paramiko.SSHException as e:
        print(f"SSH Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="SSH CLI Tool")
    parser.add_argument('profile', type=str, help='Profile name to connect with')
    args = parser.parse_args()

    profile_key = args.profile
    ssh_connect(profile_key)
