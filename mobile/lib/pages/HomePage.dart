import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:tirek_mobile/exception/TirekException.dart';
import 'package:tirek_mobile/services/DistributionsService.dart';
import 'package:tirek_mobile/services/HospitalService.dart';
import 'package:tirek_mobile/services/LogoutService.dart';
import 'package:tirek_mobile/services/SharedPreferencesService.dart';
import 'package:flutter_speed_dial/flutter_speed_dial.dart';

class HomePage extends StatefulWidget {
  HomePage(
      {this.hospitalService,
      this.logoutService,
      this.sharedPreferencesService,
      this.distributionsService});

  final HospitalService hospitalService;
  final LogoutService logoutService;
  final SharedPreferencesService sharedPreferencesService;
  final DistributionsService distributionsService;

  @override
  State<StatefulWidget> createState() => new _HomePageState();
}

class _HomePageState extends State<HomePage>
    with SingleTickerProviderStateMixin {
  List _hospitals = [];
  List _distributions = [];
  String _errorMessage;
  bool _isLoading;
  String _userName = '';

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
    fetchData();
  }

  void fetchData() async {
    setState(() {
      _errorMessage = "";
      _isLoading = true;
    });

    try {
      final hospitalResponse = await widget.hospitalService.get();
      final user = await widget.sharedPreferencesService.getCurrentUserInfo();
      final distributionResponse =
          await widget.distributionsService.getManagerDistributions();

      setState(() {
        _hospitals = hospitalResponse.hospitals;
        _distributions = distributionResponse.distributions;
        _userName = user.user.fullName;
        _isLoading = false;
      });
    } on TirekException {
      setState(() {
        _isLoading = false;
        _errorMessage = "Произошла ошибка при подключении";
      });
    } finally {
      setState(() {
        _isLoading = false;
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
    SharedPreferencesService sharedPreferencesService =
        new TirekSharedPreferencesService();

    return DefaultTabController(
      length: 2,
      child: new Scaffold(
        backgroundColor: Colors.white,
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
                              _userName,
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
        body: Stack(children: <Widget>[
          TabBarView(
            controller: _tabController,
            children: [
              new ListView.builder(
                  itemCount: _hospitals.length,
                  itemBuilder: (BuildContext ctxt, int index) {
                    return new ListTile(
                      title: new Text(_hospitals[index].name),
                      subtitle: new Text('КОД ' + _hospitals[index].code),
                      trailing: Icon(Icons.add),
                    );
                  }),
              new ListView.builder(
                  itemCount: _distributions.length,
                  itemBuilder: (BuildContext ctxt, int index) {
                    return new ListTile(
                      title: new Text(_distributions[index].hospital.name),
                      subtitle: new Text(_distributions[index].sender),
                    );
                  }),
            ],
          ),
          _showCircularProgress()
        ]),
        floatingActionButton: SpeedDial(
          overlayColor: Color.fromARGB(35, 0, 0, 0),
          animatedIcon: AnimatedIcons.menu_close,
          children: [
            SpeedDialChild(
                child: Icon(Icons.add_shopping_cart),
                label: 'Добавить пожертвование',
                backgroundColor: Colors.green),
            SpeedDialChild(
                child: Icon(Icons.add),
                label: 'Добавить больницу',
                backgroundColor: Colors.green),
            SpeedDialChild(
                child: Icon(Icons.note_add),
                label: 'Добавить потребности больниц',
                onTap: () {
                  Navigator.pushNamed(context, '/needs-create');
                },
                backgroundColor: Colors.green),
          ],
        ),
      ),
    );
  }

  Widget _showCircularProgress() {
    if (_isLoading) {
      return Center(child: CircularProgressIndicator());
    }
    return Container(
      height: 0.0,
      width: 0.0,
    );
  }
}
