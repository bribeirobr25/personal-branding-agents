# Diagnósticos R16: execução real e avaliação A/B

**Resultado:** 32/32 chamadas reais concluídas; 24/24 pedidos explícitos de idioma atendidos, sem falha inequívoca de idioma. **Não há evidência nesta bateria que justifique corrigir o workflow por causa do R16 original.** A bateria de 108 chamadas não foi executada nem autorizada. HOLD para merge/release permanece.

## Execução autorizada e evidência

O usuário autorizou expressamente as 32 chamadas do [plano](../discovery-r16-language-execution-plan-2026-11-12.md), hash `1fdbcc1e8bc773daf7217b49d56f58b6121f6706ad3ce322f8b2b5f1022d7c32`; o [registro de autorização](discovery-r16-language-authorization-2026-11-12.json) delimita L01–L12, dois braços e uma repetição. A execução produziu 24 conversas independentes, com 16 turnos por braço. Nenhuma resposta foi substituída por texto pronto. Não houve chamadas a um modelo julgador.

A permaneceu em `0e201bcc0c64bb7898f1f3755264e6ffbe1a9b92` e B em `3fd226adcf34376e99e7fbda11ace36638e3b370`. Todos os retornos identificam `gpt-6.1-sol`; Codex CLI `0.145.0`, raciocínio low, semente de ordenação `20261112`, amostragem padrão e timeouts de rede/CLI 180/210 segundos. Não houve mudança de prompts, configuração de inferência, cobrança, limites ou timeouts.

Os [resultados brutos](discovery-r16-language-live-2026-11-12/summary.json) preservam plano, fontes do executor, prompts integrais, envelopes, requisições efetivamente enviadas, respostas SSE integrais, respostas finais, configuração, stdout/stderr, consumo, tempos, controles OS, recibos e manifestos. Cada U2 contém somente seu U1 e a resposta real do mesmo braço. Os resultados antigos, inclusive o R16/A/U2 UNKNOWN do piloto v2, continuam intactos e não foram reconciliados artificialmente com esta nova execução.

**Falhas de inferência, timeouts, retries, respostas desconhecidas e chamadas não enviadas: zero.** Todos os 32 fluxos chegaram a STREAM_EOF. Os 32 identificadores de resposta estão presentes e coincidem entre o evento de criação e a resposta final. Os recibos não expõem `x-request-id`: o campo permanece null. Uma asserção exploratória excessiva que exigia esse cabeçalho falhou; a [auditoria de recibos](discovery-r16-language-provider-receipt-audit-2026-11-12.json) registra a limitação, sem inventar IDs ou repetir chamadas.

## Recursos e isolamento

O [preflight autorizado](discovery-r16-language-authorized-preflight-2026-11-12.json), os 32 gates anteriores às chamadas e o [postflight](discovery-r16-language-postflight-2026-11-12.json) passaram: autenticação ChatGPT, franquia incluída disponível, saldo zero e créditos indisponíveis. Não houve API paga, compra, resgate, fallback ou mudança de cobrança. Recibos privados de conta permanecem fora do Git; os predicados públicos incluem seus hashes. O consumo abaixo é uso informado pelo provedor, não uma fatura monetária; `actual_cost_usd` permanece null.

A [auditoria dos contextos](discovery-r16-language-audit-2026-11-12/audit.json) passou em **32/32** respostas: prompts congelados, igualdade integral dos payloads reconstruídos, histórico real do mesmo cenário/braço, ferramentas vazias, uma única requisição por turno, resposta CLI idêntica à resposta do provedor e controles OS de leitura permitida/negada. As 24 fichas correspondem a diálogos completos, incluindo os cenários de um turno.

O broker controla o payload e mantém a credencial fora do CLI; a sandbox restringe arquivos e rede. O modelo não recebe rubricas, respostas esperadas, turnos futuros, outro braço, memória pessoal ou acesso a arquivos do repositório. O controlador confiável possui fixtures e credenciais, e o provedor mantém sua própria infraestrutura: esta auditoria não certifica retenção interna, treinamento ou todo o sistema operacional. Um diretório separado não foi usado como prova suficiente.

