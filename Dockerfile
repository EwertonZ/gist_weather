FROM python:3.11-slim

# Instala o binário do uv diretamente
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copia os arquivos de definição
COPY pyproject.toml uv.lock ./

# Instala as dependências
RUN uv sync --frozen --no-cache --no-dev

COPY . .

EXPOSE 8000

# Executa usando o contexto do uv (garante que os pacotes instalados estejam no path)
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]