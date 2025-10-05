# Probe on Mars

API para controlar o movimento de sondas enviadas em missão para Marte para explorar um planalto estranhamente retangular.

## 🚀 Tecnologias Utilizadas

* **Python 3.11.2** – Linguagem principal
* **FastAPI** – Framework web
* **SQLAlchemy** – ORM para banco de dados
* **Alembic** – Migrations para banco de dados
* **Docker & Docker Compose** – Para containerização e desenvolvimento

## 🛠️ Instalação

Clone o repositório:

```bash
git clone https://github.com/AllanPS98/probe-on-mars.git
cd probe-on-mars
```

Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## 🐳 Rodando com Docker

Use o `docker-compose` para subir o ambiente:

OBS: crie um `.env`

```bash
DB_HOST="probe_on_mars_database"
```

```bash
docker-compose up --build
```

O serviço ficará disponível em `http://localhost:8000/docs`.

## 🧪 Testes

Para rodar os testes automatizados:

```bash
pytest --cov=src --cov-report=term-missing
```

Foram desenvolvidos testes unitários para cobrir 100% do código. Dentre eles, os testes dos controllers são os mais importantes, uma vez que neles possuem as regras para criação da malha e da sonda, além da parte de movimentação da sonda e de retorno das informações.

Como a parte principal é a movimentação da sonda, existem testes para mover para cima, mover para a esquerda, mover para a direita, mover para baixo, rotacionar para a esquerda, rotacionar para a direita, rotacionar para a esquerda duas vezes e rotacionar para a direita duas vezes. Esses testes de rotação com mais de um comando, é basicamente para verificar se o código iria se comportar corretamente nesses cenários com mais de um comando de rotação.

## 🔧 Como Usar Sem o Docker Compose

1. Inicie o servidor local:

```bash
export PYTHONPATH=$(pwd)
python src/main.py
```
OBS: O banco precisar estar rodando, então lembre-se de rodar o container dele. Caso ainda não tenha atualizado as migrations, use o comando:
```bash
alembic upgrade head
```

## 🛠️ Contribuindo

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit das alterações (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request