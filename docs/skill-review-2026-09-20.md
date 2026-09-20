# Revisão das 27 skills — 20/09/2026

Revisão sequencial autorizada, com alterações locais para revisão humana. O objetivo é melhorar qualidade dos resultados, precisão técnica, proporcionalidade e verificabilidade. Não houve instalação das skills, publicação, commit, deploy ou alteração de contas externas.

## Alterações por skill

| Skill | Melhoria principal | Verificação específica |
|---|---|---|
| adk-developer | Handoff por estado explícito, limite no loop, contratos compatíveis com a versão do SDK. | Revisão dos exemplos e cenário de execução limitada; sem agente remoto executado. |
| agent-engine-deploy | Alvo de deployment explícito, APIs dependentes da versão, validação local/remota e rollback separados. | Revisão de imports/contratos e receita de update; deployment não executado. |
| agent-engine-ops | Telemetria comprovada por leitura, logs sem payloads sensíveis, escopo de CMEK e conectividade. | Revisão de cenários e referência de segurança; sem observabilidade real consultada. |
| agent-engine-sessions-memory | Adaptador ADK correto, isolamento de sessão e limites de TTL/deleção. | Conferência do código oficial do adaptador; receitas antigas de Memory Bank marcadas como pseudocódigo histórico, não APIs executáveis. |
| ai-studio-architect | Mapeamento por evidência, SDK atual, identidade e destino explícitos; template sem mudança global de projeto. | Dois testes Bash: dry run sem chamadas cloud e falha de consulta sem criação de conta. |
| app-security-audit | Limites de autorização, achados do estudo de caso separados de regras universais, validação de caminhos e identidade. | Revisão de cenários; nenhum alvo externo testado. |
| clarity-presenter | Narrativa e pares técnico/negócio proporcionais; marca, contagem e formato respeitados. | Revisão de instruções de exportação, dependências e critérios visuais; não foi renderizado um deck completo desta skill. |
| cloud-architecture-diagram | Tema claro/escuro, modo diagrama, notas, legenda, acessibilidade e referências específicas de Google Cloud/slides. | Exemplo de 11 slides inspecionado em cinco viewports, navegação/notas e geometria; validador de dados aprovado. |
| design-critique | Severidade por impacto e WCAG AA corrigido para 24 CSS px com exceções; screenshots não provam comportamento. | Conferência do WCAG e alinhamento do checklist. |
| design-system-management | Inventário de consumidores, aliases, estados, temas e migração verificável. | Cenário de alteração de tokens com consumidores existentes. |
| developer-growth-analysis | Cobertura, privacidade e atribuição humana explícitas. | Limites reais do coletor documentados: sessões atualizadas no período podem conter mensagens antigas; sem filtro de projeto ou respostas do modelo. |
| documentation | Comandos e contratos ancorados no repositório; exemplos não executados identificados. | Cenário de documentação/runbook sem inventar APIs ou evidência. |
| feature-spec | Escopo proporcional, critérios observáveis, metas separadas de baselines. | Cenário de alteração somente de interface, sem exigir banco/API desnecessários. |
| google-ads-funnel | Métricas com janela, moeda e atribuição; concentração e desperdício não presumidos. | Cenário de exportação e baixo volume; nenhuma conta Ads consultada ou alterada. |
| html-to-pptx | Editabilidade delimitada por tipo de objeto, instalação/captura corrigidas e autoria fornecida pelo usuário. | Build de PPTX sintético; ZIP/XML confirma texto nativo. Não comprova fidelidade visual geral. |
| research-skill-graph-agy | Lentes relevantes e profundidade solicitada; sem desacordo ou probabilidades fabricados. | Cenário de checagem curta; templates alinhados ao uso proporcional. |
| software-troubleshooter | Reprodução e hipóteses antes da correção; relatório proporcional e verificação do resultado. | Cenário de bug simples sem exigir duas soluções artificiais. |
| spring-boot-upgrader | Alvo e versão Java respeitados; namespaces Java SE e anotações Jackson preservados. | Conferência das fontes oficiais; nenhum aplicativo Spring migrado. |
| system-design | Carga e restrições explícitas, limites de falha, migração e estimativas identificadas. | Cenário de baixa carga sem impor cache, filas ou microsserviços. |
| technical-drawing | Dimensões críticas desconhecidas explicitadas; fórmula de obstrução e margem corrigidas. | Revisão algébrica: sombra = t·d/(h−t), para h>t e geometria especificada; sem validação física/estrutural. |
| using-git-worktrees | Base/branch verificadas, exclusão local sem commit automático, preservação de trabalho e remoção via Git. | Cenário com worktree suja e outro agente; referências sem remoção recursiva como atalho. |
| ux-copywriter | Texto recomendado direto, promessa coerente com a ação, placeholders/localização/acessibilidade. | Cenário de ação irreversível sem promessa falsa de desfazer. |
| visual-explainer | HTML/interatividade proporcionais, marca preservada, dependências offline e exportação honestas. | Cenário de tabela simples e formato solicitado; critérios de inspeção adicionados. |
| webapp-testing | Readiness da aplicação separado de TCP; helper rejeita portas ocupadas e não bloqueia por logs. | Seis testes de integração aprovados, também repetidos por revisão independente. |
| writing-plans | Etapas/testes proporcionais, commits somente quando autorizados, preservação de arquivos alheios. | Cenário de mudança pequena; template de plano alinhado. |
| zen-pitch | Evidência suficiente sem quotas arbitrárias, ferramentas/caminhos portáveis, fontes nas notas. | Revisão de instruções e referência de pesquisa; não foi renderizado um deck completo desta skill. |
| zen-presenter | Concisão como alvo, imagens estáveis, preferências existentes reaproveitadas, limites de exportação. | Busca por endpoints aleatórios obsoletos e alinhamento dos templates; placeholders de imagens exigem substituição. |

