from dataclasses import replace
from datetime import datetime, timedelta

from ..logic import find_itineraries, is_valid_connection
from ..models import AirportCode, Flight, FlightNo, Itinerary


flight1 = Flight(
    flight_no=FlightNo('X11'),
    origin=AirportCode('AAA'),
    destination=AirportCode('BBB'),
    departure=datetime.fromisoformat('2022-01-01T10:00:00'),
    arrival=datetime.fromisoformat('2022-01-01T12:00:00'),
    base_price=30.,
    bag_price=10.,
    bags_allowed=2
)


flight2 = Flight(
    flight_no=FlightNo('Y22'),
    origin=AirportCode('BBB'),
    destination=AirportCode('CCC'),
    departure=datetime.fromisoformat('2022-01-01T14:00:00'),
    arrival=datetime.fromisoformat('2022-01-02T14:00:00'),
    base_price=30.,
    bag_price=10.,
    bags_allowed=2
)


def test_is_valid_connection_valid():
    assert is_valid_connection(flight1, flight2)


def test_is_valid_connection_different_origin():
    flight3 = replace(flight2, origin=AirportCode('EEE'))
    assert not is_valid_connection(flight1, flight3)


def test_is_valid_connection_long_wait():
    flight3 = replace(flight2,
                      departure=flight1.arrival + timedelta(minutes=59))
    assert not is_valid_connection(flight1, flight3)


def test_is_valid_connection_short_wait():
    flight3 = replace(flight2,
                      departure=flight1.arrival + timedelta(hours=6, minutes=1))
    assert not is_valid_connection(flight1, flight3)


def test_find_itineraries_no_options():
    itineraries = find_itineraries(flights=[flight1, flight2],
                                   origin=AirportCode('AAA'),
                                   destination=AirportCode('XXX'),
                                   bag_count=0)
    assert list(itineraries) == []


def test_find_itineraries_direct_flight():
    itineraries = find_itineraries(flights=[flight1, flight2],
                                   origin=AirportCode('AAA'),
                                   destination=AirportCode('BBB'),
                                   bag_count=0)
    assert list(itineraries) == [Itinerary.from_flight_list([flight1], 0)]


def test_find_itineraries_multiple_options():
    flight3 = replace(flight1,
                      departure=flight1.departure + timedelta(hours=5),
                      arrival=flight1.arrival + timedelta(hours=10),
                      bags_allowed=3,
                      base_price=flight1.base_price + 1000)
    itineraries = find_itineraries(flights=[flight3, flight1, flight2],
                                   origin=AirportCode('AAA'),
                                   destination=AirportCode('BBB'),
                                   bag_count=0)
    assert list(itineraries) == [Itinerary.from_flight_list([flight1], 0), Itinerary.from_flight_list([flight3], 0)]


def test_find_itineraries_direct_flight_number_bags():
    flight3 = replace(flight1,
                      bags_allowed=3)
    itineraries = find_itineraries(flights=[flight1, flight2, flight3],
                                   origin=AirportCode('AAA'),
                                   destination=AirportCode('BBB'),
                                   bag_count=3)
    assert list(itineraries) == [Itinerary.from_flight_list([flight3], 3)]


def test_find_itineraries_one_stop():
    itineraries = find_itineraries(flights=[flight1, flight2],
                                   origin=AirportCode('AAA'),
                                   destination=AirportCode('CCC'),
                                   bag_count=0)
    assert list(itineraries) == [Itinerary.from_flight_list([flight1, flight2], 0)]


def test_find_itineraries_two_stops():
    flight3 = replace(flight2,
                      origin=AirportCode('CCC'),
                      destination=AirportCode('DDD'),
                      departure=flight2.arrival + timedelta(hours=2),
                      arrival=flight2.arrival + timedelta(hours=6))
    itineraries = find_itineraries(flights=[flight1, flight2, flight3],
                                   origin=AirportCode('AAA'),
                                   destination=AirportCode('DDD'),
                                   bag_count=0)
    assert list(itineraries) == [Itinerary.from_flight_list([flight1, flight2, flight3], 0)]
