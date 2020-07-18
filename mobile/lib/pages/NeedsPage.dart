import 'package:flutter/material.dart';
import 'package:tirek_mobile/exception/TirekException.dart';


class NeedsPage extends StatefulWidget {
  @override
  State<StatefulWidget> createState() => new _NeedsPageState();
}

class _NeedsPageState extends State<NeedsPage> {
  final _formKey = new GlobalKey<FormState>();

  String _hospital;
  String _organization;
  String _fromPerson;
  String _toPerson;
  String _distributionDate;
  String _deliveryDate;
  String _status;

  String _errorMessage;

  bool _showPassword = false;
  bool _isLoading;

  bool _rememberMe = false;

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

        Navigator.pushNamed(context, '/home');

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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Детали распределения"),
      ),
      body: Center(
        child: _showForm(),
        ),
    );
  }

  

  Widget _showForm() {
    return new Container(
        padding: EdgeInsets.fromLTRB(0.0, 12.0, 16.0, 16.0),
        child: new Form(
          key: _formKey,
          child: new ListView(
            shrinkWrap: true,
            children: <Widget>[
              Text("Создание данных о пожертвование  1 из 2"),
              showHospitalInput(),
              showOrganizationInput(),
              showFromPersonInput(),
              showToPersonInput(),
              showDistributionDateInput(),
              showDeliveryDateInput(),
              showStatusInput(),
              showPrimaryButton(),
              showErrorMessage(),
            ],
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

  Widget showHospitalInput() {
    return Padding(
      padding: const EdgeInsets.fromLTRB(0.0, 12.0, 0.0, 0.0),
      child: new TextFormField(
        maxLines: 1,
        keyboardType: TextInputType.text,
        autofocus: false,
        decoration: new InputDecoration(
            filled: true,
            fillColor: Color(0xFFE8E8E8),
            hintText: 'Больница',
        ),
        onSaved: (value) => _hospital = value.trim(),
      ),
    );
  }

  Widget showOrganizationInput() {
    return Padding(
      padding: const EdgeInsets.fromLTRB(0.0, 44.0, 0.0, 0.0),
      child: new TextFormField(
        maxLines: 1,
        keyboardType: TextInputType.text,
        autofocus: false,
        decoration: new InputDecoration(
            filled: true,
            fillColor: Color(0xFFE8E8E8),
            hintText: 'Организация',
        ),
        onSaved: (value) => _hospital = value.trim(),
      ),
    );
  }

  Widget showFromPersonInput() {
    return Padding(
      padding: const EdgeInsets.fromLTRB(0.0, 44.0, 0.0, 0.0),
      child: new TextFormField(
        maxLines: 1,
        keyboardType: TextInputType.text,
        autofocus: false,
        decoration: new InputDecoration(
            filled: true,
            fillColor: Color(0xFFE8E8E8),
            hintText: 'Ф.И.О',
        ),
        onSaved: (value) => _fromPerson = value.trim(),
      ),
    );
  }

  Widget showToPersonInput() {
    return Padding(
      padding: const EdgeInsets.fromLTRB(0.0, 44.0, 0.0, 0.0),
      child: new TextFormField(
        maxLines: 1,
        keyboardType: TextInputType.text,
        autofocus: false,
        decoration: new InputDecoration(
            filled: true,
            fillColor: Color(0xFFE8E8E8),
            hintText: 'Ф.И.О',
        ),
        onSaved: (value) => _toPerson = value.trim(),
      ),
    );
  }

  Widget showDistributionDateInput() {
    return Padding(
      padding: const EdgeInsets.fromLTRB(0.0, 44.0, 0.0, 0.0),
      child: new TextFormField(
        maxLines: 1,
        keyboardType: TextInputType.text,
        autofocus: false,
        decoration: new InputDecoration(
            filled: true,
            fillColor: Color(0xFFE8E8E8),
            hintText: 'Дата распределения*'
        ),
        onSaved: (value) => _distributionDate = value.trim(),
      ),
    );
  }

  Widget showDeliveryDateInput() {
    return Padding(
      padding: const EdgeInsets.fromLTRB(0.0, 44.0, 0.0, 0.0),
      child: new TextFormField(
        maxLines: 1,
        keyboardType: TextInputType.text,
        autofocus: false,
        decoration: new InputDecoration(
            filled: true,
            fillColor: Color(0xFFE8E8E8),
            hintText: 'Дата доставки',
        ),
        onSaved: (value) => _deliveryDate = value.trim(),
      ),
    );
  }

  Widget showStatusInput() {
    return Padding(
      padding: const EdgeInsets.fromLTRB(0.0, 44.0, 0.0, 0.0),
      child: new TextFormField(
        maxLines: 1,
        keyboardType: TextInputType.text,
        autofocus: false,
        decoration: new InputDecoration(
            filled: true,
            fillColor: Color(0xFFE8E8E8),
            hintText: 'Статус',
        ),
        onSaved: (value) => _status = value.trim(),
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