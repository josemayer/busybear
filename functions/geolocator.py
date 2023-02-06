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

def closest_point(center, list_points):
    closest_point = list_points[0]
    closest_location = (float(closest_point["lat"]), float(closest_point["lng"]))
    closest_distance = haversine(center, closest_location)
    
    for point in list_points[1:]:
        location = (float(point["lat"]), float(point["lng"]))
        distance = haversine(center, location)
        if distance < closest_distance:
            closest_distance = distance
            closest_point = point
    
    return closest_point
