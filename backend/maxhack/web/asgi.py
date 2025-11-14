from maxhack.config import load_config
from maxhack.web.main import main

config = load_config()
app = main(config)
