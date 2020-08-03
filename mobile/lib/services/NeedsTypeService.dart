import 'dart:async';
import 'package:tirek_mobile/helper/ApiHelper.dart';

import 'package:tirek_mobile/models/response/NeedsTypeResponse.dart';
import 'package:tirek_mobile/services/SharedPreferencesService.dart';

abstract class NeedsTypeService {
  Future<NeedsTypeResponse> get();
}

class TirekNeedsTypeService implements NeedsTypeService {
  final SharedPreferencesService sharedPreferencesService;

  TirekNeedsTypeService(this.sharedPreferencesService);

  @override
  Future<NeedsTypeResponse> get() async {
    final userInfo = await sharedPreferencesService.getCurrentUserInfo();

    final Map<String, String> headers = {
      'Authorization': "Token ${userInfo.token}",
      'Content-Type': 'application/json; charset=utf-8',
      'Accept': 'application/json; charset=utf-8',
    };

    final responseJson = await ApiHelper.get("need-types/", headers);

    return NeedsTypeResponse.fromJson(responseJson);
  }
}
