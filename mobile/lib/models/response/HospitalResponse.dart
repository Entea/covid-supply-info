class HospitalResponse {
  final int count;

  final List<Hospital> hospitals;

  HospitalResponse(this.count, this.hospitals);

  factory HospitalResponse.fromJson(dynamic json) {
    var results = json['results'] as dynamic;
    var hospitals = <Hospital>[];
    for (var result in results) {
      var hospital = Hospital.fromJson(result);
      hospitals.add(hospital);
    }
    return HospitalResponse(json['count'] as int, hospitals);
  }
}

class Hospital {
  final int id;
  final String name;
  final String code;
  final double indicator;

  Hospital(this.id, this.name, this.code, this.indicator);

  factory Hospital.fromJson(dynamic json) {
    return Hospital(json['id'] as int, json['name'] as String,
        json['code'] as String, json['indicator'] as double);
  }
}
