import 'package:flutter/material.dart';
import 'package:tirek_mobile/components/TextFieldDatePicker.dart';
import 'package:tirek_mobile/exception/TirekException.dart';
import 'package:tirek_mobile/pages/DistributionNeedsPage.dart';
import 'package:tirek_mobile/models/response/DistributionStatus.dart';
import 'package:tirek_mobile/models/response/DonationResponse.dart';
import 'package:tirek_mobile/models/response/HospitalResponse.dart';
import 'package:tirek_mobile/services/DonationService.dart';
import 'package:tirek_mobile/services/HospitalService.dart';

class NeedsPage extends StatefulWidget {
  const NeedsPage({this.hospitalService, this.donationService});

  final DonationService donationService;
  final HospitalService hospitalService;

  @override
  State<StatefulWidget> createState() => new _NeedsPageState();
}

class _NeedsPageState extends State<NeedsPage> {
  final donationController = TextEditingController();
  final hospitalController = TextEditingController();
  DateTime selectedDate = DateTime.now();
  final statusController = TextEditingController();

  List _hospitalsList = [];
  List _donationsList = [];

  String _deliveryDate;
  String _distributionDate;
  String _errorMessage;
  final _formKey = new GlobalKey<FormState>();
  String _fromPerson;
  int _hospital;
  int _donation;
  bool _isLoading;
  String _organization;
  bool _rememberMe = false;
  bool _showPassword = false;
  Status _status;
  String _toPerson;

  final formItemPadding = EdgeInsets.fromLTRB(0, 0, 0, 16.0);

  @override
  void initState() {
    _errorMessage = "";
    _isLoading = false;
    super.initState();
    fetchRequiredData();
    fetchDonationsRequiredData();
  }

  void fetchRequiredData() async {
    try {
      final hospitalsResponse = await widget.hospitalService.get();

      setState(() {
        _hospitalsList = hospitalsResponse.hospitals;
      });
    } on TirekException {
      setState(() {
        _isLoading = false;
        _errorMessage = "Произошла ошибка при подключении";
      });
    }
  }

