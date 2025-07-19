# Imagem base OpenJDK
FROM openjdk:17-jdk-alpine

# Diretório dentro do container
WORKDIR /app

# Copia o jar para dentro do container
COPY target/app.jar app.jar

# Expõe a porta da aplicação Spring Boot (geralmente 8080)
EXPOSE 8080

# Comando para rodar o jar
ENTRYPOINT ["java", "-jar", "app.jar"]
