import 'dart:async';
import 'package:tirek_mobile/helper/ApiHelper.dart';
import 'package:tirek_mobile/models/response/LogoutResponse.dart';
import 'package:tirek_mobile/services/TokenService.dart';
import 'dart:convert';

abstract class LogoutService {
  Future<LogoutResponse> logout();
}

class TirekLogoutService implements LogoutService {
  final TokenService tokenService;

  TirekLogoutService(this.tokenService);

  @override
  Future<LogoutResponse> logout() async {
    final token = await tokenService.get();
    final body = json.encode({});

    final Map<String, String> headers = {
      'Authorization': "Token $token",
      'Content-Type': 'application/json; charset=utf-8',
      'Accept': 'application/json',
    };

    final responseJson = await ApiHelper.post("logout/", headers, body);

    await tokenService.remove();

    return LogoutResponse.fromJson(responseJson);
  }
}
