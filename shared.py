left_side_of_regiment = 6
min_spacing = 4
max_length = 75

def points_text(num_points: int, num_places: int = 4) -> str:
    points = f"{num_points}"
    points = (num_places - len(points)) * " " + points + " Points"
    return points

def header_line(header_name: str, points_value: int) -> str:
        """Return a 'header' for the regiment display, limited to 120 characters"""
        points = points_text(points_value)
        
        max_name_length = max_length - len(points) - min_spacing - left_side_of_regiment
        if len(header_name) > max_name_length:
            header_name = header_name[:max_name_length]
        padding = max_length - len(points) - len(header_name) -left_side_of_regiment
        return header_name + " " * padding + points