class NeedsResponse {
  final int count;

  final List<NeedType> needs;

  NeedsResponse(this.count, this.needs);

  factory NeedsResponse.fromJson(dynamic json) {
    var results = json['results'] as dynamic;
    var needs = <NeedType>[];
    for (var result in results) {
      var need = NeedType.fromJson(result);
      needs.add(need);
    }
    return NeedsResponse(json['count'] as int, needs);
  }
}

class NeedType {
  final int id;
  final String name;

  NeedType(this.id, this.name);

  factory NeedType.fromJson(dynamic json) {
    return NeedType(json['id'] as int, json['name'] as String);
  }
}
