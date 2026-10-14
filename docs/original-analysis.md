# TPM — evidências Flash

Fonte analisada: cópia de `CD TPM e Musicas Mp3/Dados` em `tmp-analysis/Dados`. Nenhum EXE foi executado. A extração lê os oito bytes finais do projetor Macromedia: inteiro little endian `0xfa123456`, seguido do tamanho da película SWF. Ambos os projetores têm cabeçalho nativo de 819200 bytes, SWF integral e rodapé de oito bytes. SHA-256 completos e os intervalos extraídos encontram-se em `flash-extraction.json`.

- `Abre.exe` (1152029 bytes) → `Abre.swf` (332821 bytes), SHA-256 `0385299791abbed2612c5562c4e872cc34df11bfd142aff43ce085ac69e85abc`.
- `PianoMelhor.exe` (1036493 bytes) → `PianoMelhor.swf` (217285 bytes), SHA-256 `90e7c39c4c5543530a1c6b88087e91a160bd3c0001c7f4b21dd4e5c473ebb235`.
- `Abre.swf` e o arquivo distribuído `TPMmod1.swf` são idênticos byte a byte. Abre não carrega TPMmod1 automaticamente; é a mesma película inicial de quatro quadros, cada quadro com Stop.

## Tecnologia e autoria

27 películas SWF: Flash versão 5, exceto `IntSegUniOit.swf`, versão 6. Todas usam AVM1, sem flag AVM2/ActionScript 3. O artefato permite afirmar a família ActionScript antiga, mas não distinguir com segurança qual sintaxe autoral ou versão da ferramenta de criação. Cursos/menu com palco 800×600; piano 550×400. FPS: 12, exceto ArtiAcent/ArtiLiga/ArtiStac/ArtiVari a 30 e ArtiTenu a 60.

Texto da introdução: “Treinamento de Percepção Musical”, “Módulo 1 versão 1.0 2004”. Autor Prof. Glauber Lúcio Alves Santiago, UFSCar/CECH/DAC. Créditos atribuem concepção pedagógica e execução a Glauber; navegação a Gidenilson Alves Santiago. As películas preservam contatos históricos que não precisam ser promovidos a novos links de interface.

321 definições de áudio MP3 estão embutidas nas 27 películas (o total inclui duplicação byte a byte do menu Abre/TPMmod1 e sons compartilhados por módulos). Não são 321 gravações distintas. Os nomes `.wav` nas ações são símbolos ExportAssets usados por Sound.attachSound, não caminhos de arquivos externos. Não foram encontrados ImportAssets nem carregamentos externos de áudio. Piano tem oito teclas/botões sonoros (DefineButtonSound), sem ações ou navegação.

## Rotas originais

Todas as rotas abaixo usam GetURL para `_level0`, realizando substituição da película principal dentro do player. A lista completa com ID de botão e destino está em `flash-summary.json` e `flash-dependencies.json`.

- Menu `Abre`/`TPMmod1` → Articulacao, Dina, Afinacao, Notas, Intervalo, Escala, Cadencia, Modulacao.
- Articulacao → ArtiStac, ArtiTenu, ArtiVari, ArtiLiga, **artiacent.swf**; retorno dos cinco exercícios → **articulacao.swf**. Os arquivos físicos chamam-se `ArtiAcent.swf` e `Articulacao.swf`, portanto o servidor web precisa de aliases ou reescrita desses dois nomes minúsculos.
- Afinacao → AfinacaoUni/Oit/Qui/Qua; exercícios voltam ao menu Afinacao; menu volta TPMmod1.
- Intervalo → IntFixo1458, IntFixo3MaMe, IntSegUniOit, IntSegQuaQui, IntJuntUniOit, IntJuntQuaQui, IntJunt3MaMe; exercícios voltam Intervalo; menu volta TPMmod1.
- Dina, Notas, Escala, Cadencia, Modulacao retornam a TPMmod1.

FSCommand observados: `fullscreen` com valor verdadeiro na abertura dos módulos; `quit` nos botões Sair do treinamento. A interface web deve tratar Quit como saída do treinamento/retorno ao início e Fullscreen como um pedido que precisa respeitar interação do navegador. Não foram encontrados FSCommand exec, links a PianoMelhor.exe, URLs de rede ou `javascript:`. Piano é recurso independente e deve ter acesso explícito na interface web.

## Exercícios e comportamento recuperado

O conteúdo não se limita a navegação e textos: as ações e botões são parte dos exercícios. `Notas.swf` instrui clicar nas notas executadas incorretamente do coral de J. S. Bach. O feedback original inclui “muito bem!” e “negativo!”, com repetição do trecho ao erro; cada tela pede uma quantidade de notas erradas, de uma a sete. São preservados teclado de referência, escala ascendente/descendente e dó sustentado.

ArtiAcent pede identificar qual pentagrama corresponde à audição, repetir e acompanhar a execução; há segunda série com sete alternativas. Outros módulos apresentam reconhecimento de intervalos, afinação, escalas, articulações, cadências e modulações. As instruções inteiras de cada módulo estão nos arquivos `*-texts.txt`; as ações completas ficam em `*-flash.json`. Atalhos Enter/próximo, barra de espaço/parar, anterior/tocar figuram na tela Dicas; botões condicionais da AVM1 devem permanecer ativos.

## Problemas já presentes no artefato

1. `Notas.swf` usa attachSound com `notacoro01.wav` etc., enquanto os símbolos exportados são `NotaCoro01.wav` etc. Isso é discrepância apenas de caixa. Flash AVM1 antigo pode tratar identificadores sem distinguir caixa; a reprodução em Ruffle deve ser confirmada antes de alterar qualquer símbolo.
2. `ArtiAcent.swf`, ação do **quadro 4**, tag DoAction offset descomprimido **1824027**, chama `ArtiAcent1.wav` (com t), enquanto ExportAssets só disponibiliza `ArtiAcen1.wav` (sem t). Este nome não tem correspondência mesmo ignorando caixa. É um provável defeito de reprodução do original. Caso seja corrigido para a web, preserve o SWF original e registre alteração exata e hash da variante, incluindo validação dos restantes payloads intactos.
3. Os nomes de rotas minúsculos de articulação exigem atenção no GitHub Pages, que distingue caixa.

## Limites e validação

Todos os SWFs foram descomprimidos se CWS, conferidos contra comprimento declarado, percorridos por tags raiz e sprites, e tiveram End tags e ausência de truncamento validadas. Arquivos descomprimidos, constantes, botões DefineButton2, tags de som e exportação foram analisados sem execução nativa. A investigação estática comprova que as ações existem e apontam a esses destinos; não comprova sozinha a compatibilidade de cada resposta/áudio com Ruffle. A validação final exige testes no navegador, sobretudo Notas, ArtiAcent quadro 4, teclas do piano, respostas corretas/incorretas e retorno dos submenus.

Scripts reproduzíveis: `analyze_flash.py` e `flash_dependencies.py`. JSONs não contêm código nativo do EXE. O conteúdo Flash integral extraído continua preservado em Dados.
