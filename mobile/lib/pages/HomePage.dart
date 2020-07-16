import 'package:flutter/material.dart';
import 'package:tirek_mobile/services/AuthenticationService.dart';
import 'package:tirek_mobile/services/TokenService.dart';

class HomePage extends StatefulWidget {
  HomePage();
  State<StatefulWidget> createState() => new _HomePageState();
}

class _HomePageState extends State<HomePage> {
  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 2,
      child: new Scaffold(
        appBar: new AppBar(
          title: new Text('Tirek'),
          bottom: TabBar(
            tabs: [
              Tab(text: 'Больницы'),
              Tab(text: 'Распределение'),
            ],
          ),
        ),
        drawer: new Drawer(),
        floatingActionButton: FloatingActionButton(
          onPressed: () {
          },
          child: Icon(Icons.add),
        ),
        body: TabBarView(
          children: [
            new ListView(
              children: <Widget>[
                ListTile(
                  title: new Text('ОШСКИЙ МЕДИЦИНСКИЙ КОЛ...'),
                  subtitle: new Text('КОД 9040'),
                ),
                ListTile(
                  title: new Text('ОШСКИЙ МЕДИЦИНСКИЙ КОЛ...'),
                  subtitle: new Text('КОД 9040'),
                )
              ],
            ),
            new ListView(
              padding: const EdgeInsets.only(
                  top: 10,
                  bottom: 15
              ),
              children: <Widget>[
                ListTile(
                  title: new Text('Ошская Медицинский Колледж'),
                  subtitle: new Text('Народный штаб Биз Барбыз. Сообщество Кыргызстанцев в США в лице Айзада Марат...'),
                ),
                ListTile(
                  title: new Text('Ошская Медицинский Колледж'),
                  subtitle: new Text('Народный штаб Биз Барбыз. Сообщество Кыргызстанцев в США в лице Айзада Марат...'),
                )
              ],
            ),
          ],
        ),
      ),
    );
  }
}
