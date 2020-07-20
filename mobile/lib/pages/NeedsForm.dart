import 'package:flutter/material.dart';
import 'package:tirek_mobile/exception/TirekException.dart';
import 'package:tirek_mobile/models/response/HospitalResponse.dart';
import 'package:tirek_mobile/models/response/NeedsResponse.dart';
import 'package:tirek_mobile/services/HospitalService.dart';
import 'package:tirek_mobile/services/NeedsService.dart';
import 'package:tirek_mobile/services/NeedsRequestService.dart';
import 'package:tirek_mobile/services/SharedPreferencesService.dart';

class NeedsForm extends StatefulWidget {
  NeedsForm(
      {this.hospitalService, this.needsService, this.sharedPreferencesService, this.needsRequestService});

  final HospitalService hospitalService;
  final NeedsService needsService;
  final NeedsRequestService needsRequestService;
  final SharedPreferencesService sharedPreferencesService;

  @override
  State<StatefulWidget> createState() => new _NeedsFormState();
}

class _NeedsFormState extends State<NeedsForm> {
  String _errorMessage;
  bool _isLoading;

  List _needTypes = [];
  List _hospitals = [];

  Hospital hospital;
  NeedType needType;
  String reserveAmount;
  String requestAmount;
  String requestAmountMonth;

  @override
  void initState() {
    _errorMessage = "";
    _isLoading = false;
    super.initState();
    getData();
  }

  void getData() async {
    try {
      final needsResponse = await widget.needsService.get();
      final hospitalsResponse = await widget.hospitalService.get();

      print(_hospitals);

      setState(() {
        _needTypes = needsResponse.needs;
        _hospitals = hospitalsResponse.hospitals;
      });
    } on TirekException {
      setState(() {
        _isLoading = false;
        _errorMessage = "Произошла ошибка при подключении";
      });
    }
  }

  final _formKey = GlobalKey<FormState>();
  final padding = EdgeInsets.all(16);
  final formItemPadding = EdgeInsets.fromLTRB(0, 0, 0, 16.0);

  void validateAndSubmit() {
    setState(() {
      _errorMessage = "";
      _isLoading = true;
    });

    bool validateAndSave() {
      final form = _formKey.currentState;
      if (form.validate()) {
        form.save();
        return true;
      }
      return false;
    }

    if (validateAndSave()) {
      try {
        widget.needsRequestService.req(
            hospital,
            needType,
            reserveAmount,
            requestAmount,
            requestAmountMonth);

        Navigator.pushNamedAndRemoveUntil(context, '/home', (r) => false);

        setState(() {
          _isLoading = false;
        });
      } on BadRequestException {
        setState(() {
          _isLoading = false;
          _errorMessage = "Неправильное имя пользователя или пароль";
          _formKey.currentState.reset();
        });
      } on TirekException {
        setState(() {
          _isLoading = false;
          _errorMessage = "Произошла ошибка при подключении";
          _formKey.currentState.reset();
        });
      }
    } else {
      setState(() {
        _isLoading = false;
      });
    }
  }

  Widget build(BuildContext context) {
    return new Scaffold(
        appBar: new AppBar(
          title: new Text('Создание таблицы данных'),
        ),
        body: Container(
          child: SingleChildScrollView(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: <Widget>[
                new Form(
                  key: _formKey,
                  child: Padding(
                    padding: padding,
                    child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: <Widget>[
                          Padding(
                            padding: formItemPadding,
                            child: new DropdownButtonFormField<NeedType>(
                                decoration: const InputDecoration(
                                  labelText: 'Тип нужды',
                                  helperText: 'Укажите тип помощи больнице',
                                ),
                                style: TextStyle(color: Colors.black),
                                onChanged: (NeedType newValue) {
                                  setState(() {
                                    needType = newValue;
                                  });
                                },
                                isExpanded: true,
                                items: _needTypes
                                    .map((value) =>
                                        new DropdownMenuItem<NeedType>(
                                          value: value,
                                          child: new Text(value.name),
                                        ))
                                    .toList()),
                          ),
                          Padding(
                            padding: formItemPadding,
                            child: new DropdownButtonFormField<Hospital>(
                              decoration: const InputDecoration(
                                labelText: 'Больница',
                                helperText: 'Укажите больницу',
                              ),
                              style: TextStyle(color: Colors.black),
                              onChanged: (Hospital newValue) {
                                setState(() {
                                  hospital = newValue;
                                });
                              },
                              isExpanded: true,
                              items: _hospitals
                                  .map(
                                      (value) => new DropdownMenuItem<Hospital>(
                                            value: value,
                                            child: new Text(value.name),
                                          ))
                                  .toList(),
                            ),
                          ),
                          Padding(
                            padding: formItemPadding,
                            child: TextFormField(
                              decoration: const InputDecoration(
                                labelText: 'В наличии',
                                helperText: 'Укажите количество',
                              ),
                              keyboardType: TextInputType.number,
                              onChanged: (value) => reserveAmount = value,
                              validator: (value) {
                                if (value.isEmpty) {
                                  return 'Please enter some text';
                                }
                                return null;
                              },
                            ),
                          ),
                          Padding(
                            padding: formItemPadding,
                            child: TextFormField(
                              decoration: const InputDecoration(
                                labelText: 'Требуется',
                                helperText: 'Укажите количество',
                              ),
                              keyboardType: TextInputType.number,
                              onChanged: (value) => requestAmount = value,
                              validator: (value) {
                                if (value.isEmpty) {
                                  return 'Please enter some text';
                                }
                                return null;
                              },
                            ),
                          ),
                          Padding(
                            padding: formItemPadding,
                            child: TextFormField(
                              decoration: const InputDecoration(
                                labelText: 'Требуется в месяц',
                                helperText: 'Укажите количество',
                              ),
                              keyboardType: TextInputType.number,
                              onChanged: (value) => requestAmountMonth = value,
                              validator: (value) {
                                if (value.isEmpty) {
                                  return 'Please enter some text';
                                }
                                return null;
                              },
                            ),
                          ),
                          Padding(
                            padding: formItemPadding,
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.end,
                              children: <Widget>[
                                FlatButton(
                                    color: Colors.blue,
                                    textColor: Colors.white,
                                    disabledColor: Colors.grey,
                                    disabledTextColor: Colors.black,
                                    padding: EdgeInsets.all(8.0),
                                    splashColor: Colors.blueAccent,
                                    shape: RoundedRectangleBorder(
                                        borderRadius:
                                            BorderRadius.circular(20)),
                                    onPressed: validateAndSubmit,
                                    child: Padding(
                                      padding:
                                          EdgeInsets.fromLTRB(16, 0, 16, 0),
                                      child: Text('СОХРАНИТЬ'),
                                    ))
                              ],
                            ),
                          ),
                        ]),
                  ),
                ),
              ],
            ),
          ),
        ));
  }
}
