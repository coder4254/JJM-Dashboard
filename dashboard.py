import os
import pandas as pd
import geopandas as gpd
from glob import glob
import folium
from folium.features import GeoJsonTooltip
from folium.plugins import MarkerCluster
import json


def load_data():
    df_fhtc = pd.read_csv('Karnataka_FHTC.csv')
    df_fhtc.shape
    df_fhtc = df_fhtc.sort_values(by='District').reset_index()
    df_fhtc = df_fhtc[['District','Household','Total_HH_Connection','Connection Coverage (%)']]
    return df_fhtc


def read_shapefiles(directory):
    shapefiles = glob(os.path.join(directory, '**/*.shp'), recursive=True)
    all_data = []
    # Iterate over each shapefile
    for shapefile in shapefiles:
        print(shapefile)
        try:
            gdf = gpd.read_file(shapefile)
            # Convert to WGS84 projection if needed
            if gdf.crs != "EPSG:4326":
                gdf = gdf.to_crs("EPSG:4326")
            all_data.append(gdf)
        except Exception as e:
            print(f"Error reading shapefile '{shapefile}': {e}")
    # Concatenate all GeoDataFrames into one
    combined_gdf = gpd.GeoDataFrame(pd.concat(all_data, ignore_index=True), crs=all_data[0].crs)
    return combined_gdf

def arrange_and_merge(dist_gdf, df_fhtc):
    dist_gdf['Area'] = dist_gdf['SHAPE_STAr'].apply(lambda x: (x / (1000*1000)))
    dist_gdf = dist_gdf.sort_values(by='KGISDist_1').reset_index()
    dist_gdf['District'] = df_fhtc['District']
    return dist_gdf #temp

def preprocess(temp):
    temp['URL'] = temp['District'].apply(lambda x: f"https://jjm-{x.lower()}.netlify.app")
    temp['URL'] = temp['URL'].apply(lambda x: x.replace(' ','-').replace('(','').replace(')',''))
    temp['Area'] = temp['Area'].apply(lambda x: int(x))
    cols_req = ['District', 'URL', 'Area', 'geometry']
    temp = temp[cols_req]
    return temp

def final_merge(temp, df_fhtc):
    df_merged = pd.merge(temp, df_fhtc, on='District', how='left')
    df_merged.to_csv('KARNATAKA.csv')
    print("Successfully Saved: KARNATAKA.csv")
    return df_merged 

def create_map(temp):
    geojson =  temp.to_json()
    geojson = json.loads(geojson)
    print("DONE: JSON")

    map_center = [temp['geometry'].centroid.y.mean(), temp['geometry'].centroid.x.mean()]
    map_zoom = 7
    mymap = folium.Map(
        location=map_center, 
        zoom_start=map_zoom, 
        tiles='cartodb-positron'
    )

    district_layer = folium.Choropleth(
        name="District",
        geo_data=geojson,  
        data=temp, 
        columns=['District', 'Connection Coverage (%)'], 
        key_on='feature.properties.District',  
        fill_color='Purples',  
        fill_opacity=1,
        line_color='black',
        line_opacity=1,
        legend_name="FHTC Coverage Percentage",
        bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100], 
        highlight=True,
        show=True
    )
    district_layer.add_to(mymap)

    # Function to format URL as clickable link
    def format_url(url):
        return f'<a href="{url}" target="_blank">{url}</a>'

    # Ensure the 'URL' field in the geojson contains clickable HTML links
    for feature in geojson['features']:
        if 'URL' in feature['properties']:
            feature['properties']['URL'] = format_url(feature['properties']['URL'])

    # Add Tooltip and Popup
    tooltip=folium.GeoJsonTooltip(
            fields=['District', 'Area', 'Household', 'Total_HH_Connection', 'Connection Coverage (%)'],
            aliases=['District:', 'Area (Sq.Km):', 'No.of Households:', 'Total HH Connection:', 'Connection Coverage (%):'],
            sticky=False,
            localize=True
        )
    tooltip.add_to(district_layer.geojson)
    popup=folium.GeoJsonPopup(
            fields=['URL'],
            aliases=['Report URL: '],
            localize=True
        )
    popup.add_to(district_layer.geojson)

    mymap.save('Index_Karnataka.html')
    print("Successfully Saved: Index_Karnataka.html")


# Calling functions linearly
df_fhtc = load_data()
dist_gdf = read_shapefiles('District/')
temp = arrange_and_merge(dist_gdf, df_fhtc)
temp = preprocess(temp)
df_merged = final_merge(temp, df_fhtc)
create_map(df_merged)
