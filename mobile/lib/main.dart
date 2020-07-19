import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:tirek_mobile/services/AuthenticationService.dart';
import 'package:tirek_mobile/pages/RootPage.dart';
import 'package:tirek_mobile/pages/HomePage.dart';
import 'package:tirek_mobile/pages/NeedsPage.dart';
import 'package:tirek_mobile/services/DonationService.dart';
import 'package:tirek_mobile/services/HospitalService.dart';
import 'package:tirek_mobile/services/LogoutService.dart';
import 'package:tirek_mobile/services/SharedPreferencesService.dart';

void main() {
  runApp(new TirekApplication());
}

class TirekApplication extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    var sharedPreferencesService = new TirekSharedPreferencesService();
    var tirekHospitalService =
        new TirekHospitalService(sharedPreferencesService);
    var tirekDonationService = new TirekDonationService();

    return new MaterialApp(
      title: 'Tirek Application',
      initialRoute: '/',
      localizationsDelegates: [
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
      ],
      supportedLocales: [
        const Locale('ru', 'RU'),
      ],
      routes: {
        '/': (context) => new RootPage(
            sharedPreferencesService: sharedPreferencesService,
            authenticationService: new TirekAuthenticationService()),
        '/home': (context) => new HomePage(
              hospitalService: tirekHospitalService,
              logoutService: new TirekLogoutService(sharedPreferencesService),
              donationService: tirekDonationService,
            ),
        '/needs': (context) {
          return new NeedsPage(
            hospitalService: tirekHospitalService,
            donationService: tirekDonationService,
          );
        }
      },
      debugShowCheckedModeBanner: false,
      theme: new ThemeData(
        primarySwatch: Colors.blue,
      ),
    );
  }
}
