from flask import Flask, render_template, request, redirect, url_for, flash
from database import db, init_db, Denuncia, Estatistica
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)
app.secret_key = 'chave_secreta_bullying_2023'

# Inicializar banco de dados
init_db(app)

@app.route('/')
def index():
    # Buscar estatísticas do banco
    estatisticas = Estatistica.query.all()
    
    # Calcular dados para os gráficos
    denuncias = Denuncia.query.all()
    
    # Estatísticas por tipo
    tipos_count = {
        'bullying': len([d for d in denuncias if d.tipo == 'bullying']),
        'cyberbullying': len([d for d in denuncias if d.tipo == 'cyberbullying'])
    }
    
    # Dados para gráfico de tipos (valores simulados + reais)
    dados_tipos = {
        'Verbal': 35,
        'Social': 25,
        'Físico': 20,
        'Cyberbullying': 15 + tipos_count['cyberbullying'] * 2,
        'Outros': 5
    }
    
    # Dados para gráfico por faixa etária
    dados_idade = {
        '6-10 anos': 15,
        '11-14 anos': 40,
        '15-18 anos': 35,
        '19+ anos': 10
    }
    
    return render_template('index.html', 
                         estatisticas=estatisticas,
                         dados_tipos=dados_tipos,
                         dados_idade=dados_idade,
                         total_denuncias=len(denuncias))

@app.route('/denuncia', methods=['POST'])
def registrar_denuncia():
    if request.method == 'POST':
        try:
            # Coletar dados do formulário
            tipo = request.form['tipo']
            data_ocorrencia = datetime.strptime(request.form['data'], '%Y-%m-%d')
            local = request.form['local']
            descricao = request.form['descricao']
            envolvidos = request.form['envolvidos']
            testemunhas = request.form.get('testemunhas', '')
            contato = request.form.get('contato', '')
            anonimo = 'anonimo' in request.form
            
            # Criar nova denúncia
            nova_denuncia = Denuncia(
                tipo=tipo,
                data_ocorrencia=data_ocorrencia,
                local=local,
                descricao=descricao,
                envolvidos=envolvidos,
                testemunhas=testemunhas,
                contato=contato,
                anonimo=anonimo
            )
            
            # Salvar no banco
            db.session.add(nova_denuncia)
            db.session.commit()
            
            flash('Denúncia registrada com sucesso! ID: ' + str(nova_denuncia.id), 'success')
            
        except Exception as e:
            flash(f'Erro ao registrar denúncia: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/relatorio')
def relatorio():
    denuncias = Denuncia.query.all()
    
    # Estatísticas do relatório
    total_denuncias = len(denuncias)
    bullying_count = len([d for d in denuncias if d.tipo == 'bullying'])
    cyberbullying_count = len([d for d in denuncias if d.tipo == 'cyberbullying'])
    taxa_anonimato = len([d for d in denuncias if d.anonimo]) / total_denuncias * 100 if total_denuncias > 0 else 0
    
    # Locais mais comuns
    locais_count = defaultdict(int)
    for denuncia in denuncias:
        locais_count[denuncia.local] += 1
    
    locais_mais_comuns = dict(sorted(locais_count.items(), key=lambda x: x[1], reverse=True)[:3])
    
    return render_template('relatorio.html',
                         total_denuncias=total_denuncias,
                         bullying_count=bullying_count,
                         cyberbullying_count=cyberbullying_count,
                         taxa_anonimato=taxa_anonimato,
                         locais_mais_comuns=locais_mais_comuns,
                         denuncias=denuncias)

if __name__ == '__main__':
    app.run(debug=True, port=5000)