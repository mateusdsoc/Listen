import 'package:flutter/foundation.dart';

/// Configuração da URL base da API.
///
/// - Em navegador (Flutter web) o backend é acessível em `localhost`.
/// - No emulador Android o host da máquina é exposto em `10.0.2.2`.
/// - Em dispositivo físico, troque por `http://<ip-da-maquina>:8000`.
class ApiConfig {
  static String get baseUrl {
    if (kIsWeb) {
      return 'http://localhost:8000/api/v1';
    }
    return 'http://10.0.2.2:8000/api/v1';
  }

  /// Intervalo de polling para refletir mudanças de estado vindas do
  /// servidor (ex.: ouvinte aceitou a sessão) sem ação do usuário.
  static const Duration pollingInterval = Duration(seconds: 5);
}