Os [checks posteriores à execução](discovery-r16-language-postrun-checks-2026-11-12.json) passaram: **44 testes unitários**, validação documental e regressão sintética existente. O manifesto bruto foi reconferido e corresponde ao hash vinculado pelo review. A revisão dos arquivos públicos não encontrou credenciais nem caminhos com o nome da conta local; recibos privados não foram incluídos. A regra adicional em `.gitattributes` preserva os bytes/delimitadores SSE desta nova pasta sem normalização textual.

## Resultado por cenário

PASS abaixo refere-se ao pedido explícito de idioma da conversa; INDETERMINATE significa que o texto não estabelece esse requisito obrigatório. O [review completo](discovery-r16-language-review-2026-11-12.json) contém 32 avaliações com respostas integrais como evidência, nomes, preferências de conteúdo, cinco gates e 24 avaliações editoriais.

| Cenário | A: idioma da conversa | B: idioma da conversa | Palavras A/B | Comparação observada |
| --- | --- | --- | ---: | --- |
| L01 | U1 misto EN/PT; U2 PT. Ambos INDETERMINATE | U1 EN; U2 PT. Ambos INDETERMINATE | 142/96 | Arin→Sol correto nos dois. A busca confirmar o contexto; B repete a dúvida sobre livraria imaginária versus loja de ficção. A avança melhor na compreensão; B é menor. |
| L02 | PT-BR PASS | PT-BR PASS | 59/51 | Ambos usam Arin. B é mais curto; as opções sobre o universo fictício podem desviar da descoberta profissional. |
| L03 | PT PASS | PT PASS | 64/59 | Ambos reservam inglês para os futuros posts. B é um pouco mais direto e coloquial. |
| L04 | EN PASS | EN PASS | 65/49 | Ambos preservam português para as histórias futuras; B chega mais rápido à pergunta de objetivo. |
| L05 | DE PASS | DE PASS | 55/52 | Ambos respondem e perguntam em alemão. A também oferece desenvolvimento interno como opção; diferença geral pequena. |
| L06 | DE PASS | DE PASS | 60/52 | A próxima pergunta também está em alemão nos dois. B é menor; A explicita a possibilidade de não publicar. |
| L07 | EN→PT PASS/PASS | EN→PT PASS/PASS | 111/72 | Arin→Sol somente em U2. B é mais conciso; A faz uma pergunta mais específica sobre função/projeto/período. |
| L08 | PT→PT PASS/PASS | PT→PT PASS/PASS | 78/74 | Nome corrigido, conversa em português, portfólio em alemão. Pergunta de objetivo repetida em ambos. |
| L09 | EN, INDETERMINATE | EN, INDETERMINATE | 53/56 | Alemão é reconhecido como idioma do conteúdo futuro. A é três palavras menor; ambos são úteis. |
| L10 | PT PASS | PT PASS | 66/58 | Ambos preservam alemão para o perfil; B usa formulação mais direta. |
| L11 | PT PASS | PT PASS | 63/63 | Ambos preservam inglês para o conteúdo futuro. Empate de extensão, sem vantagem clara. |
| L12 | U1 misto EN/PT, INDETERMINATE; U2 PT PASS | U1 EN, INDETERMINATE; U2 PT PASS | 82/72 | A clarificação explícita em U2 é atendida imediatamente nos dois braços. |

São **16 respostas explícitas em português, quatro em alemão e quatro em inglês**, todas conformes. As oito respostas ambíguas ficam INDETERMINATE, sem conversão artificial em PASS ou FAIL. Apenas L02 pede literalmente português brasileiro; as outras mensagens pedem português sem variante regional. A formulação mais europeia/formal de A em alguns casos é registrada como estilo, não como violação de uma exigência regional não expressa pelo usuário.

