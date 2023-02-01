
# Hide PyGame welcome message
import yaml
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# Load config file

with open("config.yml", "r") as cfg:
    CONFIG = yaml.safe_load(cfg)
