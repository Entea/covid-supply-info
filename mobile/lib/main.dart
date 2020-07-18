import 'package:flutter/material.dart';
import 'package:tirek_mobile/services/AuthenticationService.dart';
import 'package:tirek_mobile/pages/RootPage.dart';
import 'package:tirek_mobile/pages/HomePage.dart';
import 'package:tirek_mobile/pages/NeedsPage.dart';
import 'package:tirek_mobile/services/HospitalService.dart';
import 'package:tirek_mobile/services/LogoutService.dart';
import 'package:tirek_mobile/services/SharedPreferencesService.dart';

void main() {
  runApp(new TirekApplication());
}

class TirekApplication extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    SharedPreferencesService sharedPreferencesService = new TirekSharedPreferencesService();

    return new MaterialApp(
        title: 'Tirek Application',
        initialRoute: '/',
        routes: {
          '/': (context) => new RootPage(
              sharedPreferencesService: sharedPreferencesService,
              authenticationService: new TirekAuthenticationService()),
          '/home': (context) => new HomePage(
                hospitalService: new TirekHospitalService(sharedPreferencesService),
                logoutService: new TirekLogoutService(sharedPreferencesService),
              ),
          '/needs': (context) => new NeedsPage()
        },
        debugShowCheckedModeBanner: false,
        theme: new ThemeData(
          primarySwatch: Colors.blue,
        ));
  }
}
