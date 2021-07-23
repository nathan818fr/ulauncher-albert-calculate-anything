import os
import json
from calculate_anything.logging_wrapper import LoggingWrapper as logging
from calculate_anything.utils.singleton import Singleton
from calculate_anything.constants import TIMEZONES_SQL_FILE


class TimezoneJsonCache(metaclass=Singleton):
    def __init__(self):
        self._data = {}
        self._logger = logging.getLogger(__name__)
        try:
            with open(TIMEZONES_SQL_FILE, 'r') as f:
                self._data = json.loads(f.read())
        except Exception as e:
            self._logger.error('Could not load timezone data: {}'.format(e))

    def get(self, city_name, *search_terms):
        city_code = city_name.strip().lower()
        if city_code not in self._data:
            return []
        cities = self._data[city_code]
        if not search_terms:
            return cities

        search_terms = [s.lower() for s in search_terms]
        cities_found = []
        for city in cities:
            found_all = True
            for search_term in search_terms:
                if search_term == city['state'].lower():
                    found = True
                elif search_term == city['country'].lower():
                    found = True
                elif search_term == city['cc'].lower():
                    found = True
                elif search_term == city['timezone'].lower():
                    found = True
                else:
                    found = False

                if not found:
                    found_all = False
                    break

            if found_all:
                cities_found.append(city)
        return cities_found or cities