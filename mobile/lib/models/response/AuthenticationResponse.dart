class AuthenticationResponse {
  final String token;

  AuthenticationResponse(this.token);

  factory AuthenticationResponse.fromJson(dynamic json) {
    return AuthenticationResponse(json['token'] as String);
  }
}
