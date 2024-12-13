# modules/config_loader.py
import json

class ConfigLoader:
    @staticmethod
    def load_config(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    
    @classmethod
    def load_general_config(cls, config_path="config/config.json"):
        return cls.load_config(config_path)
    
    @classmethod
    def load_targets(cls, targets_path="config/targets.json"):
        # Extract the list under "targets" key
        return cls.load_config(targets_path)["targets"]
    
    @classmethod
    def load_viewports(cls, viewports_path="config/viewports.json"):
        return cls.load_config(viewports_path)

    @classmethod
    def load_servers(cls, servers_path="config/servers.json"):
        return cls.load_config(servers_path)

    @classmethod
    def load_user_agents(cls, agents_path="config/user_agents.json"):
        return cls.load_config(agents_path)
