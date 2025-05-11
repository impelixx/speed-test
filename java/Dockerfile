FROM openjdk:17-jdk-slim

WORKDIR /app

COPY JavaSieve.java .

RUN javac JavaSieve.java

ENTRYPOINT ["java", "JavaSieve"]