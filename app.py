from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime, timezone
import pytz
import io
from dateutil import parser  # Para parsing robusto de datas

from models import db, User, Reading

# --- Configuração ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'segredo'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///glicemia.db'
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

# --- Context processor para ano atual ---
@app.context_processor
def inject_now():
    return {'current_year': datetime.now(pytz.timezone('America/Sao_Paulo')).year}

# --- Login Manager ---
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# --- Função para definir status ---
def classify_glucose(value):
    if value < 70:
        return "Hipoglicemia"
    elif 70 <= value <= 180:
        return "Normal"
    elif 180 < value <= 350:
        return "Acima do recomendado"
    else:
        return "Procure um hospital"

# --- Função para converter datas para timezone local ---
def to_localtime(dt, tz_str="America/Sao_Paulo"):
    if dt is None:
        return None
    tz = pytz.timezone(tz_str)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(tz)

# --- Rotas ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash("Cadastro realizado com sucesso!")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash("Usuário ou senha incorretos")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    readings = Reading.query.filter_by(user_id=current_user.id).order_by(Reading.when.desc()).all()

    readings_tz = [
        {
            'value': r.value,
            'status': r.status,
            'note': r.note,
            'when': to_localtime(r.when)
        }
        for r in readings
    ]

    latest = readings[0].value if readings else None
    latest_status = readings[0].status if readings else None
    out_of_range = latest is not None and (latest < 70 or latest > 180)

    return render_template(
        "dashboard.html",
        readings=readings_tz,
        latest=latest,
        latest_status=latest_status,
        out_of_range=out_of_range
    )

@app.route('/add', methods=['GET','POST'])
@login_required
def add_reading():
    if request.method == 'POST':
        value = float(request.form['value'])
        note = request.form.get('note')
        when_str = request.form.get('when_utc')

        status = classify_glucose(value)

        if when_str:
            when_dt = parser.isoparse(when_str)
            if when_dt.tzinfo is None:
                when_dt = pytz.timezone("America/Sao_Paulo").localize(when_dt)
            when_dt_utc = when_dt.astimezone(pytz.utc)
        else:
            when_dt_utc = datetime.utcnow().replace(tzinfo=pytz.utc)

        reading = Reading(value=value, note=note, user_id=current_user.id, status=status, when=when_dt_utc)
        db.session.add(reading)
        db.session.commit()

        flash(f"Medição registrada! Status: {status}")
        return redirect(url_for('dashboard'))

    return render_template("add_reading.html")

@app.route('/quemsomos')
def quemsomos():
    return render_template('quemsomos.html')

@app.route('/api/readings')
@login_required
def api_readings():
    readings = Reading.query.filter_by(user_id=current_user.id).order_by(Reading.when.asc()).all()

    return jsonify([
        {
            "when": to_localtime(r.when).isoformat(),
            "value": r.value
        } for r in readings
    ])

@app.route('/export_pdf')
@login_required
def export_pdf():
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 50, "Relatório de Glicemia")
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 80, f"Usuário: {current_user.email}")

    y = height - 120
    p.setFont("Helvetica-Bold", 10)
    p.drawString(100, y, "Data/Hora")
    p.drawString(220, y, "Valor (mg/dL)")
    p.drawString(320, y, "Status")
    p.drawString(420, y, "Observação")
    y -= 20

    readings = Reading.query.filter_by(user_id=current_user.id).order_by(Reading.when.desc()).all()
    p.setFont("Helvetica", 10)
    for r in readings:
        if y < 50:
            p.showPage()
            y = height - 50
            p.setFont("Helvetica", 10)
        p.drawString(100, y, to_localtime(r.when).strftime('%d/%m/%Y %H:%M'))
        p.drawString(220, y, str(int(r.value)))
        p.drawString(320, y, r.status if r.status else "-")
        p.drawString(420, y, r.note if r.note else "-")
        y -= 20

    p.showPage()
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="relatorio_glicemia.pdf", mimetype='application/pdf')

# --- Inicialização ---
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
