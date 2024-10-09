import math

# all distances in kilometers

class GroundStation:
    def __init__(self, latitude, longitude, altitude):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

    def distance_to_satellite(self, sat_latitude, sat_longitude, sat_altitude):
        R = 6371  # Earth's radius (km)

        lat1 = math.radians(self.latitude)
        lon1 = math.radians(self.longitude)
        lat2 = math.radians(sat_latitude)
        lon2 = math.radians(sat_longitude)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        distance = R * c
        return distance

    def is_visible(self, sat_latitude, sat_longitude, sat_altitude):
        # Determine if the satellite is visible from the ground station
        # Simplified, assuming no obstructions and clear line of sight.
        distance = self.distance_to_satellite(sat_latitude, sat_longitude, sat_altitude)
        max_distance = 2000

        return distance <= max_distance

# Example usage
ground_station = GroundStation(latitude=34.05, longitude=-118.25, altitude=0)  # Los Angeles, CA
satellite_latitude = 35.0
satellite_longitude = -120.0
satellite_altitude = 500  # Example (km)

print("Distance to satellite:", ground_station.distance_to_satellite(satellite_latitude, satellite_longitude, satellite_altitude))
print("Is satellite visible?", ground_station.is_visible(satellite_latitude, satellite_longitude, satellite_altitude))