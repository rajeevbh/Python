import csv
import os
import xml.etree.ElementTree as ET
import winrm

# Path to the CSV file containing server details
csv_file_path = "servers.csv"

# AppDynamics configuration
appdynamics_download_url = "https://download.appdynamics.com/download/file/machine_agent.zip"  # Update with the actual URL
install_path = r"C:\AppDynamics\MachineAgent"
controller_host = "your-controller-host"  # Update with your AppDynamics controller details
controller_port = "8090"
account_name = "your-account-name"
access_key = "your-access-key"

# Function to run a command remotely using pywinrm
def run_remote_command(server, username, password, command):
    session = winrm.Session(f'http://{server}:5985/wsman', auth=(username, password))
    result = session.run_cmd(command)
    if result.status_code == 0:
        return result.std_out.decode('utf-8')
    else:
        return result.std_err.decode('utf-8')

# Function to download, extract and install AppDynamics Machine Agent remotely
def install_machine_agent(server_name, domain_name, server_hierarchy, username, password):
    print(f"Processing {server_name} in {domain_name} under {server_hierarchy}...")

    # PowerShell script to download, extract and install AppDynamics Machine Agent
    powershell_script = f"""
    if (-Not (Test-Path {install_path})) {{
        New-Item -Path {install_path} -ItemType Directory
    }}
    
    $zip_path = "{install_path}\\machine_agent.zip"
    Invoke-WebRequest -Uri "{appdynamics_download_url}" -OutFile $zip_path

    Add-Type -AssemblyName System.IO.Compression.FileSystem
    [System.IO.Compression.ZipFile]::ExtractToDirectory($zip_path, "{install_path}")
    Remove-Item $zip_path -Force

    $config_file = "{install_path}\\conf\\controller-info.xml"
    if (Test-Path $config_file) {{
        $xml = [xml](Get-Content $config_file)
        $xml.'controller-info'.'controller-host' = "{controller_host}"
        $xml.'controller-info'.'controller-port' = "{controller_port}"
        $xml.'controller-info'.'account-name' = "{account_name}"
        $xml.'controller-info'.'account-access-key' = "{access_key}"
        $xml.Save($config_file)
    }}

    $agent_path = "{install_path}\\bin\\machine-agent.bat"
    if (Test-Path $agent_path) {{
        Start-Process -FilePath $agent_path -ArgumentList "install-service" -Wait
        Start-Service -Name "AppDynamicsMachineAgent"
    }}
    """

    # Execute the PowerShell script remotely
    result = run_remote_command(server_name, username, password, powershell_script)
    print(result)

# Read the server list from CSV
with open(csv_file_path, mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        server_name = row['ServerName']
        domain_name = row['DomainName']
        server_hierarchy = row['ServerHierarchy']
        username = row['Username']  # Assuming the CSV has username and password for each server
        password = row['Password']
        
        # Call the function to install the Machine Agent on each server
        install_machine_agent(server_name, domain_name, server_hierarchy, username, password)
