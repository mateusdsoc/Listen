import '../models/sessao.dart';
import '../models/status_sessao.dart';
import 'api_client.dart';

/// Operações de sessão disponíveis para o solicitante.
class SessaoService {
  final ApiClient _api;

  SessaoService(this._api);

  /// Abre uma nova sessão de escuta (status inicial `pendente`).
  Future<Sessao> criar(String descricao) async {
    final json = await _api.post('/sessoes', {'descricao': descricao});
    return Sessao.fromJson(json as Map<String, dynamic>);
  }

  /// Lista as sessões do solicitante autenticado (mais recentes primeiro).
  Future<List<Sessao>> listarMinhas() async {
    final json = await _api.get('/sessoes/minhas');
    return (json as List)
        .map((e) => Sessao.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  /// Consulta uma sessão por ID (usado no polling da tela de detalhes).
  Future<Sessao> consultar(String id) async {
    final json = await _api.get('/sessoes/$id');
    return Sessao.fromJson(json as Map<String, dynamic>);
  }

  /// Atualiza o status da sessão (ex.: cancelar ou concluir).
  Future<Sessao> atualizarStatus(String id, StatusSessao status) async {
    final json = await _api.patch('/sessoes/$id/status', {
      'status': status.apiValue,
    });
    return Sessao.fromJson(json as Map<String, dynamic>);
  }
}
