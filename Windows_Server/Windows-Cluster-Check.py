import winrm
import logging

# Logging setup for high-level coding standards
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Server information (update with actual server IPs or hostnames)
servers = ["Server1", "Server2"]

# Define the PowerShell command to check cluster roles and services
CLUSTER_STATUS_CMD = """
Get-ClusterGroup | ForEach-Object {
    $_ | Select-Object -Property Name, OwnerNode, State
}
"""

# Define credentials for remote connection (update with actual credentials)
USERNAME = 'XXXXX'
PASSWORD = 'XXXXX!'

# Function to connect and run PowerShell command on Windows Server
def run_powershell(server, cmd):
    session = winrm.Session(server, auth=(USERNAME, PASSWORD))
    result = session.run_ps(cmd)
    if result.status_code == 0:
        return result.std_out.decode('utf-8')
    else:
        logging.error(f"Failed to run command on {server}. Error: {result.std_err.decode('utf-8')}")
        return None

# Function to parse and check cluster status
def check_cluster_status(server_output, server_name):
    # Parse the PowerShell output
    cluster_roles = []
    for line in server_output.splitlines():
        if "Name" in line or not line.strip():
            continue
        role_data = line.split()
        if len(role_data) >= 3:
            role_name, owner_node, state = role_data[0], role_data[1], role_data[2]
            cluster_roles.append({"name": role_name, "owner": owner_node, "state": state})
    
    # Ensure roles are running and distributed
    running_roles = [role for role in cluster_roles if role['state'] == 'Online']
    if len(running_roles) == 0:
        logging.warning(f"No roles are running on {server_name}.")
        return False
    
    # Log and check role distribution
    for role in cluster_roles:
        logging.info(f"Cluster role '{role['name']}' is on '{role['owner']}' and in '{role['state']}' state.")
    return True

# Main function to check both servers
def check_cluster_servers():
    all_good = True

    for server in servers:
        logging.info(f"Checking cluster roles and services on {server}...")
        cluster_output = run_powershell(server, CLUSTER_STATUS_CMD)
        
        if cluster_output:
            if not check_cluster_status(cluster_output, server):
                all_good = False
        else:
            all_good = False

    if all_good:
        logging.info("All cluster roles and services are running and distributed correctly.")
    else:
        logging.error("Cluster check failed: some roles or services are not distributed or running properly.")

if __name__ == '__main__':
    check_cluster_servers()
