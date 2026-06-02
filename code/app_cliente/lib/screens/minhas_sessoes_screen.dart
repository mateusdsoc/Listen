import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../state/auth_provider.dart';
import '../state/sessoes_provider.dart';
import '../widgets/sessao_card.dart';
import 'criar_sessao_screen.dart';
import 'detalhe_sessao_screen.dart';
import 'login_screen.dart';

class MinhasSessoesScreen extends StatefulWidget {
  const MinhasSessoesScreen({super.key});

  @override
  State<MinhasSessoesScreen> createState() => _MinhasSessoesScreenState();
}

class _MinhasSessoesScreenState extends State<MinhasSessoesScreen> {
  @override
  void initState() {
    super.initState();
    // Carrega a lista e inicia o polling após o primeiro frame.
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final provider = context.read<SessoesProvider>();
      provider.carregar();
      provider.iniciarPolling();
    });
  }

  @override
  void dispose() {
    context.read<SessoesProvider>().pararPolling();
    super.dispose();
  }

  void _logout() {
    context.read<SessoesProvider>().pararPolling();
    context.read<AuthProvider>().logout();
    Navigator.of(context).pushAndRemoveUntil(
      MaterialPageRoute(builder: (_) => const LoginScreen()),
      (_) => false,
    );
  }

  @override
  Widget build(BuildContext context) {
    final usuario = context.watch<AuthProvider>().usuario;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Minhas sessões'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            tooltip: 'Sair',
            onPressed: _logout,
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => Navigator.of(context).push(
          MaterialPageRoute(builder: (_) => const CriarSessaoScreen()),
        ),
        icon: const Icon(Icons.add),
        label: const Text('Nova sessão'),
      ),
      body: Column(
        children: [
          if (usuario != null)
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 12, 16, 0),
              child: Align(
                alignment: Alignment.centerLeft,
                child: Text('Olá, ${usuario.nome} 👋',
                    style: Theme.of(context).textTheme.titleMedium),
              ),
            ),
          Expanded(
            child: Consumer<SessoesProvider>(
              builder: (context, provider, _) {
                if (provider.carregando && provider.sessoes.isEmpty) {
                  return const Center(child: CircularProgressIndicator());
                }
                if (provider.erro != null && provider.sessoes.isEmpty) {
                  return _MensagemCentral(
                    icone: Icons.error_outline,
                    texto: provider.erro!,
                    acaoTexto: 'Tentar novamente',
                    onAcao: () => provider.carregar(),
                  );
                }
                if (provider.sessoes.isEmpty) {
                  return const _MensagemCentral(
                    icone: Icons.inbox_outlined,
                    texto:
                        'Você ainda não abriu nenhuma sessão.\nToque em "Nova sessão" para começar.',
                  );
                }
                return RefreshIndicator(
                  onRefresh: () => provider.carregar(silencioso: true),
                  child: ListView.builder(
                    padding: const EdgeInsets.only(top: 8, bottom: 88),
                    itemCount: provider.sessoes.length,
                    itemBuilder: (context, i) {
                      final sessao = provider.sessoes[i];
                      return SessaoCard(
                        sessao: sessao,
                        onTap: () => Navigator.of(context).push(
                          MaterialPageRoute(
                            builder: (_) =>
                                DetalheSessaoScreen(sessaoId: sessao.id),
                          ),
                        ),
                      );
                    },
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}

class _MensagemCentral extends StatelessWidget {
  final IconData icone;
  final String texto;
  final String? acaoTexto;
  final VoidCallback? onAcao;

  const _MensagemCentral({
    required this.icone,
    required this.texto,
    this.acaoTexto,
    this.onAcao,
  });

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icone, size: 56, color: Colors.grey),
            const SizedBox(height: 16),
            Text(texto, textAlign: TextAlign.center),
            if (acaoTexto != null) ...[
              const SizedBox(height: 16),
              FilledButton.tonal(onPressed: onAcao, child: Text(acaoTexto!)),
            ],
          ],
        ),
      ),
    );
  }
}
