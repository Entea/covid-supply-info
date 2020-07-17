import 'dart:async';
import 'package:tirek_mobile/helper/ApiHelper.dart';

import 'package:tirek_mobile/models/response/HospitalResponse.dart';
import 'package:tirek_mobile/services/SharedPreferencesService.dart';

abstract class HospitalService {
  Future<HospitalResponse> get();
}

class TirekHospitalService implements HospitalService {
  final SharedPreferencesService sharedPreferencesService;

  TirekHospitalService(this.sharedPreferencesService);

  @override
  Future<HospitalResponse> get() async {
    final userInfo = await sharedPreferencesService.getCurrentUserInfo();

    final Map<String, String> headers = {
      'Authorization': "Token ${userInfo.token}",
      'Content-Type': 'application/json; charset=utf-8',
      'Accept': 'application/json; charset=utf-8',
    };

    final responseJson = await ApiHelper.get("managers/hospitals/", headers);

    return HospitalResponse.fromJson(responseJson);
  }
}
