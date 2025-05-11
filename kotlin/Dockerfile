FROM openjdk:11-jdk

# Install Kotlin compiler
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Download and install Kotlin
RUN wget -q https://github.com/JetBrains/kotlin/releases/download/v1.8.22/kotlin-compiler-1.8.22.zip && \
    unzip kotlin-compiler-1.8.22.zip && \
    rm kotlin-compiler-1.8.22.zip && \
    mv kotlinc /opt/ && \
    ln -s /opt/kotlinc/bin/kotlinc /usr/local/bin/kotlinc

WORKDIR /app
COPY KotlinSieve.kt .

RUN kotlinc KotlinSieve.kt -include-runtime -d KotlinSieve.jar

ENTRYPOINT ["java", "-jar", "KotlinSieve.jar"]