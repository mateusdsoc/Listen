import 'package:flutter/material.dart';

import '../models/status_sessao.dart';

/// Chip colorido que representa o status da sessão.
class StatusChip extends StatelessWidget {
  final StatusSessao status;

  const StatusChip(this.status, {super.key});

  Color get _cor {
    switch (status) {
      case StatusSessao.pendente:
        return Colors.orange;
      case StatusSessao.aceita:
        return Colors.blue;
      case StatusSessao.emAndamento:
        return Colors.teal;
      case StatusSessao.concluida:
        return Colors.green;
      case StatusSessao.cancelada:
        return Colors.grey;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(
        color: _cor.withValues(alpha: 0.15),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: _cor),
      ),
      child: Text(
        status.label,
        style: TextStyle(color: _cor, fontWeight: FontWeight.w600, fontSize: 12),
      ),
    );
  }
}
