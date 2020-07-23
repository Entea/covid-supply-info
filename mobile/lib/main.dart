import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:tirek_mobile/services/AuthenticationService.dart';
import 'package:tirek_mobile/pages/RootPage.dart';
import 'package:tirek_mobile/pages/HomePage.dart';
import 'package:tirek_mobile/pages/NeedsPage.dart';
import 'package:tirek_mobile/services/DonationService.dart';
import 'package:tirek_mobile/services/DistributionsService.dart';
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
    HospitalService tirekHospitalService = new TirekHospitalService(sharedPreferencesService);
    DonationService tirekDonationService = new TirekDonationService();
    AuthenticationService tirekAuthenticationService = new TirekAuthenticationService();
    LogoutService tirekLogoutService = new TirekLogoutService(sharedPreferencesService);
    DistributionsService tirekDistributionsService = new TirekDistributionsService(sharedPreferencesService);

    Widget rootPage = new RootPage(
      sharedPreferencesService: sharedPreferencesService,
      authenticationService: tirekAuthenticationService
    );

    Widget homePage = new HomePage(
      hospitalService: tirekHospitalService,
      logoutService: tirekLogoutService,
      sharedPreferencesService: sharedPreferencesService,
      distributionsService: tirekDistributionsService,
    );

    Widget needsPage = new NeedsPage(
      hospitalService: tirekHospitalService,
      donationService: tirekDonationService,
    );

    Widget _defaultPage = rootPage;

    void setDefaultPage() async {
      final isLoggedIn = await sharedPreferencesService.isLoggedIn();
      _defaultPage = isLoggedIn ? homePage : rootPage;
    }

    setDefaultPage();

    return new MaterialApp(
      title: 'Tirek Application',
      home: _defaultPage,
      localizationsDelegates: [
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
      ],
      supportedLocales: [
        const Locale('ru', 'RU'),
      ],
      routes: {
        '/login': (context) => rootPage,
        '/home': (context) => homePage,
        '/needs': (context) => needsPage
      },
      debugShowCheckedModeBanner: false,
      theme: new ThemeData(
          primarySwatch: Colors.blue,
          inputDecorationTheme: const InputDecorationTheme(
            filled: true,
            labelStyle: TextStyle(color: Colors.black),
            hintStyle: TextStyle(color: Colors.grey),
            enabledBorder: UnderlineInputBorder(
              borderSide: BorderSide(color: Color.fromARGB(0, 0, 0, 0)),
            ),
            focusedBorder: UnderlineInputBorder(
              borderSide: BorderSide(color: Color.fromARGB(38, 0, 0, 0)),
            ),
            border: UnderlineInputBorder(
              borderSide: BorderSide(color: Color.fromARGB(38, 0, 0, 0)),
            ),
          )),
    );
  }
}
