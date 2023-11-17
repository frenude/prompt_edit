from pathlib import Path
import pytomlpp

from src.conf.config import Config

config_name = "config.toml"
cfg = Config(
    **pytomlpp.loads((Path(__file__).resolve().parent.parent.parent / config_name).read_text(encoding="utf-8")))
