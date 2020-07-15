import 'package:flutter/material.dart';
import 'package:tirek_mobile/pages/LoginPage.dart';
import 'package:tirek_mobile/services/AuthenticationService.dart';
import 'package:tirek_mobile/services/TokenService.dart';

enum AuthStatus {
  NOT_DETERMINED,
  NOT_LOGGED_IN,
  LOGGED_IN,
}

class RootPage extends StatefulWidget {
  RootPage({this.tokenService, this.authenticationService});

  final TokenService tokenService;
  final AuthenticationService authenticationService;

  @override
  State<StatefulWidget> createState() => new _RootPageState();
}

class _RootPageState extends State<RootPage> {
  AuthStatus authStatus = AuthStatus.NOT_DETERMINED;

  @override
  void initState() {
    super.initState();
//    widget.auth.getCurrentUser().then((user) {
//      setState(() {
//        if (user != null) {
//          _userId = user?.uid;
//        }
//        authStatus =
//            user?.uid == null ? AuthStatus.NOT_LOGGED_IN : AuthStatus.LOGGED_IN;
//      });
//    });
  }

  void loginCallback() {
//    widget.auth.getCurrentUser().then((user) {
//      setState(() {
//        _userId = user.uid.toString();
//      });
//    });
//    setState(() {
//      authStatus = AuthStatus.LOGGED_IN;
//    });
  }

  void logoutCallback() {
    setState(() {
      authStatus = AuthStatus.NOT_LOGGED_IN;
    });
  }

  Widget buildWaitingScreen() {
    return Scaffold(
      body: Container(
        alignment: Alignment.center,
        child: CircularProgressIndicator(),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return new LoginPage(
      authenticationService: widget.authenticationService,
      tokenService: widget.tokenService,
      loginCallback: loginCallback,
    );
  }
}
