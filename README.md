<h1>FRAMWORK: Flask</h1>

<h2>"Rodar"</h2>
<p>Para que o site "rode" executar o código do ficheiro <a href="main.py">main.py</a></p>

<h2>Estrutura</h2>
<ol>
    <li>Fakepinterest</li>
        <ol>
            <li>static</li>
            <li>templates</li>
            <small>páginas</small>
            <li>__init__.py</li>
            <small>É onde se define o site em sim(ficheiro obrigatório do flask)</small>
            <li>forms.py</li>
            <small>formulários</small>
            <li>models.py</li>
            <small>base de dados</small>
            <li>routes.py</li>
            <small>rotas</small>
        </ol>
</ol>

<h2>Base de dados</h2>
<p>Instalar o Flask SQL Alchemy. Este é responsavel pela gestão de SQL que vai permitir a integração com o banco de dados.</p>
<pre>
    pip install Flask-SQLAlchemy
</pre>
<p>Após a sua instalação, cria-se o banco de dados no ficheiro __init__.py da seguinte forma:<p>
<pre>
    from flask import Flask<br>
    <span style="color: green">from flask_sqlalchemy import SQLAlchemy</span><br>
    app = Flask(__name__)<br>
    <span style="color: green">app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.bd"<br>
    database = SQLAlchemy(app)</span><br>
    from Fakepinterest import routes<br>
</pre>

<p>De seguida deve ser criado o ficheiro da base de dados, neste caso foi create_danck.py</p>
<pre>
    from Fakepinterest import database, app<br>
    with app.app_context():<br>
        database.create_all()
</pre>
<p>Para que finalmente o ficheiro seja criado não te esqueças de "correr" o código deste mesmo ficheiro.</p>
<p>Assim é criada uma nova pasta chamada <b>instance</b>, para serem criadas as tabelas na base de dados precisamos 
defenir quais são no ficheiro <b>models.py</b>.</p> 
<p>Depois de definidas as tabelas e respetivas colunas, deve ser apagado o ficheiiro que se encontra na pasta
<b>instance</b>, e só depois executado novamente o ficheiro create_banck com a importação das models.</p>
<code>
    from Fakepinterest.models import User, Post
</code>
<p>Agora sim, ao abrires o ficheiro comunidade.bd em qualquer leitor de ficheiros de base de dados vais ver que já tens as tabelas criadas</p>

<h2>Sistema de Login</h2>
<p>Usa-se a ferramenta Flask Login que faz o gerênciamento de login para nós. Para isso funcionar
é necessário conseguir regênciar as senhas, para isso ser possivél é necessário que o site seja um site seguro.</p>
<p><b>Para isso...</b> vamos ter de instalar algumas coisas:</p>
<ol>
    <li>flask-login - gerencia as senhas</li>
    <li>flask-bcrypt - encripta as senhas</li>
</ol>
    <pre>pip install flask-login flask-bcrypt</pre>
<p>E vamos alterar o ficheiro <b>__init__.py</b></p>
<pre>

    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_login import  LoginManager
    from flask_bcrypt import Bcrypt

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.bd"
    app.config["SECRET_KEY"] = "91079e75c7a25cd8672a" # chave de segurança do site que vai usar como referência para garantir a segurança

    database = SQLAlchemy(app)
    bcrypt = Bcrypt(app)
    login_manager = LoginManager(app)
    login_manager.login_view = "homepage" # isto faz com que o utilizador seja redirecionado para a rota homepage
    
    from Fakepinterest import routes
</pre>
<p>Agora é necessário fazer algumas alterações no ficheiro de base de dados, <b>models.py</b>. Temos de importar a o UserMixin
e dizer que senha será usada para fazer login. Neste caso será a senha da tabela do utilizador.</p>
<p>Depois deve ser ir buscar o login_manager criado no ficheiro <b>__init__.py</b></p>
<p>Este precisa, <b>obrigatóriamente</b> de uma função, <b>load_tabelaUtilizador</b>, neste caso a load_user 
esta recebe o id de um utilizador e tem de retornar quem é esse utilizador.</p>
<pre>
    @login_manager.user_loader
    def load_user(id_user):
        return User.query.get(int(id_user))
</pre>

<h3>Restrições</h3>
Concordas que a página de homepage pode ser vista por todos? Concordas também que a página de utilizador só deve ser vista por utilizadores logados?
Para isso acontecer, a página de user deve ter restrições. Essas, podem ser feitas a partir do flask_login, o login_required
<pre>
    ...
    from flask_login import login_required

    ...
    
    @app.route("/user/<user>")
    @login_required
    def userpage(user):
        return render_template("user/user.html", user=user)
</pre>

<h3>Tela de Login</h3>
Para o utilizador poder fazer login e criar a sua conta é necessário a criação de formulários para esses fins. Por isso vamos cria-los em <b>forms.py</b>