import 'dart:convert';

import 'package:http/http.dart' as http;

import '../core/api_config.dart';
import '../core/api_exception.dart';

/// Cliente HTTP fino sobre o `package:http`, responsável por montar a URL
/// base, anexar o token Bearer e traduzir respostas de erro em
/// [ApiException] com mensagem amigável.
class ApiClient {
  final http.Client _http;
  String? _token;

  ApiClient({http.Client? client}) : _http = client ?? http.Client();

  /// Define o token usado no header `Authorization` das próximas chamadas.
  void setToken(String? token) => _token = token;

  Map<String, String> get _headers => {
        'Content-Type': 'application/json',
        if (_token != null) 'Authorization': 'Bearer $_token',
      };

  Uri _uri(String path) => Uri.parse('${ApiConfig.baseUrl}$path');

  Future<dynamic> get(String path) async {
    final res = await _http.get(_uri(path), headers: _headers);
    return _handle(res);
  }

  Future<dynamic> post(String path, Map<String, dynamic> body) async {
    final res = await _http.post(
      _uri(path),
      headers: _headers,
      body: jsonEncode(body),
    );
    return _handle(res);
  }

  Future<dynamic> patch(String path, Map<String, dynamic> body) async {
    final res = await _http.patch(
      _uri(path),
      headers: _headers,
      body: jsonEncode(body),
    );
    return _handle(res);
  }

  dynamic _handle(http.Response res) {
    final hasBody = res.body.isNotEmpty;
    final decoded = hasBody ? jsonDecode(utf8.decode(res.bodyBytes)) : null;

    if (res.statusCode >= 200 && res.statusCode < 300) {
      return decoded;
    }

    // O backend devolve {"detail": "..."} ou {"message": "..."} nos erros.
    String message = 'Erro ${res.statusCode}';
    if (decoded is Map) {
      message = (decoded['detail'] ?? decoded['message'] ?? message).toString();
    }
    throw ApiException(message, statusCode: res.statusCode);
  }
}
