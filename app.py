from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

URL_ESPN = "https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard"

@app.route('/resultados', methods=['GET'])
def buscar_resultados():
    try:
        resposta = requests.get(URL_ESPN)
        dados = resposta.json()
        jogos_formatados = []

        if 'events' in dados:
            for evento in dados['events']:
                comp = evento['competitions'][0]
                
                # Pegando o status e o cronômetro
                status_state = evento['status']['type']['state'] # 'pre', 'in', 'post'
                clock = evento['status']['displayClock']
                
                if status_state == 'pre': status_jogo = 'PRE'
                elif status_state == 'in': status_jogo = 'LIVE'
                else: status_jogo = 'FT'

                # Pegando os times e placares
                time_casa = comp['competitors'][0]
                time_fora = comp['competitors'][1]

                # Lógica para contar cartões (ESPN geralmente coloca em statistics ou redCards)
                def contar_cartoes(dados_time):
                    cartoes = 0
                    if 'statistics' in dados_time:
                        for stat in dados_time['statistics']:
                            if stat['name'] in ['yellowCards', 'redCards']:
                                cartoes += int(stat.get('displayValue', 0))
                    # Fallback para cartões vermelhos diretos
                    cartoes += int(dados_time.get('redCards', 0))
                    return cartoes

                total_cartoes = contar_cartoes(time_casa) + contar_cartoes(time_fora)

                jogos_formatados.append({
                    "h": time_casa['team']['name'],
                    "a": time_fora['team']['name'],
                    "gh": time_casa.get('score', '0'),
                    "ga": time_fora.get('score', '0'),
                    "time": clock,
                    "status": status_jogo,
                    "cards": total_cartoes
                })
                
        return jsonify(jogos_formatados)
    
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
