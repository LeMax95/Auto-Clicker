# modules/vpn_manager.py
import subprocess
import random
import time

class VPNManager:
    def __init__(self, vpn_path, servers):
        self.vpn_path = vpn_path
        self.servers = servers

    def change_vpn(self):
        server = random.choice(self.servers)
        print(f"Connecting to VPN server: {server}")

        # Disconnect if already connected
        subprocess.run(f'cd /d "{self.vpn_path}" && ExpressVPN.CLI disconnect', shell=True)
        time.sleep(3)

        # Connect to a random server
        subprocess.run(f'cd /d "{self.vpn_path}" && ExpressVPN.CLI connect "{server}"', shell=True)
        time.sleep(10)
        print(f"Connected to {server}")
