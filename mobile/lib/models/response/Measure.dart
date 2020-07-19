class Measure {
  final int id;
  final String name;

  Measure(this.id, this.name);

  factory Measure.fromJson(dynamic json) {
    return Measure(json['id'] as int, json['name'] as String);
  }
}
