# quiniela-zubillaga-api


Auth Done

1. Route Update GAMES ADMIN 

2. Route para ingresar predictions cumpliendo restrictions de hora check!

3. Route para devolver todas tus predictions ingresadas armando Listo

4. Function ya se cron job o ui para actualizar el score de los usuarios en base a los predicitons y los nuevos resultados

5. Crear table view para ranking de puntages [{'Name': "amando", "Puntos": 50}] Listo

6. View para ver los scores 

7. SI hay tiempo, change en la table de resultados dependiendo cambio de puntos


waitress-serve --listen=*:8000 main:app


Prediction rules:
group stage
1. si adivinas marcador 5 puntos
2. si advinas ganador o empate 3 puntos
3. suma de goles 2

read excel team a team b or team b vs team a -> update score agarro predictions associated -> llamo get_score para calcular puntos -> update score en users


* Command to upload games:
  *  flask --app manage.py init_games --file data/partidos.csv
