import 'package:flutter/material.dart';
import 'package:tirek_mobile/exception/TirekException.dart';
import 'package:tirek_mobile/services/HospitalService.dart';
import 'package:tirek_mobile/services/LogoutService.dart';
import 'package:tirek_mobile/services/SharedPreferencesService.dart';

class HomePage extends StatefulWidget {
  HomePage(
      {this.hospitalService,
      this.logoutService,
      this.sharedPreferencesService});

  final HospitalService hospitalService;
  final LogoutService logoutService;
  final SharedPreferencesService sharedPreferencesService;

  @override
  State<StatefulWidget> createState() => new _HomePageState();
}

class _HomePageState extends State<HomePage>
    with SingleTickerProviderStateMixin {
  List _data = [];
  String _errorMessage;
  bool _isLoading;
  String userName = '';

  final List<Tab> myTabs = <Tab>[
    Tab(text: 'Больницы'),
    Tab(text: 'Распределение'),
  ];

  TabController _tabController;

  @override
  void initState() {
    _errorMessage = "";
    _isLoading = false;
    _tabController = new TabController(length: myTabs.length, vsync: this);

    super.initState();
    getData();
  }

  void getData() async {
    try {
      final response = await widget.hospitalService.get();
      final user = await widget.sharedPreferencesService.getCurrentUserInfo();

      setState(() {
        _data = response.hospitals;
        userName = user.user.fullName;
      });
    } on TirekException {
      setState(() {
        _isLoading = false;
        _errorMessage = "Произошла ошибка при подключении";
      });
    }
  }

  void logout() async {
    Navigator.pushNamedAndRemoveUntil(context, '/', (r) => false);

    try {
      await widget.logoutService.logout();
    } on TirekException {
      setState(() {
        _isLoading = false;
        _errorMessage = "Произошла ошибка";
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
            controller: _tabController,
            tabs: myTabs,
          ),
        ),
        drawer: Theme(
          data: Theme.of(context).copyWith(canvasColor: Colors.blue),
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
                              userName,
                              style:
                                  TextStyle(color: Colors.white, fontSize: 24),
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
                      title: Text('Больницы',
                          style: TextStyle(
                            color: Colors.white,
                          )),
                      onTap: () {
                        Navigator.of(context).pop();
                        _tabController.animateTo((0));
                      },
                    ),
                    ListTile(
                        title: Text('Распределение',
                            style: TextStyle(
                              color: Colors.white,
                            )),
                        onTap: () {
                          Navigator.of(context).pop();
                          _tabController.animateTo((1));
                        }),
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
                        ),
                      ),
                      onTap: logout,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
        body: TabBarView(
          controller: _tabController,
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
