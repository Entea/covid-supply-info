class TirekException implements Exception {
  final message;
  final prefix;

  TirekException([this.message, this.prefix]);

  String toString() {
    return "$prefix$message";
  }
}

class FetchDataException extends TirekException {
  FetchDataException([String message])
      : super(message, "Ошибка при подключении: ");
}

class BadRequestException extends TirekException {
  BadRequestException([message]) : super(message, "Неверный запрос: ");
}

class UnauthorisedException extends TirekException {
  UnauthorisedException([message]) : super(message, "Неразрешенный: ");
}

class InvalidInputException extends TirekException {
  InvalidInputException([String message])
      : super(message, "Некорректный ввод: ");
}
