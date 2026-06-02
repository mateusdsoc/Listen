/// Avaliação embutida na sessão (somente leitura no app do cliente —
/// o backend ainda não expõe endpoint para enviá-la).
class Avaliacao {
  final int nota;
  final String? comentario;

  Avaliacao({required this.nota, this.comentario});

  factory Avaliacao.fromJson(Map<String, dynamic> json) {
    return Avaliacao(
      nota: json['nota'] as int,
      comentario: json['comentario'] as String?,
    );
  }
}
