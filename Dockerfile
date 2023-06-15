FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

WORKDIR /app

# Install and configure Poetry
ENV POETRY_VERSION=1.4.2
RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false

# Install dependencies
COPY pyproject.toml .
RUN poetry install --no-root --without dev

# Copy the entry point
COPY app.py .

# Start the entrypoint
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]