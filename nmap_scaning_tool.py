import argparse
import nmap

# Function to scan IP addresses
def scan_ips(ips, scan_type, save_to_file, speed_option, ports):
    nm = nmap.PortScanner()  

    # Convert the list of IPs into a comma-separated string
    ips_string = ",".join(ips)

    # Build the scan arguments
    scan_arguments = ""
    if speed_option:
        scan_arguments += f"-T{speed_option} "  # Add speed option if provided

    # Convert the list of ports into a comma-separated string
    if ports:
        ports_str = ",".join(ports)
    else:
        ports_str = ""


    print(f"Ports to scan: {ports_str}")

    # Select the scan type based on the provided flags
    if scan_type == 'syn':
        print(f"Starting SYN scan on: {ips_string} for ports: {ports_str}")
        nm.scan(hosts=ips_string, arguments=f"{scan_arguments}-sS {ports_str}")  # Perform SYN scan
    elif scan_type == 'udp':
        print(f"Starting UDP scan on: {ips_string} for ports: {ports_str}")
        nm.scan(hosts=ips_string, arguments=f"{scan_arguments}-sU {ports_str}")  # Perform UDP scan
    elif scan_type == 'os':
        print(f"Starting OS detection scan on: {ips_string}")
        nm.scan(hosts=ips_string, arguments=f"{scan_arguments}-O")  # Perform OS detection scan
    elif scan_type == 'version':
        print(f"Starting version detection scan on: {ips_string}")
        nm.scan(hosts=ips_string, arguments=f"{scan_arguments}-sV")  # Perform version detection scan
    else:
        print(f"Unknown scan type '{scan_type}'. Exiting.")  # Handle unknown scan type
        return

    # Collect and display the scan results
    results = []
    for host in nm.all_hosts():
        result = f"\nHost: {host} ({nm[host].hostname() or 'Unknown'})\nState: {nm[host].state()}"
        for proto in nm[host].all_protocols():
            ports = nm[host][proto].keys()  # Get all ports for the protocol
            result += f"\nProtocol: {proto}"
            for port in ports:
                state = nm[host][proto][port]['state']  # Get the state of the port
                service = nm[host][proto][port].get('name', 'Unknown')  # Get the service name
                service_desc = nm[host][proto][port].get('product', 'No description')  # Get service description
                result += f"\nPort: {port}\tState: {state}\tService: {service}\tDescription: {service_desc}"
        print(result)  # Print the result for each host
        results.append(result)  # Append results for saving

    # Save results to a file if required
    if save_to_file:
        with open(save_to_file, 'w') as f:
            f.write("\n".join(results))  
        print(f"Results saved to {save_to_file}")  

# Main function to handle argument parsing
def main():
    
    parser = argparse.ArgumentParser(description="Nmap Scanner using Python. Some scans require root privileges.")
    
    # Add arguments for IP addresses, scan type, output file, speed option, and ports
    parser.add_argument("ips", help="Target IP addresses (comma separated if multiple)")
    parser.add_argument("-t", "--type", choices=["syn", "udp", "os", "version"], required=True,
                        help="Type of scan to run")
    parser.add_argument("-o", "--output", help="File to save the scan results")
    parser.add_argument("-T", "--speed", type=int, choices=[0, 1, 2, 3, 4, 5], 
                        help="Set the timing template (0: Paranoid, 1: Sneaky, 2: Polite, 3: Normal, 4: Aggressive, 5: Insane).")
    parser.add_argument("-p", "--ports", help="Comma separated list of ports to scan (e.g. 22,80)")

    
    args = parser.parse_args()

    
    scan_ips(args.ips.split(","), args.type, args.output, args.speed, args.ports.split(",") if args.ports else [])


if __name__ == "__main__":
    main()
