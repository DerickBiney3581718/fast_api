# List of coordinates
coords = (-0.0825291, 5.749422) ,(-0.0823508, 5.7492499) ,(-0.0822113, 5.7493993) ,(-0.0822596, 5.7495408) ,(-0.0825291, 5.749422)

# Initialize min and max values
min_lon = min(coord[0] for coord in coords)
max_lon = max(coord[0] for coord in coords)
min_lat = min(coord[1] for coord in coords)
max_lat = max(coord[1] for coord in coords)


# POLYGON ((-0.0825291 5.749422, -0.0823508 5.7492499, -0.0822113 5.7493993, -0.0822596 5.7495408, -0.0825291 5.749422))
# Create the bounding box
bounding_box = [min_lon, min_lat, max_lon, max_lat]

print(bounding_box) 

