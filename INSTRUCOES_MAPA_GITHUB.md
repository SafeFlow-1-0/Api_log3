# SafeFlow — Mapa Interativo (código-fonte)

Extraído da versão `outputs/safeflow-map` do pacote de trabalho.

## Publicação
Copie o conteúdo da pasta `web/` para `web/` no repositório.
Não envie bases históricas, caches, arquivos de roteamento com endereços ou chaves de API sem revisão e autorização.

## Execução local
O mapa depende de arquivos na pasta `web/data/`, **não incluídos neste pacote** por cautela com dados operacionais.
Para execução com dados autorizados, mantenha a estrutura esperada pelos caminhos em `js/map.js`.
Em `web/`, execute `python iniciar_safeflow.py` ou `python -m http.server 8000` e acesse `http://localhost:8000`.

## Limites
As distâncias/tempos do TomTom representam estimativas da sede aos locais; não são rotas históricas observadas nem otimização das equipes.
O pacote preserva o código do mapa, mas não foi executado em teste ponta a ponta.
