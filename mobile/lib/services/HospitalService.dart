import 'dart:async';
import 'package:tirek_mobile/helper/ApiHelper.dart';

import 'package:tirek_mobile/models/response/HospitalResponse.dart';
import 'package:tirek_mobile/services/TokenService.dart';

abstract class HospitalService {
  Future<HospitalResponse> get();
}

class TirekHospitalService implements HospitalService {
  final TokenService tokenService;

  TirekHospitalService(this.tokenService);

  @override
  Future<HospitalResponse> get() async {
    final token = await tokenService.get();

    final Map<String, String> headers = {
      'Authorization': "Token $token",
      'Content-Type': 'application/json; charset=utf-8',
      'Accept': 'application/json; charset=utf-8',
    };

    final responseJson = await ApiHelper.get("managers/hospitals/", headers);

    return HospitalResponse.fromJson(responseJson);
  }
}
