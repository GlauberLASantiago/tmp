# Verificação da edição web

O arquivo final é a combinação de 57 alterações de roteamento para FSCommand:loadModule e uma correção de símbolo sonoro em ArtiAcent. A versão anterior que mudava somente a caixa dos links foi substituída. Manifestos finalizados: fscommand-route-manifest.json, audio-patch-manifest.json e preservation-verification.json.

Os 27 arquivos finais passaram na comparação byte a byte contra a transformação esperada dos originais, validação de comprimentos e tags e preservação dos 321 payloads de som. Os scripts de diagnóstico temporários usados para observar o áudio não integram o app publicado.

No navegador com Ruffle 0.7.1 foram observados:

- Introdução original de 2004 e menu de treinamentos.
- Carregamento visual de todos os módulos e exercícios específicos da lista.
- Menu Articulação → Staccato e retorno ao submenu pelo botão original.
- Reprodução do trecho e de uma tecla em Notas, com sinal Web Audio não nulo. Uma resposta correta avançou do exercício que pede uma nota errada para a próxima tela, que pede três; outro clique manteve a tela e gerou novo áudio.
- Quarta tela de Acento: o aviso de símbolo ArtiAcent1.wav inexistente foi observado antes da correção e deixou de ocorrer na variante corrigida. Também foi observado sinal de áudio durante a sequência.
- Oito teclas do piano acionadas, com saída Web Audio não nula.

Medidas temporárias do pico absoluto de amostras na saída Web Audio: Notas 0,399 e posteriormente 0,679; Acento 0,129; piano 0,597. São observações de geração de áudio pelo navegador, não uma auditoria acústica ou uma comparação de cada gravação com o Windows.

A tela cheia automática solicitada pelas películas não é forçada; há um botão explícito da interface web. Quit retorna ao menu. A navegação é aceita somente para nomes de módulos locais da lista permitida. A configuração Ruffle allowNetworking=all é necessária para que os FSCommands de navegação cheguem ao wrapper; openUrlMode=deny bloqueia a abertura de URLs externas pelo player.

Não foram percorridas todas as telas e respostas de todos os treinamentos até o final. Os conteúdos históricos, inclusive linguagem e contatos incorporados, permanecem nos arquivos originais.
