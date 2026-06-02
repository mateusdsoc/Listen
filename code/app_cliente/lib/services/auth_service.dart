import '../models/usuario.dart';
import 'api_client.dart';

/// Operações de cadastro e autenticação do solicitante.
class AuthService {
  final ApiClient _api;

  AuthService(this._api);

  /// Cadastra um novo solicitante. Não autentica — o app segue para o login.
  Future<void> cadastrar({
    required String primeiroNome,
    required String email,
    required String senha,
  }) async {
    await _api.post('/solicitantes', {
      'primeiro_nome': primeiroNome,
      'email': email,
      'senha': senha,
    });
  }

  /// Autentica o solicitante e devolve o usuário com o token JWT.
  Future<Usuario> login({
    required String email,
    required String senha,
  }) async {
    final json = await _api.post('/auth/login', {
      'email': email,
      'senha': senha,
      'role': 'solicitante',
    });
    return Usuario.fromLoginJson(json as Map<String, dynamic>);
  }
}
