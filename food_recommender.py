import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

class FoodRecommender:
    def __init__(self):
        self.gdf = self._get_gdf()
        self.restaurants = pd.read_csv("./data/restaurants.csv")

    def _get_gdf(self):
        gdf = gpd.read_file("./data/master_plan_zone.geojson")
        gdf['Name'] = gdf['PLN_AREA_N']
        return gdf

    def _get_user_zone(self, coordinates):
        point = Point(*coordinates)
        for zone in range(self.gdf.shape[0]):
            if(point.within(self.gdf.loc[zone, 'geometry'])):
                return self.gdf.loc[zone, 'Name']

    def get_ranked_restaurants(self, coordinates, cuisine_chosen):
        zone = self._get_user_zone(coordinates)

        # filter by zone
        df = self.restaurants[self.restaurants['zone'] == zone]

        # filter by cuisine
        df = df[df['cuisines'].str.contains(cuisine_chosen)]

        # ranked by ratings and return the top 5 restaurants information
        res = df.sort_values(by='rating', ascending=False)[['name', "address", "cuisines", "rating"]].to_dict('records')

        return res


if __name__ == "__main__":
    fr = FoodRecommender()
    print(fr.get_ranked_restaurants((103.95, 1.35), "Afghan"))
    