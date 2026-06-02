import 'package:flutter/material.dart';

import '../models/sessao.dart';
import 'status_chip.dart';

/// Cartão que resume uma sessão na lista.
class SessaoCard extends StatelessWidget {
  final Sessao sessao;
  final VoidCallback onTap;

  const SessaoCard({super.key, required this.sessao, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
      child: ListTile(
        contentPadding: const EdgeInsets.all(16),
        title: Text(
          sessao.descricao,
          maxLines: 2,
          overflow: TextOverflow.ellipsis,
          style: const TextStyle(fontWeight: FontWeight.w600),
        ),
        subtitle: Padding(
          padding: const EdgeInsets.only(top: 8),
          child: StatusChip(sessao.status),
        ),
        trailing: const Icon(Icons.chevron_right),
        onTap: onTap,
      ),
    );
  }
}
