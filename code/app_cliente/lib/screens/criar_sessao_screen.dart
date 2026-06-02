import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../state/sessoes_provider.dart';

class CriarSessaoScreen extends StatefulWidget {
  const CriarSessaoScreen({super.key});

  @override
  State<CriarSessaoScreen> createState() => _CriarSessaoScreenState();
}

class _CriarSessaoScreenState extends State<CriarSessaoScreen> {
  final _formKey = GlobalKey<FormState>();
  final _descricaoCtrl = TextEditingController();
  bool _enviando = false;

  @override
  void dispose() {
    _descricaoCtrl.dispose();
    super.dispose();
  }

  Future<void> _enviar() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _enviando = true);
    try {
      await context.read<SessoesProvider>().criar(_descricaoCtrl.text.trim());
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Sessão criada! Aguardando um ouvinte.')),
      );
      Navigator.of(context).pop();
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text(e.toString())));
    } finally {
      if (mounted) setState(() => _enviando = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Nova sessão')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Text(
                'Conte como você está se sentindo. Um ouvinte disponível '
                'poderá aceitar sua sessão.',
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _descricaoCtrl,
                maxLines: 6,
                maxLength: 2000,
                decoration: const InputDecoration(
                  labelText: 'Como você está?',
                  alignLabelWithHint: true,
                  border: OutlineInputBorder(),
                ),
                validator: (v) => (v == null || v.trim().isEmpty)
                    ? 'Escreva uma breve descrição'
                    : null,
              ),
              const SizedBox(height: 16),
              FilledButton.icon(
                onPressed: _enviando ? null : _enviar,
                icon: _enviando
                    ? const SizedBox(
                        height: 20,
                        width: 20,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : const Icon(Icons.send),
                label: const Text('Abrir sessão'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
