// Teste de fumaça: garante que o app inicia na tela de login.

import 'package:flutter_test/flutter_test.dart';

import 'package:app_cliente/main.dart';

void main() {
  testWidgets('App inicia na tela de login', (WidgetTester tester) async {
    await tester.pumpWidget(const ListenApp());

    expect(find.text('Listen'), findsOneWidget);
    expect(find.text('Entrar'), findsOneWidget);
  });
}
