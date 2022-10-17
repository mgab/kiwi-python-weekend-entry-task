from dataclasses import dataclass, replace
from datetime import datetime, timedelta
from typing import List, NewType, Type, TypeVar


FlightNo: Type = NewType('FlightNo', str)

AirportCode: Type = NewType('AirportCode', str)


@dataclass(frozen=True)
class Flight:
    flight_no: FlightNo  # type: ignore
    origin: AirportCode  # type: ignore
    destination: AirportCode  # type: ignore
    departure: datetime
    arrival: datetime
    base_price: float
    bag_price: float
    bags_allowed: int


T = TypeVar('T', bound='Itinerary')
@dataclass(frozen=True)
class Itinerary:
    flights: List[Flight]
    origin: AirportCode  # type: ignore
    destination: AirportCode  # type: ignore
    bags_allowed: int
    bags_count: int
    total_price: float
    travel_time: timedelta

    @classmethod
    def from_flight_list(cls: Type[T], flight_list: List[Flight], bags_count: int) -> T:
        return cls(flights=flight_list,
                   bags_allowed=min(f.bags_allowed for f in flight_list),
                   bags_count=bags_count,
                   origin=flight_list[0].origin,
                   destination=flight_list[-1].destination,
                   total_price=sum(f.base_price + f.bag_price * bags_count for f in flight_list),
                   travel_time=flight_list[-1].arrival - flight_list[0].departure
                   )

    def add_flight(self: T, new_flight: Flight) -> T:
        return replace(self,
                       flights=self.flights + [new_flight],
                       destination=new_flight.destination,
                       bags_allowed=min(self.bags_allowed, new_flight.bags_allowed),
                       total_price=self.total_price + new_flight.base_price + new_flight.bag_price + self.bags_count,
                       travel_time=self.travel_time + (new_flight.arrival - self.flights[-1].arrival)
                       )
