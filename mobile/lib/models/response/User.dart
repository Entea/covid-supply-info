class User {
  final int id;
  final String fullName;

  User(this.id, this.fullName);

  factory User.fromJson(dynamic json) {
    return User(json['id'] as int, json['full_name'] as String);
  }
}
