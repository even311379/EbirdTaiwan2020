import folium
import geopandas

dd = geopandas.read_file('TOWN_MOI_1090727.shp')

tt = dd.to_crs("EPSG:4326").geometry[0]
test_points = list(tt.exterior.coords)

m = folium.Map(
        location = [23.5, 120.5],
        zoom_start = 10,
        tiles='Stamen Terrain'
    )

for i in test_points:
    folium.Marker(location=(i[1], i[0])).add_to(m)

m.save('foli.html')
