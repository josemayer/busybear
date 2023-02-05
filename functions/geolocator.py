import math

def haversine(center, location):
    earth_radius = 6371e3 # radius of the Earth in meters

    center_lat, center_lng = center
    lat, lng = location

    d_lat = math.radians(lat - center_lat)
    d_lng = math.radians(lng - center_lng)
    center_lat = math.radians(center_lat)
    lat = math.radians(lat)

    a = (math.sin(d_lat / 2)**2) + math.cos(center_lat) * math.cos(lat) * (math.sin(d_lng / 2)**2)
    c = 2 * math.asin(math.sqrt(a))
    distance = earth_radius * c

    return distance

def is_within_radius(center, location):
    return haversine(center, location) <= 250
