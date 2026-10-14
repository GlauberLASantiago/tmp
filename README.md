# TPM — Treinamento de Percepção Musical

Edição web do **módulo 1, versão 1.0, de 2004**, recuperada do CD fornecido. Autoria: Prof. Glauber Lúcio Alves Santiago, UFSCar. Os créditos originais atribuem a concepção pedagógica e a execução a Glauber e a navegação a Gidenilson Alves Santiago.

## Usar

Ative o som quando o player solicitar. Use o menu original para abrir os treinamentos de articulação, dinâmica, afinação, notas, intervalos, escalas, cadências e modulação. A lista acima do player também abre cada módulo e seus exercícios específicos.

As partituras, instruções, exercícios e gravações são os conteúdos recuperados. O jogo de notas mantém a identificação das notas executadas incorretamente, suas respostas e o teclado de referência. O piano de uma oitava, extra do CD, está na lista. O outro extra, Áudimus, possui um link na janela Sobre.

Reiniciar reabre o módulo selecionado; Menu original volta à introdução; Silenciar controla o som; Tela cheia amplia o player. O botão original Sair do treinamento retorna ao menu na edição web. No celular, a orientação horizontal facilita a leitura.

## Tecnologia e preservação

Os executáveis Windows eram projetores Macromedia Flash. Seus SWFs foram extraídos pelo rodapé do projetor, sem executar os EXEs. A inspeção PE do REA gerou a evidência `ev_75d70a1457d6f530f47ebf6f590e8152b083519211cb75281e6e2ea1bab4878c` para Abre.exe. Os limites de extração e hashes estão em `docs/flash-extraction.json`.

São 27 arquivos SWF, versões 5/6 e bytecode AVM1, com 321 definições de áudio MP3 incorporadas. Esse total inclui duplicações, não representa 321 gravações diferentes. Abre.swf e TPMmod1.swf são idênticos na fonte. O palco original é 800 × 600, exceto o piano, 550 × 400.

A edição executa os SWFs com **Ruffle 0.7.1**, distribuído localmente, e uma interface HTML/CSS/JavaScript. A navegação antiga para `_level0` foi adaptada em 57 ações para uma ponte `FSCommand:loadModule`, restrita à lista de arquivos locais conhecidos. Os destinos também usam a caixa correta para o GitHub Pages. Uma referência inexistente `ArtiAcent1.wav` foi corrigida para o símbolo incorporado `ArtiAcen1.wav` na quarta tela de acentos. Todos os demais conteúdos e instruções são preservados, incluindo cada payload de áudio. Os originais intactos estão em `assets/original/`.

O runtime permite os comandos necessários à navegação; o wrapper aceita somente módulos conhecidos e bloqueia abertura de URLs externas pelo player. As licenças do Ruffle estão em `vendor/ruffle/`. O conteúdo original mantém sua autoria.

O ZIP TPM.zip da pasta contém os mesmos módulos, e não adiciona arquivos MP3 independentes. Os documentos auxiliares de etiqueta e listagem musical não são necessários para executar os exercícios e não integram esta edição.

## Executar e verificar

Requer Node.js para servir e Python 3 para a comparação das películas:

```sh
npm start
python scripts/verify_flash_preservation.py assets/original assets --report docs/preservation-verification.json
```

Abra `http://127.0.0.1:4193/`. O verificador reproduz as alterações permitidas e compara os 27 arquivos byte a byte, validando as estruturas e a preservação dos 321 blocos de áudio. Manifestos e scripts de adaptação estão em `docs/` e `scripts/`.

Verificações no navegador incluem o menu, troca e retorno de submódulos de articulação, reprodução de áudio em Notas e Acento, avanço por resposta correta em Notas e ausência do erro de símbolo corrigido na quarta tela de Acento. A extração e a comparação não constituem execução nem comparação visual integral com o projetor Windows; nem todos os exercícios foram percorridos até o final.

GitHub Pages serve a raiz da branch main, sem etapa de compilação.