## Evidências executadas

- Validador `quick_validate.py` do skill-creator: **27/27 válidas**, com Python em UTF-8 no Windows.
- `python -m unittest discover -s skills/webapp-testing/tests -v`: **6/6 aprovados**. Cobrem porta ocupada, preflight de múltiplas portas, saída antecipada, timeout, saída volumosa e propagação do exit code do comando dependente.
- `python -m unittest discover -s skills/ai-studio-architect/tests -v`: **2/2 aprovados**, usando Git Bash via `BASH_EXECUTABLE`.
- Sintaxe: scripts JavaScript alterados com `node --check`, scripts shell alterados com `bash -n`, scripts/testes Python com `ast.parse`.
- `validate-data.cjs assets/example-data.js`: sem erros de endpoints, IDs, rotas, grupos ou enquadramento.
- PPTX sintético gerado e inspecionado como pacote OOXML: texto presente em shape nativo. Isso não substitui renderização em PowerPoint/LibreOffice.
- Links Markdown locais dos entrypoints inspecionados: os caminhos inexistentes encontrados são exemplos de saída/arquivos a gerar, não dependências empacotadas.
- `git diff --check`: sem erros de whitespace. Avisos de conversão LF/CRLF refletem a configuração local do Git.

Os testes do helper web usam processos foreground e readiness TCP IPv4. Não demonstram limpeza de daemons/orphans nem readiness funcional; o consumidor deve verificar a aplicação. As revisões por cenário avaliam instruções e referências, não equivalem a executar cada skill de ponta a ponta em produção.

## Fontes técnicas conferidas

- [Google Cloud icons](https://cloud.google.com/icons)
- [WCAG 2.2: Target Size Minimum](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) e [Enhanced](https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html)
- [Marp CLI: exportação e limites](https://github.com/marp-team/marp-cli#readme)
- [Google Gen AI JavaScript SDK](https://github.com/googleapis/js-genai)
- [Adaptador de sessões ADK](https://github.com/google/adk-python/blob/main/src/google/adk/sessions/vertex_ai_session_service.py)
- [Spring Boot 4 Migration Guide](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.0-Migration-Guide) e [System Requirements](https://docs.spring.io/spring-boot/system-requirements.html)

APIs, versões e suporte devem ser novamente conferidos quando as skills forem aplicadas. Alguns links antigos de Agent Engine redirecionam para páginas genéricas; resposta HTTP 200 não confirma a validade de uma receita.
