import 'package:tirek_mobile/helper/ApiHelper.dart';
import 'package:tirek_mobile/models/response/DistributionResponse.dart';

import 'SharedPreferencesService.dart';

abstract class DistributionsService {
  Future<DistributionResponse> getManagerDistributions();
}

class TirekDistributionsService extends DistributionsService {
  final SharedPreferencesService sharedPreferencesService;

  TirekDistributionsService(this.sharedPreferencesService);

  @override
  Future<DistributionResponse> getManagerDistributions() async {
    final userInfo = await sharedPreferencesService.getCurrentUserInfo();

    final Map<String, String> headers = {
      'Authorization': "Token ${userInfo.token}",
      'Content-Type': 'application/json; charset=utf-8',
      'Accept': 'application/json; charset=utf-8',
    };

    final responseJson =
        await ApiHelper.get("managers/distributions/", headers);

    return DistributionResponse.fromJson(responseJson);
  }
}
