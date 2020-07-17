import 'package:shared_preferences/shared_preferences.dart';
import 'package:tirek_mobile/models/response/AuthenticationResponse.dart';
import 'package:tirek_mobile/models/response/User.dart';

abstract class SharedPreferencesService {
  saveAuthenticationResponse(AuthenticationResponse authenticationResponse);

  Future<AuthenticationResponse> getCurrentUserInfo();

  removeCurrentUserInfo();
}

class TirekSharedPreferencesService implements SharedPreferencesService {
  @override
  saveAuthenticationResponse(
      AuthenticationResponse authenticationResponse) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();

    await prefs.setString('token', authenticationResponse.token);
    await prefs.setInt('userId', authenticationResponse.user.id);
    await prefs.setString('userFullName', authenticationResponse.user.fullName);
  }

  @override
  Future<AuthenticationResponse> getCurrentUserInfo() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('token');
    final userId = prefs.getInt('userId');
    final fullName = prefs.getString('userFullName');

    return AuthenticationResponse(token, User(userId, fullName));
  }

  @override
  removeCurrentUserInfo() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.remove('token');
    await prefs.remove('userId');
    await prefs.remove('userFullName');
  }
}
