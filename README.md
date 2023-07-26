<h1>FRAMWORK: Flask</h1>

<h2>"Rodar"</h2>
Para que o site "rode" executar o código do ficheiro <a href="main.py">main.py</a>

<h2>Estrutura</h2>
<ol>
    <li>Fakepinterest</li>
        <ol>
            <li>static</li>
            <li>templates</li>
            <small>páginas</small>
            <li>__init__.py</li>
            <small>É onde se define o site(ficheiro obrigatório do flask)</small>
            <li>forms.py</li>
            <small>formulários</small>
            <li>models.py</li>
            <small>base de dados</small>
            <li>routes.py</li>
            <small>rotas</small>
        </ol>
</ol>

<h2>Base de dados</h2>
Instalar o Flask SQL Alchemy. Este é responsavel pela gestão de SQL que vai permitir a integração com o banco de dados.
<pre>
    pip install Flask-SQLAlchemy
</pre>
Após a sua instalação, cria-se o banco de dados no ficheiro __init__.py da seguinte forma:
<pre>
    from flask import Flask<br>
    <span style="color: green">from flask_sqlalchemy import SQLAlchemy</span><br>
    app = Flask(__name__)<br>
    <span style="color: green">app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.bd"<br>
    database = SQLAlchemy(app)</span><br>
    from Fakepinterest import routes<br>
</pre>

A seguir deve ser criado o ficheiro da base de dados, neste caso foi create_danck.py
<pre>
    from Fakepinterest import database, app<br>
    with app.app_context():<br>
        database.create_all()
</pre>
<p>Para que finalmente o ficheiro seja criado não se esqueça de "correr" o código deste mesmo ficheiro.</p>
<p>Assim é criada uma pasta chamada <b>instance</b>, para serem criadas as tabelas na base de dados precisamos 
defenir quais são no ficheiro <b>models.py</b>.</p> 
<p>Depois de definidas as tabelas e respetivas colunas, deve ser apagado o ficheiiro que se encontra na pasta
<b>instance</b>, e só depois executado novamente o ficheiro create_banck com a importação das models.</p>
<code>
    from Fakepinterest.models import User, Post
</code>
<p>Agora sim, ao abrir o ficheiro comunidade.bd em qualquer leitor de ficheiros de base de dados vais ver que já tens as tabelas criadas</p>

<h2>Sistema de Login</h2>
<p>Usa-se a ferramenta Flask Login que faz o gerênciamento de login para nós. Para isso funcionar
é necessário conseguir regênciar as senhas, para isso ser possivél, deve o site seja um site seguro.</p>
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
esta recebe o ‘id’ de um utilizador e tem de retornar quem é esse utilizador.</p>
<pre>
    @login_manager.user_loader
    def load_user(id_user):
        return User.query.get(int(id_user))
</pre>

<h3>Restrições</h3>
Concordas que a página de homepage pode ser vista por todos? Concorda também que a página de utilizador só deve ser vista por utilizadores logados?
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

<h3>Formulários</h3>
Para o utilizador poder fazer login e criar a sua conta é necessário a criação de formulários para esses fins. Por isso vamos criá-los no ficheiro <b>forms.py</b>
Será necessário a instalação de outra parte do flask o <b>Flask-WTF</b> que permite a criação de formulários de forma masi simples e fácil.
<pre>
    pip install Flask-WTF
</pre>
A seguir, faz-se a instalação que irá validar o email, <b>email_validator</b>.
<pre>
    pip install email_validator
</pre>
E com isto já é possivél a criação de formulários.

<h4>Implementação</h4>
Primeiramente deve importar o documento dos formulários ao documento de rotas, pois é nele que se vai fazer a gestão dos formulários.<br>
Ou seja, no ficheiro <b>forms.py</b> criam-se os formulários e nas rotas, <b>routes.py</b> diz-se que página vai ter X formulário.
<pre>
    ...
    from Fakepinterest.forms import formLogin, formSingUp #importanção dos formulários
    ...

    @app.route("/")
    def homepage():
        formlogin = FormLogin() # variavel que chama o formulário
        return render_template("homepage.html", form=formlogin) # adicionar o formulário à página
    
    @app.route("/singup")
    def singup():
        formSingUp = FormSingUp()
        return render_template("singup.html", form=formSingUp)
</pre>

<h2>Login</h2>
Como a página de Login vai receber os dados que o utilizador dá, temos de informar que esta página vai receber o metodo <b>POST</b> e <b>GET</b> 
para isso dizemos á rota que tem de permitir os metodos POST
<pre>
    ...
    @app.route("/", methods=["GET", "POST"])
    def homepage():
        formlogin = FormLogin()
        return render_template("homepage.html", form=formlogin)
</pre>

<h3>Como carregar os formulários no html?</h3>
<pre>
    <small>homepage.html</small>
    < form method="POST">
        {{ form.csrf_token }} <!-- {{ NomeFormulário.csrf_token }} ==== protege de ataques informáticos, em Laravel é como se fosse o @csrf -->
        {{ form.email.label() }} <!-- Ao colocar .label() informa que vai aparecer o texto que foi informado no ficheiro forms.py -->
        {{ form.email() }} <!-- {{ NomeFormulário.nomeVariavel }} -->
        {{ form.password.label() }}
        {{ form.password() }}
        {{ form.button_confirm }}
    < /form>
</pre>

<h2>Página criar conta</h2>
A página criar conta é parecida com a página de login, tem de se informar que categoria de methods ela vai receber
