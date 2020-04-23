from distributor.models import Region, District, Locality, Hospital
import csv, requests, os
from django.contrib.gis.geos import fromstr

# Script imports data that wasn't imported by import_hospitals.py
def run():
    with open('scripts/new_hospital_list.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count < 2:
                print(f'Column names are {", ".join(row)}')
            else:
                region_name = row[0]
                region, created = Region.objects.get_or_create(name=region_name)
                if created:
                    print(f'\tCreated region: {region_name}')

                district_name = row[1]
                district, created = District.objects.get_or_create(name=district_name, region=region)
                if created:
                    print(f'\tCreated district: {district_name}')

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
                        locality, created = Locality.objects.get_or_create(name=district_name, district=district)
                        if created:
                            print(f'Creating new locality: {district_name}')

                    # Create new hospital and fill out fields
                    hospital = Hospital(code=hospital_code, name=hospital_name, locality=locality)

                r = requests.get('https://maps.googleapis.com/maps/api/place/findplacefromtext/json', 
                    params={'input': f'{address}', 'inputtype':'textquery', 'fields': 'name,geometry', 'key': os.environ.get("MAP_API_KEY")})
                candidates = r.json()["candidates"]
                print(f'Candidates: {candidates}')
                candidate = None
                if len(candidates) > 0:
                    candidate = candidates[0]

                if candidate:
                    lat = candidate["geometry"]["location"]["lat"]
                    lng = candidate["geometry"]["location"]["lng"]
                    new_loc = fromstr(f'POINT({lng} {lat})', srid=4326)
                    print(f'Updating hospital location from {hospital.location} to {new_loc}')
                    hospital.location = new_loc

                hospital.save()
                
                print(f'{region.name} \t{district.name} \t{locality.name} \t {hospital.name}.')
            line_count += 1
        print(f'Import {line_count} lines.')
