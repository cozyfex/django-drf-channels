FROM python:3.12-slim

WORKDIR /app

COPY . /app/

RUN rm -f .env
RUN rm -f .env.sample

SHELL ["/bin/bash", "-c"]

RUN pip install uv
RUN uv venv
RUN source .venv/bin/activate
RUN uv pip install --no-cache-dir -r requirements.txt

EXPOSE 8000 8001

CMD ["./deploy/docker_runner.sh"]
