import 'dart:convert';
import 'dart:io';

import 'package:http/http.dart' as http;
import 'package:tirek_mobile/exception/TirekException.dart';

class ApiHelper {
  static final String baseUrl = "https://antivirus.el.kg/api/v1/";

  static Future<dynamic> post(
      String path, Map<String, String> headers, String body) async {
    try {
      final response =
          await http.post(baseUrl + path, headers: headers, body: body);

      return _returnResponse(response);
    } on SocketException {
      throw FetchDataException('Нет подключения к интернету');
    }
  }

  static Future<dynamic> get(String path, Map<String, String> headers) async {
    try {
      final response = await http.get(baseUrl + path, headers: headers);

      return _returnResponse(response);
    } on SocketException {
      throw FetchDataException('Нет подключения к интернету');
    }
  }

  static dynamic _returnResponse(http.Response response) async {
    switch (response.statusCode) {
      case 200:
        var responseJson = json.decode(utf8.decode(response.bodyBytes));
        return responseJson;
      case 400:
        throw BadRequestException(response.body.toString());
      case 401:
      case 403:
        throw UnauthorisedException(response.body.toString());
      case 500:
      default:
        throw FetchDataException('Произошла ошибка : ${response.statusCode}');
    }
  }
}
