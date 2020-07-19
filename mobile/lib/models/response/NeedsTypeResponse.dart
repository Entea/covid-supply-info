import 'Measure.dart';

class NeedsTypeResponse {
  final int count;

  final List<NeedsType> needsTypes;

  NeedsTypeResponse(this.count, this.needsTypes);

  factory NeedsTypeResponse.fromJson(dynamic json) {
    var results = json['results'] as dynamic;
    var needsTypes = <NeedsType>[];
    for (var result in results) {
      var needsType = NeedsType.fromJson(result);
      needsTypes.add(needsType);
    }
    return NeedsTypeResponse(json['count'] as int, needsTypes);
  }
}

class NeedsType {
  final int id;
  final String name;
  final Measure measure;

  NeedsType(this.id, this.name, this.measure);

  factory NeedsType.fromJson(dynamic json) {
    var measureJson = json['measure'] as dynamic;
    var measure = Measure.fromJson(measureJson);
    return NeedsType(json['id'] as int, json['name'] as String, measure);
  }
}