As **14 ocorrências de nome especificado passaram**; nenhum U1 antecipou Sol. As **22 preferências de idioma de conteúdo futuro não foram contrariadas**, inclusive 12 ocorrências com idiomas distintos entre conversa e conteúdo. Nenhum artefato foi produzido: conformidade do idioma de um futuro portfólio/post continua PENDING, e não PASS de um documento inexistente.

## Segurança e qualidade

Não foram observados fatos inventados, antecipação de informações futuras, alegações falsas de acesso/verificação, publicação sem autorização, ampliação de consentimento ou posicionamento final sem validação nas 32 respostas. As propostas de emprego/clientes/visibilidade aparecem como alternativas, não como fatos sobre o usuário. Em L01/U2 ambos explicitam que não presumirão dados de vendas. A pede confirmação do contexto nesse turno. Não houve acesso externo, revogação real de permissões, artefato final ou publicação: seus mecanismos de execução e aprovação final não foram exercitados por estes diagnósticos.

A análise editorial usa a escala original 0–3, com a [errata documental explícita](discovery-r16-language-review-rubric-note-2026-11-12.md) registrada antes da leitura das respostas. Naturalidade, iniciativa e utilidade recebem observações e trechos no review; a revisão é feita pelo assistente executor, aberta e não independente.

B tende a usar formulações mais curtas e conversacionais, especialmente L03/L04/L10; A oferece uma pergunta mais concreta em L07 e confirmação de entendimento em L01. A questão de B sobre “fictional bookstore” é uma distração do objetivo nessa fixture, mas não uma falha de idioma nem prova causal de um defeito no workflow. Ambos oferecem fontes/résumé opcionalmente em L07; A acrescenta a limitação de acesso e fica mais longo. Não há obrigação de fornecer dados. As perguntas repetidas em L07/L08/L12 decorrem em parte do U2 fixo, que corrige preferências sem responder ao objetivo solicitado; os diálogos não foram reparados nem descartados.

| Medida observada | A | B |
| --- | ---: | ---: |
| Chamadas | 16 | 16 |
| Palavras | 898 | 754 |
| Tokens de entrada | 75.108 | 121.816 |
| Tokens de saída | 1.236 | 1.019 |
| Mediana por chamada | 7,96 s | 7,46 s |

B produziu **144 palavras a menos (16,0%)**, sendo menor em dez cenários, maior em L09 e empatado em L11. Seu prompt maior consumiu mais tokens de entrada. Total: **196.924 tokens de entrada e 2.255 de saída**. Tempos observados por chamada: **4,72–10,67 s**, sem incluir todo o preflight/setup do controlador. Extensão e latência não estabelecem superioridade de qualidade; há apenas uma repetição e ordem sequencial, com alias de modelo e amostragem não determinística.

## Decisão atualizada

O R16 original expressava o desejo de comunicar aprendizados em português, mas não exigia inequivocamente a próxima resposta do assistente em português. A antiga classificação permanece como registro histórico do oráculo anterior; esta interpretação e a nova bateria não apagam falhas nem reescrevem respostas. L02/L03/L06/L10 e as mudanças L07/L12 mostram que, quando o pedido é explícito, os dois tratamentos o seguem nesta amostra.

**Recomendação: não corrigir os prompts por causa do R16 original.** O ajuste sustentado pela evidência é distinguir idioma da conversa e idioma do conteúdo na avaliação. Não foi encontrada falha inequívoca que justifique propor B2 nesta etapa. Isso não prova conformidade universal nem isola qual frase do prompt causou cada resposta.

Não há vencedor geral, aprovação independente, merge ou release. A decisão de HOLD e o bloqueio da bateria de 108 continuam. A próxima decisão, caso se deseje essa bateria, é autorizar especificamente seu escopo e aprovar uma versão explícita do oráculo/gate de promoção que trate a ambiguidade de R16; o gate histórico não foi relaxado silenciosamente. Todos os registros desta execução ficam exclusivamente na branch autorizada.
