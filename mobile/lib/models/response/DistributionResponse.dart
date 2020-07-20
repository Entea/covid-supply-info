import 'package:tirek_mobile/models/response/HospitalResponse.dart';

class DistributionResponse {
  final int count;
  final List<Distribution> distributions;

  DistributionResponse(this.count, this.distributions);

  factory DistributionResponse.fromJson(dynamic json) {
    var results = json['results'] as dynamic;
    var distributions = <Distribution>[];
    for (var result in results) {
      var distribution = Distribution.fromJson(result);
      distributions.add(distribution);
    }
    return DistributionResponse(json['count'] as int, distributions);
  }
}

class Distribution {
  final int id;
  final Hospital hospital;
  final String sender;
  final String receiver;

  Distribution(this.id, this.hospital, this.sender, this.receiver);

  factory Distribution.fromJson(dynamic json) {
    return Distribution(json['id'] as int, Hospital.fromJson(json['hospital']),
        json['sender'] as String, json['receiver'] as String);
  }
}
