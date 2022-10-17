from datetime import timedelta
from itertools import groupby
from typing import Dict, List
from .models import AirportCode, Flight, Itinerary

_min_connection_time = timedelta(hours=1)
_max_connection_time = timedelta(hours=6)

def is_valid_connection(fst: Flight, snd: Flight) -> bool:
    return (fst.destination == snd.origin
            and _min_connection_time < snd.departure - fst.arrival < _max_connection_time)

def _get_origin(x: Flight) -> AirportCode:
    return x.origin

def group_by_origin(flights: List[Flight]) -> Dict[AirportCode, List[Flight]]:
    return {k: list(v) for k, v in
            groupby(sorted(flights, key=_get_origin), key=_get_origin)}

def find_itineraries(flights: List[Flight], origin: AirportCode, destination: AirportCode, bag_count: int):
    itineraries = [Itinerary.from_flight_list(flight_list, bag_count)
                   for flight_list in find_flight_seqs(flights, origin, destination, bag_count)]
    return list(sorted(itineraries, key=lambda x: x.total_price))

def find_flight_seqs(flights: List[Flight], origin: AirportCode, destination: AirportCode, bag_count: int):
    for potential_flight in flights:
        if potential_flight.origin == origin and potential_flight.bags_allowed >= bag_count:
            yield from _continue_itinerary(flights, [potential_flight], destination, bag_count)

def _continue_itinerary(flights: List[Flight], itinerary: List[Flight], destination: AirportCode, bag_count: int):
    if itinerary[-1].destination == destination:
        yield itinerary
    visited_cities = {f.origin for f in itinerary}
    for potential_flight in flights:
        if potential_flight.bags_allowed < bag_count or potential_flight.destination in visited_cities:
            continue
        elif is_valid_connection(itinerary[-1], potential_flight):
            yield from _continue_itinerary(flights, itinerary + [potential_flight], destination, bag_count)
