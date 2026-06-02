/// Erro de comunicação com a API, já com mensagem amigável extraída
/// do corpo da resposta quando disponível.
class ApiException implements Exception {
  final int? statusCode;
  final String message;

  ApiException(this.message, {this.statusCode});

  @override
  String toString() => message;
}
