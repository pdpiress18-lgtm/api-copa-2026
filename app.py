from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Libera o seu site no Netlify para acessar esses dados

# API pública da ESPN (Placares de Futebol ao Vivo)
URL_ESPN = "https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard"

@app.route('/resultados', methods=['GET'])
def buscar_resultados():
    try:
        # O robô vai na web buscar os dados
        resposta = requests.get(URL_ESPN)
        dados = resposta.json()
        
        jogos_formatados = []
        
        if 'events' in dados:
            for evento in dados['events']:
                competidores = evento['competitions'][0]['competitors']
                # Pega nomes e placares
                time_casa = competidores[0]['team']['name']
                gols_casa = competidores[0]['score']
                time_fora = competidores[1]['team']['name']
                gols_fora = competidores[1]['score']
                
                jogos_formatados.append({
                    "h": time_casa,
                    "a": time_fora,
                    "gh": gols_casa,
                    "ga": gols_fora
                })
                
        return jsonify(jogos_formatados)
    
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Necessário para rodar no servidor em nuvem
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
