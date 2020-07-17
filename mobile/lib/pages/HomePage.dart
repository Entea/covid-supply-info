import 'package:flutter/material.dart';
import 'package:tirek_mobile/exception/TirekException.dart';
import 'package:tirek_mobile/services/HospitalService.dart';

class HomePage extends StatefulWidget {
  HomePage({this.hospitalService});

  final HospitalService hospitalService;

  @override
  State<StatefulWidget> createState() => new _HomePageState();
}

class _HomePageState extends State<HomePage> {
  List _data = [];
  String _errorMessage;
  bool _isLoading;

  @override
  void initState() {
    _errorMessage = "";
    _isLoading = false;
    super.initState();
    getData();
  }

  void getData() async {
    try {
      final response = await widget.hospitalService.get();
      setState(() {
        _data = response.hospitals;
      });
    } on TirekException {
      setState(() {
        _isLoading = false;
        _errorMessage = "Произошла ошибка при подключении";
      });
    }
  }

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
        drawer: Theme(
          data: Theme.of(context).copyWith(
            canvasColor: Colors.blue
          ),
          child: Drawer(
            child: Column(
              mainAxisSize: MainAxisSize.max,
              children: <Widget>[
                DrawerHeader(
                  child: new Container(
                    child: new Column(
                      mainAxisSize: MainAxisSize.max,
                      children: [
                        new Container(
                          child: Align(
                            alignment: Alignment.topLeft,
                            child: new Image.asset(
                              'assets/logo.png',
                              height: 38.0,
                            ),
                          ),
                        ),
                        Expanded(
                          child: Align(
                            alignment: Alignment.bottomLeft,
                            child: Text(
                              'Андрей Волконский',
                              style: TextStyle(
                                  color: Colors.white,
                                  fontSize: 24
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                ListView(
                  scrollDirection: Axis.vertical,
                  shrinkWrap: true,
                  padding: EdgeInsets.zero,
                  children: <Widget>[
                    ListTile(
                      title: Text(
                          'Больницы',
                          style: TextStyle(
                            color: Colors.white,
                          )
                      ),
                    ),
                    ListTile(
                      title: Text('Распределение',
                          style: TextStyle(
                            color: Colors.white,
                          )
                      ),
                    ),
                  ],
                ),
                Expanded(
                  child: Align(
                    alignment: Alignment.bottomCenter,
                    child: ListTile(
                      title: Text(
                          'Выйти из приложения',
                          style: TextStyle(
                            color: Colors.white,
                          )
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
        body: TabBarView(
          children: [
            new ListView.builder(
                itemCount: _data.length,
                itemBuilder: (BuildContext ctxt, int index) {
                  return new ListTile(
                    title: new Text(_data[index].name),
                    subtitle: new Text('КОД ' + _data[index].code),
                    trailing: Icon(Icons.add),
                  );
                }),
            new ListView(
              padding: const EdgeInsets.only(top: 10, bottom: 15),
              children: <Widget>[
                ListTile(
                  title: new Text('Ошская Медицинский Колледж'),
                  subtitle: new Text(
                      'Народный штаб Биз Барбыз. Сообщество Кыргызстанцев в США в лице Айзада Марат...'),
                ),
                ListTile(
                  title: new Text('Ошская Медицинский Колледж'),
                  subtitle: new Text(
                      'Народный штаб Биз Барбыз. Сообщество Кыргызстанцев в США в лице Айзада Марат...'),
                )
              ],
            ),
          ],
        ),
      ),
    );
  }
}
