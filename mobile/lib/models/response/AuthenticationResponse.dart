import 'User.dart';

class AuthenticationResponse {
  final String token;
  final User user;

  AuthenticationResponse(this.token, this.user);

  factory AuthenticationResponse.fromJson(dynamic json) {
    var userJson = json['user'] as dynamic;
    var user = User.fromJson(userJson);
    return AuthenticationResponse(json['token'] as String, user);
  }
}
