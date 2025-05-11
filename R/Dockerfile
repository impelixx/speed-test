# Используем официальный образ R
FROM r-base:latest

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    && rm -rf /var/lib/apt/lists/*

# Install R packages
RUN R -e "install.packages('jsonlite', repos='https://cran.rstudio.com/')" && \
    R -e "install.packages('R.utils', repos='https://cran.rstudio.com/')"

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем R скрипт
COPY r_sieve.R .

# Устанавливаем точку входа
ENTRYPOINT ["Rscript", "r_sieve.R"]