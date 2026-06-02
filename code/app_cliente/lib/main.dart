import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'services/api_client.dart';
import 'services/auth_service.dart';
import 'services/sessao_service.dart';
import 'screens/login_screen.dart';
import 'state/auth_provider.dart';
import 'state/sessoes_provider.dart';

void main() {
  // Cliente HTTP único, compartilhado pelos serviços (carrega o token JWT).
  final api = ApiClient();
  final authService = AuthService(api);
  final sessaoService = SessaoService(api);

  runApp(
    MultiProvider(
      providers: [
        Provider<SessaoService>.value(value: sessaoService),
        ChangeNotifierProvider(create: (_) => AuthProvider(authService, api)),
        ChangeNotifierProvider(create: (_) => SessoesProvider(sessaoService)),
      ],
      child: const ListenApp(),
    ),
  );
}

class ListenApp extends StatelessWidget {
  const ListenApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Listen',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.teal),
        useMaterial3: true,
      ),
      home: const LoginScreen(),
    );
  }
}
