import json
import os

class Bootstrap():

    def __init__(self):
        self.config_path = "Config/config.json"
        self.start_program()
    
    def start_program(self):
        self.get_config()


    def get_config(self):
        try:
            with open(self.config_path, 'r') as file_config:
                text_file = file_config.read()
                json_config = json.loads(text_file)
        except Exception as e:
            os.system('clear')
            print("Errore:")
            print(e)
            return 1
        
        self.url_shard_0 = json_config["url_shard_0"]
        self.url_shard_1 = json_config["url_shard_1"]
        self.url_shard_2 = json_config["url_shard_2"]
        self.url_shard_3 = json_config["url_shard_3"]



