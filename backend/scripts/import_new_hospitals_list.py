from distributor.models import Region, District, Locality, Hospital
import csv, requests, os
from django.contrib.gis.geos import fromstr

def run():
    with open('scripts/new_hospital_list.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count < 2:
                print(f'Column names are {", ".join(row)}')
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

                hospital_code = row[2]
                hospital_name = row[4]
                address = row[5]
                try:
                    hospital = Hospital.objects.get(code=hospital_code)
                    locality = hospital.locality 
                except:
                    locality = None
                    if district.locality_set.count() == 1:
                        locality = district.locality_set.first()
                    else:
                        for l in district.locality_set.all():
                            if l.name in address:
                                locality = l
                                break
                    if locality is None:
                        locality = Locality(name=district_name, district=district)
                        locality.save()
                    hospital = Hospital(code=hospital_code, name=hospital_name, locality=locality)

                r = requests.get('https://maps.googleapis.com/maps/api/place/findplacefromtext/json', 
                    params={'input': f'{address}', 'inputtype':'textquery', 'fields': 'name,geometry', 'key': os.environ.get("MAP_API_KEY")})
                candidates = r.json()["candidates"]
                candidate = None
                if len(candidates) > 0:
                    candidate = candidates[0]

                if candidate:
                    lat = candidate["geometry"]["location"]["lat"]
                    lng = candidate["geometry"]["location"]["lng"]
                    hospital.location = fromstr(f'POINT({lng} {lat})', srid=4326)
                    
                hospital.save()
                
                print(f'{region.name} \t{district.name} \t{locality.name} \t {hospital.name}.')
            line_count += 1
        print(f'Import {line_count} lines.')