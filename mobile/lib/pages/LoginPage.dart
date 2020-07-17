import 'package:flutter/material.dart';
import 'package:tirek_mobile/exception/TirekException.dart';
import 'package:tirek_mobile/services/AuthenticationService.dart';
import 'package:tirek_mobile/services/SharedPreferencesService.dart';

class LoginPage extends StatefulWidget {
  LoginPage(
      {this.authenticationService, this.sharedPreferencesService, this.loginCallback});

  final AuthenticationService authenticationService;
  final SharedPreferencesService sharedPreferencesService;
  final VoidCallback loginCallback;

  @override
  State<StatefulWidget> createState() => new _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _formKey = new GlobalKey<FormState>();

  String _username;
  String _password;
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
        final authenticationResponse =
            await widget.authenticationService.login(_username, _password);

        await widget.sharedPreferencesService.saveAuthenticationResponse(authenticationResponse);

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
  void initState() {
    _errorMessage = "";
    _isLoading = false;
    super.initState();
  }

  void resetForm() {
    _formKey.currentState.reset();
    _errorMessage = "";
  }

  void _togglePasswordVisibility() {
    setState(() {
      _showPassword = !_showPassword;
    });
  }

  void _onRememberMeChanged(bool value) {
    setState(() {
      _rememberMe = value;
    });
  }

  @override
  Widget build(BuildContext context) {
    return new Scaffold(
        body: Stack(
      children: <Widget>[
        _showForm(),
        _showCircularProgress(),
      ],
    ));
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

  Widget _showForm() {
    return new Container(
        padding: EdgeInsets.all(16.0),
        child: new Form(
          key: _formKey,
          child: new ListView(
            shrinkWrap: true,
            children: <Widget>[
              showLogo(),
              showEmailInput(),
              showPasswordInput(),
              showPrimaryButton(),
              showErrorMessage(),
            ],
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

  Widget showLogo() {
    return new Hero(
      tag: 'hero',
      child: Padding(
        padding: EdgeInsets.fromLTRB(0.0, 111.0, 0.0, 0.0),
        child: CircleAvatar(
          backgroundColor: Colors.transparent,
          child: Image.asset(
            'assets/tirek-logo.png',
            width: 134,
            height: 50.55,
            fit: BoxFit.fitWidth,
          ),
        ),
      ),
    );
  }

  Widget showEmailInput() {
    return Padding(
      padding: const EdgeInsets.fromLTRB(0.0, 100.0, 0.0, 0.0),
      child: new TextFormField(
        maxLines: 1,
        keyboardType: TextInputType.emailAddress,
        autofocus: false,
        decoration: new InputDecoration(
            filled: true,
            fillColor: Color(0xFFE8E8E8),
            hintText: 'Имя пользователя',
            prefixIcon: new Icon(
              Icons.account_circle,
              color: Color(0xFF6B6B6B),
            )),
        validator: (value) => value.isEmpty ? 'Это поле обязательно' : null,
        onSaved: (value) => _username = value.trim(),
      ),
    );
  }

  Widget showPasswordInput() {
    return Padding(
      padding: const EdgeInsets.fromLTRB(0.0, 15.0, 0.0, 0.0),
      child: new TextFormField(
        maxLines: 1,
        obscureText: !_showPassword,
        autofocus: false,
        decoration: new InputDecoration(
            filled: true,
            hintText: 'Пароль',
            prefixIcon: new Icon(
              Icons.lock,
              color: Color(0xFF6B6B6B),
            ),
            suffixIcon: GestureDetector(
              onTap: () {
                _togglePasswordVisibility();
              },
              child: Icon(
                _showPassword ? Icons.visibility : Icons.visibility_off,
                color: Color(0xFF6B6B6B),
              ),
            )),
        validator: (value) => value.isEmpty ? 'Это поле обязательно' : null,
        onSaved: (value) => _password = value.trim(),
      ),
    );
  }

  Widget showPrimaryButton() {
    return new Padding(
//        right: 100.0,
        padding: EdgeInsets.fromLTRB(250.0, 45.0, 0.0, 0.0),
        child: SizedBox(
          height: 36.0,
          width: 96.0,
          child: new RaisedButton(
            shape: new RoundedRectangleBorder(
                borderRadius: new BorderRadius.circular(200.0),
                side: BorderSide(color: Color(0xFF2F80ED))),
            color: Color(0xFF2F80ED),
            child: new Text('ВОЙТИ',
                style: new TextStyle(
                    fontSize: 14.0,
                    color: Colors.white,
                    fontFamily: 'Roboto',
                    fontStyle: FontStyle.normal)),
            onPressed: validateAndSubmit,
          ),
        ));
  }
}