  void fetchDonationsRequiredData() async {
    try {
      final donationsResponse = await widget.donationService.get();


      setState(() {
        _donationsList = donationsResponse.donations;
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

  Widget _showForm(BuildContext context) {
    return new Container(
        padding: EdgeInsets.fromLTRB(10.0, 0.0, 10.0, 0.0),
        child: new Form(
          key: _formKey,
          child: new ListView(
            shrinkWrap: true,
            children: <Widget>[
              Text("Создание данных о пожертвование 1 из 2"),
              _showHospitalInput(),
              _showDonationInput(),
              _showFromPersonInput(),
              _showToPersonInput(),
              _showDistributionDateInput(context),
              _showDeliveryDateInput(),
              _showStatusInput(),
              _showPrimaryButton(),
              _showErrorMessage(),
            ],
          ),
        ));
  }

  Widget _showPrimaryButton() {
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
            child: new Text('Далее',
                style: new TextStyle(
                    fontSize: 14.0,
                    color: Colors.white,
                    fontFamily: 'Roboto',
                    fontStyle: FontStyle.normal)),
            onPressed: () => {
              Navigator.push(
                context,
                MaterialPageRoute(
                    builder: (context) => DistributionNeedsPage()),
              )
            }),
      ),
    );
  }

  Widget _showHospitalInput() {
    return Padding(
      padding: formItemPadding,
      child: new DropdownButtonFormField<Hospital>(
        decoration: const InputDecoration(
          labelText: 'Больница',
          helperText: 'Укажите больницу',
        ),
        style: TextStyle(color: Colors.black),
        onChanged: (Hospital newValue) {
          setState(() {
            _hospital = newValue.id;
          });
        },
        validator: (value) {
          if (value == null) {
            return 'Это обязательное поле';
          }
          return null;
        },
        isExpanded: true,
        items: _hospitalsList
            .map((value) => new DropdownMenuItem<Hospital>(
          value: value,
          child: new Text(value.name),
        ))
            .toList(),
      ),
    );
  }

  Widget _showDonationInput() {
    return Padding(
      padding: formItemPadding,
      child: new DropdownButtonFormField<Donation>(
        decoration: const InputDecoration(
          labelText: 'Организация',
          helperText: 'Укажите организацию',
        ),
        style: TextStyle(color: Colors.black),
        onChanged: (Donation newValue) {
          setState(() {
            _donation = newValue.id;
          });
        },
        validator: (value) {
          if (value == null) {
            return 'Это обязательное поле';
          }
          return null;
        },
        isExpanded: true,
        items: _donationsList
            .map((value) => new DropdownMenuItem<Donation>(
          value: value,
          child: new Text(value.donatorName),
        ))
            .toList(),
      ),
    );
  }

  Widget _showFromPersonInput() {
    return Padding(
      padding: const EdgeInsets.fromLTRB(0.0, 20.0, 0.0, 0.0),
      child: new TextFormField(
        maxLines: 1,
        keyboardType: TextInputType.text,
        autofocus: false,
        decoration: new InputDecoration(
            filled: true,
            fillColor: Color(0xFFE8E8E8),
            hintText: 'Ф.И.О',
            helperText: 'Данные выдающего'),
        onSaved: (value) => _fromPerson = value.trim(),
      ),
    );
  }

  Widget _showToPersonInput() {
    return Padding(
      padding: const EdgeInsets.fromLTRB(0.0, 20.0, 0.0, 0.0),
      child: new TextFormField(
        maxLines: 1,
        keyboardType: TextInputType.text,
        autofocus: false,
        decoration: new InputDecoration(
          filled: true,
          fillColor: Color(0xFFE8E8E8),
          hintText: 'Ф.И.О',
          helperText: 'Данные принимающих',
        ),
        onSaved: (value) => _toPerson = value.trim(),
      ),
    );
  }

  Widget _showDistributionDateInput(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(0.0, 20.0, 0.0, 0.0),
      child: new TextFieldDatePicker(
        prefixIcon: Icon(Icons.date_range),
        suffixIcon: Icon(Icons.arrow_drop_down),
        lastDate: DateTime.now().add(Duration(days: 366)),
        initialValue: true,
        firstDate: DateTime.now(),
        initialDate: DateTime.now(),
        helperText: 'Дата распределения',
        onDateChanged: (selectedDate) {
          _distributionDate = selectedDate.toString();
        },
      ),
    );
  }

  Widget _showDeliveryDateInput() {
    return Padding(
      padding: const EdgeInsets.fromLTRB(0.0, 20.0, 0.0, 0.0),
      child: new TextFieldDatePicker(
        prefixIcon: Icon(Icons.date_range),
        suffixIcon: Icon(Icons.arrow_drop_down),
        lastDate: DateTime.now().add(Duration(days: 366)),
        firstDate: DateTime.now(),
        initialDate: DateTime.now(),
        initialValue: false,
        helperText: 'Дата доставки',
        onDateChanged: (selectedDate) {
          _deliveryDate = selectedDate.toString();
        },
      ),
    );
  }

  Widget _showStatusInput() {
    return Padding(
      padding: formItemPadding,
      child: new DropdownButtonFormField<Status>(
        decoration: const InputDecoration(
          labelText: 'Статус',
          helperText: 'Укажите статус пожертвования ',
        ),
        style: TextStyle(color: Colors.black),
        onChanged: (Status newValue) {
          setState(() {
            _status = newValue;
          });
        },
        validator: (value) {
          if (value == null) {
            return 'Это обязательное поле';
          }
          return null;
        },
        isExpanded: true,
        items: [
          DropdownMenuItem(
            value: Status.ready_to_sent,
            child: const Text('Подготовлено')
          ),
          DropdownMenuItem(
            value: Status.sent,
            child: const Text('Отправлено')
          ),
          DropdownMenuItem(
            value: Status.delivered,
            child: const Text('Доставлено')
          )
        ],
      ),
    );
  }

  Widget _showErrorMessage() {
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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Детали распределения"),
      ),
      body: Container(
        child: _showForm(context),
      ),
    );
  }
}
