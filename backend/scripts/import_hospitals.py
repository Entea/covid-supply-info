from distributor.models import Region, District, Locality, Hospital
import csv, requests, os
from django.contrib.gis.geos import fromstr

def run():
    with open('scripts/hospital_list.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                region_name = row[0]
                try:
                    region = Region.objects.get(name=region_name)
                except:
                    region = Region(name=region_name)
                    region.save()

                district_name = row[1]
                try:
                    district = District.objects.get(name=district_name, region=region)
                except:
                    district = District(name=district_name, region=region)
                    district.save()

                locality_name = row[3]
                try:
                    locality = Locality.objects.get(name=locality_name, district=district)
                except:
                    locality = Locality(name=locality_name, district=district)
                    locality.save()

                hospital_code = row[4]
                hospital_name = row[6]
                try:
                    hospital = Hospital.objects.get(code=hospital_code, locality=locality)
                except:
                    hospital = Hospital(code=hospital_code, name=hospital_name, locality=locality)
                    r = requests.get('https://maps.googleapis.com/maps/api/place/findplacefromtext/json', 
                        params={'input': f'{hospital_name} {locality.name} {region.name}', 'inputtype':'textquery', 'fields': 'name,geometry', 'key': os.environ.get("MAP_API_KEY")})
                    candidates = r.json()["candidates"]
                    candidate = None
                    if len(candidates) > 1:
                        candidate = candidates[1]
                    elif len(candidates) > 0:
                        candidate = candidates[0]

                    if candidate:
                        lat = candidate["geometry"]["location"]["lat"]
                        lng = candidate["geometry"]["location"]["lng"]
                        hospital.location = fromstr(f'POINT({lng} {lat})', srid=4326)
                    
                    hospital.save()
                
                print(f'{region.name} \t{district.name} \t{locality.name} \t {hospital.name}.')
                line_count += 1
        print(f'Import {line_count} lines.')