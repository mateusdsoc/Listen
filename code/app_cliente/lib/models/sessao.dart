import 'avaliacao.dart';
import 'status_sessao.dart';

/// Espelha o `SessaoResponse` do backend.
class Sessao {
  final String id;
  final String solicitanteId;
  final String? ouvinteId;
  final String descricao;
  final StatusSessao status;
  final Avaliacao? avaliacao;
  final DateTime createdAt;
  final DateTime updatedAt;

  Sessao({
    required this.id,
    required this.solicitanteId,
    this.ouvinteId,
    required this.descricao,
    required this.status,
    this.avaliacao,
    required this.createdAt,
    required this.updatedAt,
  });

  factory Sessao.fromJson(Map<String, dynamic> json) {
    return Sessao(
      id: json['id'] as String,
      solicitanteId: json['solicitante_id'] as String,
      ouvinteId: json['ouvinte_id'] as String?,
      descricao: json['descricao'] as String,
      status: StatusSessao.fromApi(json['status'] as String),
      avaliacao: json['avaliacao'] != null
          ? Avaliacao.fromJson(json['avaliacao'] as Map<String, dynamic>)
          : null,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );
  }
}
