import 'dart:async';

import 'package:flutter/foundation.dart';

import '../core/api_config.dart';
import '../models/sessao.dart';
import '../services/sessao_service.dart';

/// Estado da lista "minhas sessões". Faz polling periódico para refletir
/// mudanças vindas do servidor (ex.: ouvinte aceitou) sem ação do usuário.
class SessoesProvider extends ChangeNotifier {
  final SessaoService _service;

  SessoesProvider(this._service);

  List<Sessao> _sessoes = [];
  List<Sessao> get sessoes => _sessoes;

  bool _carregando = false;
  bool get carregando => _carregando;

  String? _erro;
  String? get erro => _erro;

  Timer? _timer;

  /// Carrega a lista. Em modo [silencioso] não exibe spinner (usado no polling).
  Future<void> carregar({bool silencioso = false}) async {
    if (!silencioso) {
      _carregando = true;
      _erro = null;
      notifyListeners();
    }
    try {
      _sessoes = await _service.listarMinhas();
      _erro = null;
    } catch (e) {
      _erro = e.toString();
    } finally {
      _carregando = false;
      notifyListeners();
    }
  }

  Future<Sessao> criar(String descricao) async {
    final nova = await _service.criar(descricao);
    await carregar(silencioso: true);
    return nova;
  }

  void iniciarPolling() {
    _timer?.cancel();
    _timer = Timer.periodic(
      ApiConfig.pollingInterval,
      (_) => carregar(silencioso: true),
    );
  }

  void pararPolling() {
    _timer?.cancel();
    _timer = null;
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }
}
