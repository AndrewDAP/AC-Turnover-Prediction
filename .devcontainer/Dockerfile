FROM python:3.10.12

# Install poetry
RUN pip install poetry==1.7.0
RUN poetry config virtualenvs.create false --local

# Install dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry install
RUN pip3 install --force-reinstall torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
