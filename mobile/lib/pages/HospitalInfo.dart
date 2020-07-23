import 'package:flutter/material.dart';
import 'package:tirek_mobile/models/response/HospitalResponse.dart';

class HospitalInfoPage extends StatefulWidget {
  HospitalInfoPage({this.hospital});

  Hospital hospital;

  @override
  State<StatefulWidget> createState() => _HospitalInfoPage();
}

class _HospitalInfoPage extends State<HospitalInfoPage> {
  DateTime selectedDate = DateTime.now();
  String _name = 'Hospital Name';
  String _address = 'address';

  @override
  void initState() {
    super.initState();
    print(widget.hospital.indicator);
    setState(() {
      _name = widget.hospital.name;
      _address = widget.hospital.address;
    });
  }

  Future<void> _selectDate(BuildContext context) async {
    final DateTime picked = await showDatePicker(
        fieldLabelText: 'Выберите дату',
        fieldHintText: 'Выберите дату',
        helpText: 'Выберите дату',
        context: context,
        initialDate: selectedDate,
        firstDate: DateTime(2015, 8),
        lastDate: DateTime(2101));
    if (picked != null && picked != selectedDate)
      setState(() {
        selectedDate = picked;
      });
  }

  Widget build(BuildContext widget) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: Text('Назад'),
      ),
      body: Stack(
        children: <Widget>[
          SingleChildScrollView(
            child: Padding(
              padding: EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: <Widget>[
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: <Widget>[
                      Text('Данные больницы'),
                      FlatButton(
                        padding: EdgeInsets.all(0),
                        onPressed: () {},
                        child: Row(
                          children: <Widget>[
                            Padding(
                              padding: EdgeInsets.fromLTRB(0, 0, 5, 0),
                              child: Text(
                                'Изменить',
                                style: TextStyle(color: Colors.blue),
                              ),
                            ),
                            Icon(
                              Icons.edit,
                              size: 14,
                              color: Colors.blue,
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                  Padding(
                    padding: EdgeInsets.only(bottom: 16),
                    child: Text(_name, style: TextStyle(fontSize: 24),)
                  ),
                  Padding(
                    padding: EdgeInsets.only(bottom: 20),
                    child: Row(
                      children: <Widget>[
                        Padding(
                          padding: EdgeInsets.fromLTRB(0, 0, 18, 0),
                          child: Icon(Icons.navigation,
                              color: Colors.blue, size: 16),
                        ),
                        Text('asd', style: TextStyle(color: Color.fromARGB(153, 0, 0, 0)))
                      ],
                    ),
                  ),
                  Padding(
                    padding: EdgeInsets.only(bottom: 20),
                    child: Row(
                      children: <Widget>[
                        Padding(
                          padding: EdgeInsets.fromLTRB(0, 0, 18, 0),
                          child:
                              Icon(Icons.phone, color: Colors.green, size: 16),
                        ),
                        Text('0312571092',
                            style:
                                TextStyle(color: Color.fromARGB(153, 0, 0, 0)))
                      ],
                    ),
                  ),
                  Row(
                    children: <Widget>[
                      Text('Таблица данных за:',
                          style: TextStyle(fontSize: 16)),
                      FlatButton(
                        child: Row(
                          children: <Widget>[
                            Text(
                                "${selectedDate.year.toString()}-${selectedDate.month.toString().padLeft(2,'0')}-${selectedDate.day.toString().padLeft(2,'0')}",
                                style: TextStyle(fontSize: 16)
                            ),
                            Icon(Icons.arrow_drop_down)
                          ],
                        ),
                        onPressed: () {
                          _selectDate(context);
                        },
                      )
                    ],
                  ),
                  DataTable(
                    columns: [
                      DataColumn(
                        label:Text('Название'),
                        numeric: false
                      ),
                      DataColumn(
                        label:Text('Наличие'),
                        numeric: true
                      ),
                      DataColumn(
                        label:Text('Требуется'),
                        numeric: true
                      ),
                    ],
                    rows: []
                  )
                ],
              ),
            ),
          )
        ],
      ),
    );
  }
}
