import 'dart:async';
import 'package:tirek_mobile/helper/ApiHelper.dart';
import 'package:tirek_mobile/models/response/AuthenticationResponse.dart';
import 'dart:convert';

abstract class AuthenticationService {
  Future<AuthenticationResponse> login(String username, String password);
}

class TirekAuthenticationService implements AuthenticationService {
  @override
  Future<AuthenticationResponse> login(String username, String password) async {
    final body = json.encode({"username": username, "password": password});

    final Map<String, String> headers = {
      'Content-Type': 'application/json; charset=utf-8',
      'Accept': 'application/json',
    };

    final responseJson = await ApiHelper.post("auth/login/", headers, body);

    return AuthenticationResponse.fromJson(responseJson);
  }
}
