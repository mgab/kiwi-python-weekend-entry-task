import argparse
from pathlib import Path

from .models import AirportCode

cli_parser = argparse.ArgumentParser()
cli_parser.add_argument('dataset_file', type=Path, metavar='dataset-file')
cli_parser.add_argument('origin', type=AirportCode)
cli_parser.add_argument('destination', type=AirportCode)
cli_parser.add_argument('--bags', default=0, type=int)
cli_parser.add_argument('--return', action='store_true')
