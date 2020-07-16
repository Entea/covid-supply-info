import 'package:flutter/material.dart';
import 'package:tirek_mobile/services/AuthenticationService.dart';
import 'package:tirek_mobile/pages/RootPage.dart';
import 'package:tirek_mobile/services/TokenService.dart';

void main() {
  runApp(new TirekApplication());
}

class TirekApplication extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return new MaterialApp(
        title: 'Tirek Application',
        debugShowCheckedModeBanner: false,
        theme: new ThemeData(
          primarySwatch: Colors.teal,
        ),
        home: new RootPage(
            tokenService: new TokenService(),
            authenticationService: new TirekAuthenticationService()));
  }
}
