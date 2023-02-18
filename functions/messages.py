def format_bullets(list):
    dash = '- '
    string = dash + f'\n{dash}'.join(list)
    return string

def format_buses_arrival(points, buses_key):
    string = "*Estimativas de Chegada:*\n\n"
    for (key, point) in points.items():
        string += f"- *{point['titulo']}*:\n"
        for bus in point[buses_key]:
            distance = bus["distance"]
            points_str = "pontos" if distance > 1 else "ponto"
            string += f"    - *{bus['bus_line']}* há {str(distance)} {points_str} de distância.\n"
        string += "\n"
    return string
