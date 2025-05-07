# Scout de Futevôlei
**_Aplicação interativa para coleta e análise de dados de jogos de futevôlei._**

Este projeto permite registrar eventos de jogo (fundamentos, ações, resultados, erros) diretamente de um vídeo, gerando uma planilha automática para análises posteriores no Excel, Power BI ou Python.

## Funcionalidades
- Upload de vídeo do jogo
- Marcação de eventos em tempo real (fundamento, ação, erro, resultado, observações)
- Geração de planilha (`.xlsx`) com todos os eventos marcados
- Interface amigável construída com Streamlit
- Pronta para deploy gratuito via Streamlit Cloud

## Como usar

### 1. Clonar o repositório
```bash
git clone https://github.com/seu-usuario/scout-futevolei.git
cd scout-futevolei

2. Instalar dependências

Recomenda-se usar ambiente virtual:

pip install -r requirements.txt

3. Rodar localmente

streamlit run scout_app.py

4. Ou acessar a versão online

(Se já foi publicado)

https://seu-usuario.streamlit.app

Campos disponíveis no app

Tempo de evento (automático)

Jogador (1 ou 2)

Fundamento: recepção, levantamento, ataque, saque, defesa, cobertura

Ação usada (livre)

Resultado: ponto a favor, ponto contra, continua

Erro não forçado: sim/não

Observações: quantidade de rallys, movimentaçoes, etc


Exportação

Os dados são exportados automaticamente para um arquivo Excel chamado:

Scout_Eventos_Jogo.xlsx

Tecnologias utilizadas:

Python 3
Streamlit
OpenCV
Pandas 
openpyxl


Contribuição

Sugestões, melhorias e PRs são bem-vindos. Ideal para atletas, técnicos, pais e analistas
que querem trazer estatística e dados para o futevôlei.


---
Feito com resenha, suor e paixão pelo jogo.
