import ee
ee.Authenticate()
ee.Initialize(project='ee-sunnybrook')

# Define the area of interest with a bounding box
toronto = ee.Geometry.Rectangle([-79.639319, 43.403221, -79.115212, 43.855401])

# Define time range
start_date = '2018-01-01'
end_date = '2018-12-31'  # Example for a single year

# Load NAIP ImageCollection
naip_collection = ee.ImageCollection('USDA/NAIP/DOQQ') \
                    .filterBounds(toronto) \
                    .filterDate(start_date, end_date)

# You can print out the collection to see available images
print(naip_collection.getInfo())

# Use median to remove outliers and cloud shadows
naip_median = naip_collection.median()

# Export the image, specifying scale and region.
export = ee.batch.Export.image.toDrive(
    image=naip_median,
    description='NAIP_Toronto_2018',
    folder='NAIP_Images',
    fileNamePrefix='NAIP_Toronto_2018',
    scale=1,  # Specify the resolution for export
    region=toronto
)
export.start()



import requests

# Toronto Open Data is stored in a CKAN instance. It's APIs are documented here:
# https://docs.ckan.org/en/latest/api/

# To hit our API, you'll be making requests to:
base_url = "https://ckan0.cf.opendata.inter.prod-toronto.ca"

# Datasets are called "packages". Each package can contain many "resources"
# To retrieve the metadata for this package and its resources, use the package name in this page's URL:
url = base_url + "/api/3/action/package_show"
params = { "id": "web-map-services"}
package = requests.get(url, params = params).json()

# To get resource data:
for idx, resource in enumerate(package["result"]["resources"]):

       # To get metadata for non datastore_active resources:
       if not resource["datastore_active"]:
           url = base_url + "/api/3/action/resource_show?id=" + resource["id"]
           resource_metadata = requests.get(url).json()
           print(resource_metadata)
           # From here, you can use the "url" attribute to download this file
