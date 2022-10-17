from src.models import Itinerary
from src.cli import cli_parser
from src.io import load_flights_record, dump_itinerary_list
from src.logic import find_itineraries

if __name__ == '__main__':
    args = cli_parser.parse_args()
    flight_catalog = list(load_flights_record(args.dataset_file))

    itineraries = list(find_itineraries(flight_catalog, args.origin, args.destination, args.bags))

    dump_itinerary_list(itineraries)
