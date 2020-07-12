import 'package:flutter/material.dart';
import 'package:tirek_mobile/services/authentication.dart';
import 'package:tirek_mobile/pages/root_page.dart';

void main() {
  runApp(new MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return new MaterialApp(
        title: 'Flutter login demo',
        debugShowCheckedModeBanner: false,
        theme: new ThemeData(
          primarySwatch: Colors.teal,
        ),
        home: new RootPage(auth: new Auth()));
  }
}
