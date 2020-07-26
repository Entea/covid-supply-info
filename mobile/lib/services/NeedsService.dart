import 'dart:async';
import 'package:tirek_mobile/helper/ApiHelper.dart';

import 'package:tirek_mobile/models/response/NeedsResponse.dart';
import 'package:tirek_mobile/services/SharedPreferencesService.dart';

abstract class NeedsService {
  Future<NeedsResponse> get();
}

class TirekNeedsService implements NeedsService {
  final SharedPreferencesService sharedPreferencesService;

  TirekNeedsService(this.sharedPreferencesService);

  @override
  Future<NeedsResponse> get() async {
    final userInfo = await sharedPreferencesService.getCurrentUserInfo();

    final Map<String, String> headers = {
      'Authorization': "Token ${userInfo.token}",
      'Content-Type': 'application/json; charset=utf-8',
      'Accept': 'application/json; charset=utf-8',
    };

    final responseJson = await ApiHelper.get("hospital-needs/", headers);

    return NeedsResponse.fromJson(responseJson);
  }
}
