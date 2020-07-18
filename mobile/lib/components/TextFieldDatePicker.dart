import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

class TextFieldDatePicker extends StatefulWidget {
  final ValueChanged<DateTime> onDateChanged;
  final DateTime initialDate;
  final DateTime firstDate;
  final DateTime lastDate;
  final DateFormat dateFormat;
  final FocusNode focusNode;
  final String labelText;
  final String helperText;
  final Icon prefixIcon;
  final Icon suffixIcon;
  final bool initialValue;

  TextFieldDatePicker(
      {Key key,
      this.labelText,
      this.prefixIcon,
      this.suffixIcon,
      this.focusNode,
      this.dateFormat,
      @required this.lastDate,
      @required this.firstDate,
      @required this.initialDate,
      @required this.onDateChanged,
      this.initialValue,
      this.helperText})
      : assert(firstDate != null),
        assert(lastDate != null),
        assert(
            initialDate == null ||
                (initialDate != null && !initialDate.isBefore(firstDate)),
            'initialDate must be on or after firstDate'),
        assert(
            initialDate == null ||
                (initialDate != null && !initialDate.isAfter(lastDate)),
            'initialDate must be on or before lastDate'),
        assert(!firstDate.isAfter(lastDate),
            'lastDate must be on or after firstDate'),
        assert(onDateChanged != null, 'onDateChanged must not be null'),
        super(key: key);

  @override
  _TextFieldDatePicker createState() => _TextFieldDatePicker();
}

class _TextFieldDatePicker extends State<TextFieldDatePicker> {
  TextEditingController _controllerDate;
  DateFormat _dateFormat;
  DateTime _selectedDate;

  @override
  void initState() {
    super.initState();

    if (widget.dateFormat != null) {
      _dateFormat = widget.dateFormat;
    } else {
      _dateFormat = DateFormat.yMMMd('ru');
    }

    _selectedDate = widget.initialDate;

    _controllerDate = TextEditingController();

    if (widget.initialValue != null) {
      _controllerDate.text = _dateFormat.format(_selectedDate);
    }
  }

  @override
  Widget build(BuildContext context) {
    return TextField(
      focusNode: widget.focusNode,
      controller: _controllerDate,
      decoration: InputDecoration(
          filled: true,
          prefixIcon: widget.prefixIcon,
          suffixIcon: widget.suffixIcon,
          labelText: widget.labelText,
          helperText: widget.helperText),
      onTap: () => _selectDate(context),
      readOnly: true,
    );
  }

  @override
  void dispose() {
    _controllerDate.dispose();
    super.dispose();
  }

  Future<Null> _selectDate(BuildContext context) async {
    final DateTime pickedDate = await showDatePicker(
      context: context,
      initialDate: widget.initialValue ? DateTime.now() : _selectedDate,
      firstDate: widget.firstDate,
      lastDate: widget.lastDate,
    );

    if (pickedDate != null && pickedDate != _selectedDate) {
      _selectedDate = pickedDate;

      _controllerDate.text = _dateFormat.format(_selectedDate);
      widget.onDateChanged(_selectedDate);
    }

    if (widget.focusNode != null) {
      widget.focusNode.nextFocus();
    }
  }
}
