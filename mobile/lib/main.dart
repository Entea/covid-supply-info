import 'package:flutter/material.dart';
import 'package:tirek_mobile/services/AuthenticationService.dart';
import 'package:tirek_mobile/pages/RootPage.dart';
import 'package:tirek_mobile/pages/HomePage.dart';
import 'package:tirek_mobile/services/HospitalService.dart';
import 'package:tirek_mobile/services/TokenService.dart';

void main() {
  runApp(new TirekApplication());
}

class TirekApplication extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return new MaterialApp(
        title: 'Tirek Application',
        initialRoute: '/',
        routes: {
          '/': (context) => new RootPage(
              tokenService: new TokenService(),
              authenticationService: new TirekAuthenticationService()
          ),
          '/home': (context) => new HomePage(
            hospitalService: new TirekHospitalService(new TokenService()),
          )
        },
        debugShowCheckedModeBanner: false,
        theme: new ThemeData(
          primarySwatch: Colors.blue,
        ));
  }
}
