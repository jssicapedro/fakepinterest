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

<h2>SCSS e CSS</h2>
<p>Caso o CSS não esteja a corresponder ao SCSS, deve ser removido os ficheiros CSS e executar:</p>
<pre>sass Fakepinterest/static/scss:Fakepinterest/static/css</pre>
ou
<pre>sass --watch Fakepinterest/static/scss/comum.scss:Fakepinterest/static/css/comum.css</pre>

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

A seguir deve ser criado o ficheiro da base de dados, neste caso foi create_bank.py
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
<hr>
<h3>Resetar BD</h3>
<p>De modo a resetar toda a base de dados deves:</p>
<ol>
    <li>Apagar o ficheiro comunidade.bd (Fakepinterest/instance/comunidade.bd)</li>
    <li>Executar o ficheiro create_bank.py (Fakepinterest/create_bank.py)</li>
</ol>

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
A página criar conta é parecida com a página de login, tem de se informar que categoria de methods e que formulário vai receber.
<pre>
    @app.route("/singup", methods=["GET", "POST"])
    def singup():
        formSingUp = FormSingUp()
        return render_template("singup.html", form=formSingUp)
</pre>

<h2>Funcionalidades</h2>
<h3>Criar um novo utilizador</h3>
<pre>
    <span style="color: gray;">from flask import render_template, url_for,</span> redirect
    <span style="color: gray;">from Fakepinterest import app</span>, database, bcrypt
    from Fakepinterest.models import User, Post
    <span style="color: gray;">from flask_login import login_required</span>, login_user, logout_user
    <span style="color: gray;">@app.route("/singup", methods=["GET", "POST"])
    def singup():
    form_SingUp = FormSingUp()</span>
    if form_SingUp.validate_on_submit(): <span style="color: #84b6f4;"> # se todos os dados forem validos ao submeter </span><br>
        password = bcrypt.generate_password_hash(form_SingUp.password.data) <span style="color: #84b6f4;"># a password recebida vai ser encriptada </span><br>
        user = User( <span style="color: #84b6f4;"># a variavel user vai receber </span><br>
            name=form_SingUp.name.data, <span style="color: #84b6f4;"># o nome recebido </span><br>
            email=form_SingUp.email.data, <span style="color: #84b6f4;"> # o email recebido </span><br>
            password=password <span style="color: #84b6f4;"> # a password encriptada </span><br>
        )
        database.session.add(user) <span style="color: #84b6f4;"> # abre uma coneção com a BD, adiciona o novo utilizador  </span>
        database.session.commit() <span style="color: #84b6f4;"> # manda esse novo utilizador à BD </span>
        login_user(user, remember=True) <span style="color: #84b6f4;"> # executa automaticamente o novo utilizador e caso ele feche a janela do site continuará logado
        return redirect(url_for("userpage", user=user.name)) <span style="color: #84b6f4;"> # redireciona para a página de utilizador </span>
    <span style="color: gray;">return render_template("singup.html", form=form_SingUp)</span>
</pre>
<h3>Login</h3>
<pre>
    <span style="color: gray;">@app.route("/", methods=["GET", "POST"])
    def homepage():
    formlogin = FormLogin()</span>
    if formlogin.validate_on_submit(): <span style="color: #84b6f4;"># se todos os dados forem validos ao submeter</span>
        user = User.query.filter_by(email=formlogin.email.data).first() <span style="color: #84b6f4;">#variavel user recebe o email</span>
        if user and bcrypt.check_password_hash(user.password, formlogin.password.data): <span style="color: #84b6f4;"># se o email e a pass encriptada for igual á palavra passe que recebe então</span>
            login_user(user) <span style="color: #84b6f4;"># faz o login do utilizador</span>
            return redirect(url_for("userpage", user=user.name)) <span style="color: #84b6f4;"># redireciona para a página de utilizador</span>
    return render_template("homepage.html", form=formlogin)
</pre>
<h3>Logout</h3>
<pre>
    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("homepage"))
</pre>

<h3>Atualizar o perfil de utilizador</h3>
Para sabermos quando estamos no nosso perfil ou no perfil de outra pessoa é necessário comparar o user que vemos e o user que está logado
para isso é necessário fazer alguma alterações ao código que ja temos.

<pre>
    <span style="color: gray;">from flask import render_template, url_for, redirect
    from Fakepinterest import app, database, bcrypt
    from Fakepinterest.models import User, Post
    from Fakepinterest.forms import FormLogin, FormSingUp
    from flask_login import login_required, login_user, logout_user,</span> current_user
    
    <span style="color: gray;">@app.route("/", methods=["GET", "POST"])
    def homepage():
        formlogin = FormLogin()
        if formlogin.validate_on_submit():
            user = User.query.filter_by(email=formlogin.email.data).first()
            if user and bcrypt.check_password_hash(user.password, formlogin.password.data):
                login_user(user)
                return redirect(url_for("userpage", </span>id_user=user.id))
        <span style="color: gray;">return render_template("homepage.html", form=formlogin)
    
    @app.route("/singup", methods=["GET", "POST"])
    def singup():
        form_SingUp = FormSingUp()
        if form_SingUp.validate_on_submit():
            password = bcrypt.generate_password_hash(form_SingUp.password.data)
            user = User(
                name=form_SingUp.name.data,
                email=form_SingUp.email.data,
                password=password
            )
            database.session.add(user)
            database.session.commit()
            login_user(user, remember=True)
            return redirect(url_for("userpage",</span> id_user=user.id))
        <span style="color: gray;">return render_template("singup.html", form=form_SingUp)
    
    @app.route("/user/<id_user>")
    @login_required
    def userpage(id_user):</span>
        if int(id_user) == int(current_user.id): <span style="color: #84b6f4;"> # se o id do utilizador for igual ao current user (user logado), então</span>
            return render_template("user/user.html", user=current_user) <span style="color: #84b6f4;"> # retorna a página do utilizador logado</span>
        else: <span style="color: #84b6f4;"> # senão </span>
            user = User.query.get(int(id_user)) <span style="color: #84b6f4;"> # a variavel user recebe o id do url </span>
            return render_template("user/user.html", user=user) <span style="color: #84b6f4;"> # retorna a página do utilizador que procuramos </span>
    
    <span style="color: gray;">@app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("homepage"))</span>
</pre>
Com este código é possivel agora fazer alterações na página de utilizador de modo que, se for o current user na página de utilizador possam aparecer botões de edição de perfil e criação de posts.

<h3> Gestão de Imagens </h3>
Para a gestão de imagens é necessário fazer uma alteração no ficheiro <b>init</b>. Essa nova alteração fará com que sempre que haja um novo upload de imagem, esta será enviada para o diretório static/img_post. 
<pre>
    ...
    <span style="color: gray;">app = Flask(__name__, static_folder="static")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.bd"
    app.config["SECRET_KEY"] = "91079e75c7a25cd8672a"</span>
    app.config["UPLOAD_FOLDER"] = "static/img_posts"
</pre>
<h4>Postar Imagem</h4>