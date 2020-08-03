import 'dart:async';
import 'package:tirek_mobile/helper/ApiHelper.dart';

import 'package:tirek_mobile/models/response/NeedsRequestResponse.dart';
import 'package:tirek_mobile/models/response/NeedsTypeResponse.dart';
import 'package:tirek_mobile/services/SharedPreferencesService.dart';
import 'package:tirek_mobile/models/response/HospitalResponse.dart';
import 'dart:convert';

abstract class NeedsRequestService {
  Future<NeedsRequestResponse> post(Hospital hospital, NeedsType needType,
      String reserveAmount, String requestAmount, String requestAmountMonth);
}

class TirekNeedsRequestService implements NeedsRequestService {
  final SharedPreferencesService sharedPreferencesService;

  TirekNeedsRequestService(this.sharedPreferencesService);

  @override
  Future<NeedsRequestResponse> post(
      Hospital hospital,
      NeedsType needType,
      String reserveAmount,
      String requestAmount,
      String requestAmountMonth) async {
    final userInfo = await sharedPreferencesService.getCurrentUserInfo();

    final body = json.encode({
      "hospital_id": hospital.id,
      "need_type_id": needType.id,
      "reserve_amount": reserveAmount,
      "request_amount": requestAmount,
      "request_amount_month": requestAmountMonth
    });

    final Map<String, String> headers = {
      'Authorization': "Token ${userInfo.token}",
      'Content-Type': 'application/json; charset=utf-8',
      'Accept': 'application/json; charset=utf-8',
    };

    final responseJson = await ApiHelper.post("hospital-needs/", headers, body);
    return NeedsRequestResponse.fromJson(responseJson);
  }
}
