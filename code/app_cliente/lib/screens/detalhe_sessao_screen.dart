import 'dart:async';

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../core/api_config.dart';
import '../models/sessao.dart';
import '../models/status_sessao.dart';
import '../services/sessao_service.dart';
import '../state/sessoes_provider.dart';
import '../widgets/status_chip.dart';

class DetalheSessaoScreen extends StatefulWidget {
  final String sessaoId;

  const DetalheSessaoScreen({super.key, required this.sessaoId});

  @override
  State<DetalheSessaoScreen> createState() => _DetalheSessaoScreenState();
}

class _DetalheSessaoScreenState extends State<DetalheSessaoScreen> {
  late final SessaoService _service;
  Sessao? _sessao;
  String? _erro;
  bool _acaoEmCurso = false;
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    _service = context.read<SessaoService>();
    _carregar();
    // Polling: reflete automaticamente quando o ouvinte aceita/encerra.
    _timer = Timer.periodic(ApiConfig.pollingInterval, (_) => _carregar());
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  Future<void> _carregar() async {
    try {
      final sessao = await _service.consultar(widget.sessaoId);
      if (!mounted) return;
      setState(() {
        _sessao = sessao;
        _erro = null;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() => _erro = e.toString());
    }
  }

  Future<void> _mudarStatus(StatusSessao status) async {
    setState(() => _acaoEmCurso = true);
    try {
      final atualizada = await _service.atualizarStatus(widget.sessaoId, status);
      if (!mounted) return;
      setState(() => _sessao = atualizada);
      // Mantém a lista da tela anterior coerente.
      context.read<SessoesProvider>().carregar(silencioso: true);
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text(e.toString())));
    } finally {
      if (mounted) setState(() => _acaoEmCurso = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Detalhes da sessão')),
      body: _buildBody(),
    );
  }

  Widget _buildBody() {
    if (_erro != null && _sessao == null) {
      return Center(child: Text(_erro!));
    }
    final sessao = _sessao;
    if (sessao == null) {
      return const Center(child: CircularProgressIndicator());
    }

    return RefreshIndicator(
      onRefresh: _carregar,
      child: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          Row(
            children: [
              StatusChip(sessao.status),
              const Spacer(),
              if (sessao.status == StatusSessao.pendente)
                const _DicaPolling(),
            ],
          ),
          const SizedBox(height: 20),
          _Campo(rotulo: 'Descrição', valor: sessao.descricao),
          const SizedBox(height: 16),
          _Campo(
            rotulo: 'Ouvinte',
            valor: sessao.ouvinteId == null
                ? 'Ainda não atribuído'
                : 'Ouvinte vinculado (${sessao.ouvinteId})',
          ),
          const SizedBox(height: 16),
          _Campo(rotulo: 'Criada em', valor: _formatarData(sessao.createdAt)),
          const SizedBox(height: 16),
          _Campo(
            rotulo: 'Última atualização',
            valor: _formatarData(sessao.updatedAt),
          ),
          if (sessao.avaliacao != null) ...[
            const Divider(height: 32),
            _Campo(
              rotulo: 'Avaliação',
              valor:
                  '${'⭐' * sessao.avaliacao!.nota} (${sessao.avaliacao!.nota}/5)'
                  '${sessao.avaliacao!.comentario != null ? '\n${sessao.avaliacao!.comentario}' : ''}',
            ),
          ],
          const SizedBox(height: 32),
          ..._acoes(sessao),
        ],
      ),
    );
  }

  List<Widget> _acoes(Sessao sessao) {
    final widgets = <Widget>[];

    if (sessao.status == StatusSessao.emAndamento) {
      widgets.add(
        FilledButton.icon(
          onPressed: _acaoEmCurso
              ? null
              : () => _mudarStatus(StatusSessao.concluida),
          icon: const Icon(Icons.check_circle_outline),
          label: const Text('Concluir sessão'),
        ),
      );
      widgets.add(const SizedBox(height: 12));
    }

    if (!sessao.status.isTerminal) {
      widgets.add(
        OutlinedButton.icon(
          onPressed:
              _acaoEmCurso ? null : () => _mudarStatus(StatusSessao.cancelada),
          style: OutlinedButton.styleFrom(foregroundColor: Colors.red),
          icon: const Icon(Icons.cancel_outlined),
          label: const Text('Cancelar sessão'),
        ),
      );
    }

    return widgets;
  }

  String _formatarData(DateTime data) {
    final l = data.toLocal();
    String dois(int n) => n.toString().padLeft(2, '0');
    return '${dois(l.day)}/${dois(l.month)}/${l.year} ${dois(l.hour)}:${dois(l.minute)}';
  }
}

class _Campo extends StatelessWidget {
  final String rotulo;
  final String valor;

  const _Campo({required this.rotulo, required this.valor});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          rotulo,
          style: TextStyle(
            color: Colors.grey[600],
            fontSize: 12,
            fontWeight: FontWeight.w600,
          ),
        ),
        const SizedBox(height: 4),
        Text(valor, style: const TextStyle(fontSize: 16)),
      ],
    );
  }
}

class _DicaPolling extends StatelessWidget {
  const _DicaPolling();

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        SizedBox(
          height: 12,
          width: 12,
          child: CircularProgressIndicator(
            strokeWidth: 2,
            color: Colors.grey[400],
          ),
        ),
        const SizedBox(width: 8),
        Text(
          'Aguardando ouvinte…',
          style: TextStyle(color: Colors.grey[600], fontSize: 12),
        ),
      ],
    );
  }
}
