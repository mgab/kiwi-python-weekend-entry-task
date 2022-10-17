from dataclasses import asdict as dataclass_asdict
from datetime import datetime, timedelta
import csv
import json
from pathlib import Path
from typing import Iterator, List, Optional

from .models import AirportCode, Flight, FlightNo, Itinerary


def _parse_flight(flight_no: str, origin: str, destination: str, departure: str, arrival: str, base_price: str, bag_price: str, bags_allowed: str) -> Flight:
    return Flight(flight_no = FlightNo(flight_no),
                  origin = AirportCode(origin),
                  destination = AirportCode(destination),
                  departure = datetime.fromisoformat(departure),
                  arrival = datetime.fromisoformat(arrival),
                  base_price = float(base_price),
                  bag_price = float(bag_price),
                  bags_allowed = int(bags_allowed))


def load_flights_record(file_path: Path) -> Iterator[Flight]:
    with file_path.open() as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        headers = next(csv_reader)
        for row in csv_reader:
            yield _parse_flight(**dict(zip(headers, row)))


def _json_serial(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, timedelta):
        return str(obj)
    raise TypeError ("Type %s not serializable" % type(obj))


def dump_itinerary_list(itinerary_list: List[Itinerary], file_path: Optional[Path] = None) -> None:
    json_string = json.dumps([dataclass_asdict(itinerary) for itinerary in itinerary_list],
                             indent=2,
                             default=_json_serial)
    if file_path:
        with file_path.open('w') as json_file:
            json_file.write(json_string)
    else:
        print(json_string)
