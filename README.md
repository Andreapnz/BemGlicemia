# 🌸 BemGlicemia - Monitore sua glicemia com leveza 

![Python](https://img.shields.io/badge/Python-3.12-blue) ![Flask](https://img.shields.io/badge/Flask-2.x-orange) ![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey) ![Chart.js](https://img.shields.io/badge/Chart.js-4-lightblue) ![ReportLab](https://img.shields.io/badge/ReportLab-3.7-green)


BemGlicemia é um <strong>sistema web completo para monitoramento de glicemia</strong>, desenvolvido em Python com Flask, voltado para usuários com diabetes ou pessoas que desejam acompanhar seus índices glicêmicos ao longo do tempo. O sistema combina segurança, interface amigável e funcionalidades avançadas, como gráficos dinâmicos e relatórios em PDF.


## 🎨 Tecnologias Utilizadas

* **Backend:** Python, Flask
* **Frontend:** HTML5, CSS3, JavaScript, Bootstrap
* **Banco de Dados:** SQLite
* **Autenticação:** Flask-Login, Hash de senha com Werkzeug
* **Gráficos:** Chart.js
* **Relatórios PDF:** ReportLab
* **Timezone:** pytz para suporte a horários locais

---

## 🚀 Funcionalidades Principais

### 1️⃣ Cadastro e Login Seguro

* Registro de usuário com senha criptografada
* Login com verificação de hash
* Rotas protegidas com `@login_required`
* Logout seguro

### 2️⃣ Cadastro de Leitura de Glicemia

* Inserção de valor glicêmico, data e hora da medição
* Classificação automática do valor (normal, alto, baixo)
* Observações adicionais pelo usuário

```python
status = classify_glucose(value)
```

### 3️⃣ Dashboard Interativo

* Visualização das medições em **gráfico de linha**
* Datas e horas exibidas em **DD/MM/AAAA - HH\:mm**
* Gráfico responsivo e interativo com Chart.js

### 4️⃣ Relatórios em PDF

* Exportação de relatórios completos incluindo gráficos, tabelas e resumo
* Geração no timezone **America/Sao\_Paulo**

```python
p = canvas.Canvas(buffer, pagesize=A4)
```

### 5️⃣ Gerenciamento de Usuário

* Visualização de todas as leituras cadastradas
* Edição ou exclusão de leituras antigas
* Interface limpa e intuitiva

### 6️⃣ Limpeza e Validação de Formulário

* Campos resetáveis após cadastro
* Validação de valores e datas
* Mensagens de sucesso ou erro

---

## 📊 Estrutura de Arquivos

```
BemGlicemia/
│
├── app.py                # Aplicação principal Flask
├── templates/            # HTMLs (dashboard, login, cadastro)
├── static/
│   ├── css/              # Arquivos CSS
│   ├── js/               # Arquivos JS (gráficos)
│   └── images/           # Logos e ícones
├── database.db           # Banco SQLite
└── README.md
```

---

## 🔧 Como Rodar Localmente

1. Clone o repositório:

```bash
git clone https://github.com/Andreapnz/BemGlicemia.git
cd BemGlicemia
```

2. Crie e ative o ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute a aplicação:

```bash
python app.py
```

5. Acesse no navegador:

```
http://127.0.0.1:5000
```

---

## 📌 Observações Técnicas

* Datas e horários são convertidos para timezone local usando `pytz`
* Rotas protegidas garantem acesso apenas a usuários autenticados
* Gráficos renderizados com Chart.js; relatórios em PDF incluem gráficos e tabelas

---

## 💖 Contribuição

Contribuições são bem-vindas! Para reportar problemas ou sugerir melhorias, abra um **issue** ou envie um **pull request**.

---

## 🌈 Contato

Desenvolvido por:
 **Andréa Correia**
[GitHub](https://github.com/Andreapnz) | [LinkedIn](https://www.linkedin.com/in/andrea-correia-costa/)
 **Eunice M. Araujo**
[LinkedIn](https://www.linkedin.com/in/eunice-araujo/)
 **Liandra**
[GitHub](https://github.com/Andreapnz) | [LinkedIn](https://www.linkedin.com/in/liandra-lemos/))


