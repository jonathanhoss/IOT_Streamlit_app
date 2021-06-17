from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure, output_file, show
from bokeh.tile_providers import CARTODBPOSITRON, get_provider
import database_conn

from pyproj import Proj, transform
def create_coordinates(long_arg, lat_arg):
    in_wgs = Proj(init='epsg:4326')
    out_mercator = Proj(init='epsg:3857')
    long, lat = long_arg, lat_arg
    mercator_x, mercator_y = transform(in_wgs, out_mercator, long, lat)
    return(mercator_x, mercator_y)


def create_map():
    tile_provider = get_provider(CARTODBPOSITRON)

    x1, y1 = create_coordinates(4.9619, 53.8706)
    x2, y2 = create_coordinates(15.739388, 46.670701)
    # range bounds supplied in web mercator coordinates
    p = figure(x_range=(x1, x2), y_range=(y1, y2),
            x_axis_type="mercator", y_axis_type="mercator")
    p.add_tile(tile_provider)

    TOOLTIPS = [
        ("Name", "@name"),
        ("Temperatur [°C]", "@temperatur"),
        ("Feuchte [%]", "@feuchte"),
        ("Luftdruck [hPa]", "@luftdruck")
        ]

    #data = [[47.820000,12.100000], [49.860000,10.383000], [47.862000,12.108000]]

    import pandas as pd

    df = pd.DataFrame(database_conn.get_last(), columns=['Name','Breitengrad','Laengengrad', 'Temperatur', 'Feuchte', 'Luftdruck'])
    df = df.drop_duplicates(subset=['Name'], keep='first')
    print(df)

    xl =[]
    yl = []
    for index, row in df.iterrows():
        print(row['Breitengrad'], row['Laengengrad'])
        x, y = create_coordinates(row['Laengengrad'], row['Breitengrad'])
        xl.append(x)
        yl.append(y)

    source = ColumnDataSource(data=dict(
        x = xl,
        y = yl,
        name = df['Name'],
        temperatur = df['Temperatur'],
        feuchte = df['Feuchte'],
        luftdruck = df['Luftdruck']
    ))
     
    p.circle('x','y', size=10, source=source)

    p.add_tools(HoverTool(tooltips=TOOLTIPS))

    #show(p)
    return(p)


if __name__ == "__main__":
    output_file("tile.html")
    show(create_map())




