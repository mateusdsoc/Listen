/// Espelha o enum `StatusSessao` do backend.
enum StatusSessao {
  pendente,
  aceita,
  emAndamento,
  concluida,
  cancelada;

  /// Valor exato usado pela API (snake_case).
  String get apiValue {
    switch (this) {
      case StatusSessao.emAndamento:
        return 'em_andamento';
      default:
        return name;
    }
  }

  static StatusSessao fromApi(String value) {
    switch (value) {
      case 'pendente':
        return StatusSessao.pendente;
      case 'aceita':
        return StatusSessao.aceita;
      case 'em_andamento':
        return StatusSessao.emAndamento;
      case 'concluida':
        return StatusSessao.concluida;
      case 'cancelada':
        return StatusSessao.cancelada;
      default:
        throw ArgumentError('Status desconhecido: $value');
    }
  }

  /// Rótulo amigável para a interface.
  String get label {
    switch (this) {
      case StatusSessao.pendente:
        return 'Aguardando ouvinte';
      case StatusSessao.aceita:
        return 'Aceita';
      case StatusSessao.emAndamento:
        return 'Em andamento';
      case StatusSessao.concluida:
        return 'Concluída';
      case StatusSessao.cancelada:
        return 'Cancelada';
    }
  }

  bool get isTerminal =>
      this == StatusSessao.concluida || this == StatusSessao.cancelada;
}
