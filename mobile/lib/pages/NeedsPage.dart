import 'package:flutter/material.dart';
import 'package:tirek_mobile/components/TextFieldDatePicker.dart';
import 'package:tirek_mobile/pages/DistributionNeedsPage.dart';
import 'package:tirek_mobile/models/response/DistributionStatus.dart';
import 'package:tirek_mobile/models/response/DonataionResponse.dart';
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

  String _deliveryDate;
  String _distributionDate;
  String _errorMessage;
  final _formKey = new GlobalKey<FormState>();
  String _fromPerson;
  String _hospital;
  bool _isLoading;
  String _organization;
  bool _rememberMe = false;
  bool _showPassword = false;
  String _status;
  String _toPerson;

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
              _showHospitalInput(context),
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
                MaterialPageRoute(builder: (context) => DistributionNeedsPage()),
              )
            }),
          ),
        );
  }

  Widget _showHospitalInput(context) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(0.0, 12.0, 0.0, 0.0),
      child: new TextFormField(
        controller: hospitalController,
        readOnly: true,
        maxLines: 1,
        keyboardType: TextInputType.text,
        autofocus: false,
        decoration: new InputDecoration(
          suffixIcon: Icon(Icons.arrow_drop_down),
          filled: true,
          fillColor: Color(0xFFE8E8E8),
          hintText: 'Больница',
          helperText: 'Укажите больницу',
        ),
        onSaved: (value) => _hospital = value.trim(),
        onTap: () async {
          var hospital = await _selectHospital(context);
          hospitalController.text = hospital.name;
        },
      ),
    );
  }

  Widget _showDonationInput() {
    return Padding(
      padding: const EdgeInsets.fromLTRB(0.0, 20.0, 0.0, 0.0),
      child: new TextFormField(
        controller: donationController,
        readOnly: true,
        maxLines: 1,
        keyboardType: TextInputType.text,
        autofocus: false,
        decoration: new InputDecoration(
          suffixIcon: Icon(Icons.arrow_drop_down),
          filled: true,
          fillColor: Color(0xFFE8E8E8),
          hintText: 'Организация',
          helperText: 'Укажите организацию',
        ),
        onSaved: (value) => _hospital = value.trim(),
        onTap: () async {
          var donation = await _selectDonation(context);
          donationController.text = donation.donatorName;
        },
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
          // Do something with the selected date
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
          // Do something with the selected date
        },
      ),
    );
  }

  Widget _showStatusInput() {
    return Padding(
      padding: const EdgeInsets.fromLTRB(0.0, 20.0, 0.0, 0.0),
      child: new TextFormField(
        controller: statusController,
        readOnly: true,
        maxLines: 1,
        keyboardType: TextInputType.text,
        autofocus: false,
        decoration: new InputDecoration(
          filled: true,
          fillColor: Color(0xFFE8E8E8),
          hintText: 'Статус',
          helperText: 'Укажите статус пожертвования',
          suffixIcon: Icon(Icons.arrow_drop_down),
        ),
        onSaved: (value) => _status = value.trim(),
        onTap: () async {
          var distributionStatus = await _selectStatus(context);
          statusController.text = distributionStatus.value;
        },
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

  Future<DistributionStatus> _selectStatus(BuildContext context) async {
    return await showDialog<DistributionStatus>(
      context: context,
      builder: (BuildContext context) {
        return SimpleDialog(
          title: const Text('Выберите статус'),
          children: <Widget>[
            SimpleDialogOption(
              onPressed: () {
                Navigator.pop(
                    context,
                    new DistributionStatus(
                        Status.ready_to_sent, "Подготовлено"));
              },
              child: const Text('Подготовлено'),
            ),
            SimpleDialogOption(
              onPressed: () {
                Navigator.pop(
                    context, new DistributionStatus(Status.sent, "Отправлено"));
              },
              child: const Text('Отправлено'),
            ),
            SimpleDialogOption(
              onPressed: () {
                Navigator.pop(context,
                    new DistributionStatus(Status.delivered, "Доставлено"));
              },
              child: const Text('Доставлено'),
            ),
          ],
        );
      },
    );
  }

  Future<Hospital> _selectHospital(BuildContext context) async {
    var hospitalResponse = await widget.hospitalService.get();

    var options = hospitalResponse.hospitals
        .map((hospital) => SimpleDialogOption(
              onPressed: () {
                Navigator.pop(context, hospital);
              },
              child: Text(hospital.name),
            ))
        .toList();

    return await showDialog(
        context: context,
        builder: (BuildContext context) {
          return SimpleDialog(
            title: const Text('Выберите больницу'),
            children: options,
          );
        });
  }

  Future<Donation> _selectDonation(BuildContext context) async {
    var donationsResponse = await widget.donationService.get();

    var options = donationsResponse.donations
        .map((donation) => SimpleDialogOption(
              onPressed: () {
                Navigator.pop(context, donation);
              },
              child: Text(donation.donatorName),
            ))
        .toList();

    return await showDialog(
        context: context,
        builder: (BuildContext context) {
          return SimpleDialog(
            title: const Text('Выберите организацию'),
            children: options,
          );
        });
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
