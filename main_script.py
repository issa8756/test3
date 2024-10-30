import subprocess
import argparse
import logging

# Configure logging
logging.basicConfig(filename='main_script.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_encrypt_tool(action, filename=None):
    """Run the encryption tool."""
    command = ['python', 'Encrypt_tool.py', action]
    if filename:
        command.append(filename)

    logging.info(f"Running encryption tool with action: {action} and filename: {filename}")
    subprocess.run(command)

def run_nmap_scanner(ips, scan_type, output=None, speed=None, ports=None):
    """Run the nmap scanning tool."""
    command = ['python', 'nmap_scaning_tool.py', ips]
    command.extend(['-t', scan_type])
    
    if output:
        command.extend(['-o', output])
    if speed:
        command.extend(['-T', str(speed)])
    if ports:
        command.extend(['-p', ','.join(ports)])
    
    logging.info(f"Running nmap scanner tool on IPs: {ips} with scan type: {scan_type}")
    subprocess.run(command)

def run_brute_force_tool(ip, attack_type, passwords_file, username=None, usernames_file=None, threads=False):
    """Run the brute force tool."""
    command = ['python', 'brute_force_tool.py', ip, attack_type, passwords_file]
    if username:
        command.extend(['-u', username])
    if usernames_file:
        command.extend(['-u_list', usernames_file])
    if threads:
        command.append('-t')

    logging.info(f"Running brute force tool on IP: {ip} with attack type: {attack_type}")
    subprocess.run(command)

def main():
    parser = argparse.ArgumentParser(description="Main script to run various tools.")
    
    # Define subparsers for different tools
    subparsers = parser.add_subparsers(dest='tool', required=True)

    # Subparser for the encryption tool
    encrypt_parser = subparsers.add_parser('encrypt_tool', help='Run the encryption tool')
    encrypt_parser.add_argument('action', choices=['generate_key', 'encrypt', 'decrypt'], help='Action to perform')
    encrypt_parser.add_argument('filename', nargs='?', help='File to encrypt or decrypt')

    # Subparser for the nmap scanner tool
    nmap_parser = subparsers.add_parser('nmap_scanner_tool', help='Run the nmap scanner tool')
    nmap_parser.add_argument('ips', help='Target IP addresses (comma separated if multiple)')
    nmap_parser.add_argument('-t', '--type', choices=['syn', 'udp', 'os', 'version'], required=True, help='Type of scan to run')
    nmap_parser.add_argument('-o', '--output', help='File to save the scan results')
    nmap_parser.add_argument('-T', '--speed', type=int, choices=[0, 1, 2, 3, 4, 5], help='Set the timing template')
    nmap_parser.add_argument('-p', '--ports', help='Comma separated list of ports to scan (e.g. 22,80)')

    # Subparser for the brute force tool
    brute_force_parser = subparsers.add_parser('brute_force_tool', help='Run the SSH brute force tool')
    brute_force_parser.add_argument('ip', help='Target IP address')
    brute_force_parser.add_argument('attack_type', choices=['normal', 'reverse'], help='Type of attack')
    brute_force_parser.add_argument('passwords_file', help='File containing passwords')
    brute_force_parser.add_argument('-u', '--username', help='Username for normal attack')
    brute_force_parser.add_argument('-u_list', '--usernames_file', help='File containing usernames for reverse mode')
    brute_force_parser.add_argument('-t', '--threads', action='store_true', help='Enable threading for reverse attack')

    args = parser.parse_args()

    if args.tool == 'encrypt_tool':
        run_encrypt_tool(args.action, args.filename)
    elif args.tool == 'nmap_scanner_tool':
        run_nmap_scanner(args.ips, args.type, args.output, args.speed, args.ports.split(',') if args.ports else None)
    elif args.tool == 'brute_force_tool':
        run_brute_force_tool(args.ip, args.attack_type, args.passwords_file, args.username, args.usernames_file, args.threads)

if __name__ == "__main__":
    main()
