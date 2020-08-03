class NeedsResponse {
  final int count;

  final List<NeedsItem> needs;

  NeedsResponse(this.count, this.needs);

  factory NeedsResponse.fromJson(dynamic json) {
    var results = json['results'] as dynamic;

    var needs = <NeedsItem>[];
    for (var result in results) {
      var need = NeedsItem.fromJson(result);
      needs.add(need);
    }
    return NeedsResponse(json['count'] as int, needs);
  }
}

class NeedsItem {
  final String need_type;
  final Object hospital;
  final int reserve_amount;
  final int request_amount;
  final String created_at;

  NeedsItem(this.need_type, this.hospital, this.request_amount, this.reserve_amount, this.created_at);

  factory NeedsItem.fromJson(dynamic json) {
    return NeedsItem(json['need_type']['name'] as String, json['hospital'] as Object, json['request_amount'] as int, json['reserve_amount'] as int, json['created_at'] as String);
  }
}
