import 'dart:async';
import 'package:tirek_mobile/helper/ApiHelper.dart';
import 'package:tirek_mobile/models/response/LogoutResponse.dart';
import 'package:tirek_mobile/services/SharedPreferencesService.dart';
import 'dart:convert';

abstract class LogoutService {
  Future<LogoutResponse> logout();
}

class TirekLogoutService implements LogoutService {
  final SharedPreferencesService sharedPreferencesService;

  TirekLogoutService(this.sharedPreferencesService);

  @override
  Future<LogoutResponse> logout() async {
    final userInfo = await sharedPreferencesService.getCurrentUserInfo();
    final body = json.encode({});

    final Map<String, String> headers = {
      'Authorization': "Token ${userInfo.token}",
      'Content-Type': 'application/json; charset=utf-8',
      'Accept': 'application/json',
    };

    await ApiHelper.post("logout/", headers, body);
    await sharedPreferencesService.removeCurrentUserInfo();
  }
}
