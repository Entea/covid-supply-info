import 'package:tirek_mobile/helper/ApiHelper.dart';
import 'package:tirek_mobile/models/response/DonationResponse.dart';

abstract class DonationService {
  Future<DonationResponse> get();
}

class TirekDonationService extends DonationService {
  @override
  Future<DonationResponse> get() async {
    final Map<String, String> headers = {
      'Content-Type': 'application/json; charset=utf-8',
      'Accept': 'application/json',
    };

    final responseJson = await ApiHelper.get("donations/", headers);

    return DonationResponse.fromJson(responseJson);
  }
}
