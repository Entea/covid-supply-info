import 'package:flutter/material.dart';
import 'package:tirek_mobile/exception/TirekException.dart';
import 'package:tirek_mobile/models/response/HospitalResponse.dart';
import 'package:tirek_mobile/services/HospitalService.dart';

class HomePage extends StatefulWidget {
  HomePage({this.hospitalService});

  final HospitalService hospitalService;

  @override
  State<StatefulWidget> createState() => new _HomePageState();
}

class _HomePageState extends State<HomePage> {
  HospitalResponse _data;
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
        _data = response;
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
        drawer: new Drawer(),
        floatingActionButton: FloatingActionButton(
          onPressed: getData,
          child: Icon(Icons.add),
        ),
        body: TabBarView(
          children: [
            new ListView.builder(
              itemCount: _data.hospitals.length,
                itemBuilder: (BuildContext ctxt, int index) {
                  return new ListTile(
                    title: new Text(_data.hospitals[index].name),
                    subtitle: new Text('КОД ' + _data.hospitals[index].code),
                    trailing: Icon(Icons.add),
                  );
                }
            ),
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
