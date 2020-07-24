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

  List _needTypesList;
  NeedsType _needType;

  final formItemPadding = EdgeInsets.fromLTRB(0, 0, 0, 16.0);


  @override
  void initState() {
    _errorMessage = "";
    _isLoading = false;
    super.initState();
    fetchNeedTypesRequiredData();
    print(widget.needsTypeService);

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
      body: Center(
        child: _showForm(context),
      ),
    );
  }

  Widget _showForm(BuildContext context) {
    List _distributionFroms = [];
    for ( var i in _distributionNeeds ) {
      //_distributionFroms.add()
    }
    return new Container(
        padding: EdgeInsets.fromLTRB(10.0, 10.0, 10.0, 0.0),
        child: new Form(
          key: _formKey,
          child: new ListView(
            shrinkWrap: true,
            children: <Widget>[
              Text("Создание данных о пожертвование  2 из 2"),
              ..._distributionFroms,
              _showNeedsTypeSelect(context),
              showAddButton(),
              showPrimaryButton(),
              showErrorMessage(),
            ],
          ),
        ));
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
    return new Padding(
        padding: EdgeInsets.fromLTRB(10.0, 45.0, 0.0, 0.0),
        child: SizedBox(
          height: 36.0,
          width: 96.0,
          child: new RaisedButton(
            shape: new RoundedRectangleBorder(
                borderRadius: new BorderRadius.circular(0.0),
                side: BorderSide(color: Color(0xFFE8E8E8))),
            color: Color(0xFFE8E8E8),
            child: new Text('Добавить еще',
                style: new TextStyle(
                    fontSize: 14.0,
                    color: Color(0xCE000000),
                    fontFamily: 'Roboto',
                    fontStyle: FontStyle.normal)),
            onPressed: validateAndSubmit,
          ),
        ));
  }


  Widget showPrimaryButton() {
    return new Padding(
        padding: EdgeInsets.fromLTRB(250.0, 45.0, 0.0, 0.0),
        child: SizedBox(
          height: 36.0,
          width: 96.0,
          child: new RaisedButton(
            shape: new RoundedRectangleBorder(
                borderRadius: new BorderRadius.circular(200.0),
                side: BorderSide(color: Color(0xFF2F80ED))),
            color: Color(0xFF2F80ED),
            child: new Text('Сохранить',
                style: new TextStyle(
                    fontSize: 14.0,
                    color: Colors.white,
                    fontFamily: 'Roboto',
                    fontStyle: FontStyle.normal)),
            onPressed: validateAndSubmit,
          ),
        ));
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