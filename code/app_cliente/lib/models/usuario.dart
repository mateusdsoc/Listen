/// Dados do solicitante autenticado, derivados da resposta de login.
class Usuario {
  final String id;
  final String nome;
  final String email;
  final String token;

  Usuario({
    required this.id,
    required this.nome,
    required this.email,
    required this.token,
  });

  factory Usuario.fromLoginJson(Map<String, dynamic> json) {
    return Usuario(
      id: json['user_id'] as String,
      nome: json['nome'] as String,
      email: json['email'] as String,
      token: json['access_token'] as String,
    );
  }
}
