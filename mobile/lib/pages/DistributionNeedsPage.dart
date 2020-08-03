import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:tirek_mobile/exception/TirekException.dart';
import 'package:tirek_mobile/services/NeedsTypeService.dart';
import 'package:tirek_mobile/models/response/NeedsTypeResponse.dart';

class DistributionNeedsPage extends StatefulWidget {
  const DistributionNeedsPage({this.needsTypeService});

  final NeedsTypeService needsTypeService;

  @override
  State<StatefulWidget> createState() => new _DistributionNeedsPageState();
}

class _DistributionNeedsPageState extends State<DistributionNeedsPage> {
  final _formKey = new GlobalKey<FormState>();
  final needsTypelController = TextEditingController();

  String _errorMessage;

  List<Map<String, dynamic>> _distributionNeeds = [];

  bool _isLoading;

  List _needTypesList = [];
  NeedsType _needType;
  final padding = EdgeInsets.all(16);

  final formItemPadding = EdgeInsets.fromLTRB(0, 0, 0, 16.0);

  @override
  void initState() {
    _errorMessage = "";
    _isLoading = false;
    super.initState();
    fetchNeedTypesRequiredData();
  }

  void fetchNeedTypesRequiredData() async {
    try {
      final donationsResponse = await widget.needsTypeService.get();
      setState(() {
        _needTypesList = donationsResponse.needsTypes;
      });
    } on TirekException {
      setState(() {
        _isLoading = false;
        _errorMessage = "Произошла ошибка при подключении";
      });
    }
  }

  bool validateAndSave() {
    final form = _formKey.currentState;
    if (form.validate()) {
      form.save();
      return true;
    }
    return false;
  }

  void validateAndSubmit() async {
    setState(() {
      _errorMessage = "";
      _isLoading = true;
    });

    if (validateAndSave()) {
      try {
        //inal authenticationResponse = await widget.authenticationService.login(_username, _password);

        //await widget.sharedPreferencesService.saveAuthenticationResponse(authenticationResponse);

        setState(() {
          _isLoading = false;
        });
      } on BadRequestException {
        setState(() {
          _isLoading = false;
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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Text("Назад"),
        ),
        body: Stack(
          children: <Widget>[
            SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: <Widget>[_showForm(context)],
              ),
            )
          ],
        ));
  }

  Widget _showForm(BuildContext context) {
    List _distributionFroms = [];
    for (var i in _distributionNeeds) {
      //_distributionFroms.add()
    }
    return Form(
      key: _formKey,
      child: Padding(
        padding: padding,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            Padding(
              padding: EdgeInsets.fromLTRB(0, 0, 0, 12.0),
              child: Text("Создание данных о пожертвование 2 из 2"),
            ),
            ..._distributionFroms,
            _showNeedsTypeSelect(context),
            showAddButton(),
            showPrimaryButton(),
            showErrorMessage(),
          ],
        ),
      ),
    );
  }

  Widget _showNeedsTypeSelect(context) {
    return Padding(
      padding: formItemPadding,
      child: new DropdownButtonFormField<NeedsType>(
        decoration: const InputDecoration(
          labelText: 'Тип помощи',
          helperText: 'Укажите тип помощи больнице',
        ),
        style: TextStyle(color: Colors.black),
        onChanged: (NeedsType newValue) {
          setState(() {
            _needType = newValue;
          });
        },
        validator: (value) {
          if (value == null) {
            return 'Это обязательное поле';
          }
          return null;
        },
        isExpanded: true,
        items: _needTypesList
            .map((value) => new DropdownMenuItem<NeedsType>(
                  value: value,
                  child: new Text(value.name),
                ))
            .toList(),
      ),
    );
  }

  Widget showAddButton() {
    return Padding(
        padding: formItemPadding,
        child: ConstrainedBox(
            constraints: BoxConstraints.expand(height: 56),
            child: FlatButton(
                color: Color.fromRGBO(232, 232, 232, 1),
                textColor: Colors.black,
                disabledColor: Colors.grey,
                disabledTextColor: Colors.black,
                padding: EdgeInsets.all(8.0),
                onPressed: validateAndSubmit,
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: <Widget>[
                    Icon(Icons.library_add),
                    Padding(
                      padding: EdgeInsets.fromLTRB(16, 0, 16, 0),
                      child: Text('Добавить еще', style: TextStyle(fontSize: 16, color: Color.fromARGB(153, 0, 0, 0)),),
                    )
                  ],
                )
            )
        )
    );
  }

  Widget showPrimaryButton() {
    return Padding(
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
                  borderRadius: BorderRadius.circular(20)),
              onPressed: validateAndSubmit,
              child: Padding(
                padding: EdgeInsets.fromLTRB(16, 0, 16, 0),
                child: Text('СОХРАНИТЬ'),
              ))
        ],
      ),
    );
  }

  Widget showErrorMessage() {
    if (_errorMessage != null && _errorMessage.length > 0) {
      return new Container(
          padding: EdgeInsets.all(16.0),
          child: new Text(
            _errorMessage,
            textAlign: TextAlign.center,
            style: TextStyle(
                fontSize: 13.0,
                color: Colors.red,
                height: 1.0,
                fontWeight: FontWeight.w300),
          ));
    } else {
      return new Container(
        height: 0.0,
      );
    }
  }
}
