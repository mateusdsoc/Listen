import 'package:flutter/foundation.dart';

import '../models/usuario.dart';
import '../services/api_client.dart';
import '../services/auth_service.dart';

/// Estado de autenticação. Mantém o usuário logado e propaga o token
/// para o [ApiClient] compartilhado.
class AuthProvider extends ChangeNotifier {
  final AuthService _authService;
  final ApiClient _api;

  AuthProvider(this._authService, this._api);

  Usuario? _usuario;
  Usuario? get usuario => _usuario;
  bool get autenticado => _usuario != null;

  Future<void> cadastrar({
    required String primeiroNome,
    required String email,
    required String senha,
  }) {
    return _authService.cadastrar(
      primeiroNome: primeiroNome,
      email: email,
      senha: senha,
    );
  }

  Future<void> login({required String email, required String senha}) async {
    final usuario = await _authService.login(email: email, senha: senha);
    _usuario = usuario;
    _api.setToken(usuario.token);
    notifyListeners();
  }

  void logout() {
    _usuario = null;
    _api.setToken(null);
    notifyListeners();
  }
}
