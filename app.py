from flask_mail import Mail, Message
from flask import Flask, render_template, request, redirect, session, flash, send_from_directory
import sqlite3
import os
import random
import hashlib
from werkzeug.utils import secure_filename


app = Flask(__name__)
# EMAIL CONFIGURATION

app.config['MAIL_SERVER'] = 'smtp.gmail.com'

app.config['MAIL_PORT'] = 587

app.config['MAIL_USE_TLS'] = True

app.config['MAIL_USERNAME'] = 'kamakshitak4@gmail.com'

app.config['MAIL_PASSWORD'] = 'fnmb yrdc psqa quka'

mail = Mail(app)
app.secret_key = "cyber_secret_key"

# =========================
# DATA SEED (MIGRATED FROM REACT)
# =========================

SCAMS_DATA = [
    {
        "id": 10,
        "title": "Courier / Customs Scams",
        "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=600&h=400&q=80",
        "desc": "Scammers pose as customs or courier companies claiming a package addressed to you contains illegal items, demanding a 'penalty' to avoid police action.",
        "tips": [
            "Do not pay penalties for packages you didn't order.",
            "Verify directly with the official courier company.",
            "Customs officials do not demand money via WhatsApp."
        ]
    },
    {
        "id": 1,
        "title": "AI Voice & Deepfake Scams",
        "image": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?auto=format&fit=crop&w=600&h=400&q=80",
        "desc": "Scammers use AI to clone voices of loved ones or create deepfake videos to simulate distress (e.g., accidents, arrests) and demand immediate fund transfers.",
        "tips": [
            "Establish a family 'safe word'.",
            "Call back the person on their original known number.",
            "Never send money in a state of panic."
        ]
    },
    {
        "id": 2,
        "title": "Malicious APK (App) Drops",
        "image": "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?auto=format&fit=crop&w=600&h=400&q=80",
        "desc": "Fraudsters send APK files via WhatsApp disguised as banking rewards or system updates. Once installed, malware steals OTPs and empties accounts.",
        "tips": [
            "Never install apps from unverified sources or APK files.",
            "Only use Google Play Store or Apple App Store.",
            "Keep 'Install from Unknown Sources' disabled."
        ]
    },
    {
        "id": 3,
        "title": "UPI 'Collect Request' Fraud",
        "image": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?auto=format&fit=crop&w=600&h=400&q=80",
        "desc": "Scammers claiming to send you money will ask you to enter your UPI PIN. Entering your PIN approves a deduction from your account, not a deposit.",
        "tips": [
            "UPI PIN is ONLY used to SEND money, never to receive.",
            "Ignore unknown payment requests on UPI apps.",
            "Verify the receiver's details before paying."
        ]
    },
    {
        "id": 4,
        "title": "Mule Account Recruitment",
        "image": "https://images.unsplash.com/photo-1601597111158-2fceff292cdc?auto=format&fit=crop&w=600&h=400&q=80",
        "desc": "Fake 'Work from Home' jobs ask you to receive funds in your bank account and transfer them elsewhere, turning you into a money mule for illicit funds.",
        "tips": [
            "Never allow strangers to use your bank account.",
            "Be wary of jobs requiring no skills but offering high pay.",
            "Report suspicious account activity immediately."
        ]
    },
    {
        "id": 5,
        "title": "Investment & Crypto Scams",
        "image": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=600&h=400&q=80",
        "desc": "Fraudulent platforms promise guaranteed, massive returns on crypto or stock investments, only to vanish once you deposit your capital.",
        "tips": [
            "Verify if the platform is SEBI registered.",
            "If it sounds too good to be true, it is.",
            "Do independent research before investing."
        ]
    },
    {
        "id": 6,
        "title": "Sextortion / Romance Scams",
        "image": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=600&h=400&q=80",
        "desc": "Fake profiles lure victims into intimate video calls, record the screen, and then extort money by threatening to leak the video to family and friends.",
        "tips": [
            "Do not accept random video calls from unknown numbers.",
            "Keep social media profiles locked/private.",
            "If blackmailed, do not pay. Report to police immediately."
        ]
    },
    {
        "id": 7,
        "title": "Phishing & Smishing",
        "image": "https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=600&h=400&q=80",
        "desc": "Fake SMS/Emails claiming your PAN/Bank account will be blocked unless you click a link and update your KYC details immediately.",
        "tips": [
            "Never click on links received in unsolicited SMS.",
            "Banks will never ask for OTP/PIN via SMS links.",
            "Visit the official bank app or branch for updates."
        ]
    },
    {
        "id": 8,
        "title": "E-Commerce Fraud Sites",
        "image": "https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?auto=format&fit=crop&w=600&h=400&q=80",
        "desc": "Heavily discounted luxury items advertised on social media lead to fake checkout pages that steal credit card information or never deliver goods.",
        "tips": [
            "Check the website URL for spelling errors.",
            "Look for independent customer reviews.",
            "Prefer Cash on Delivery (COD) for new sites."
        ]
    },
    {
        "id": 9,
        "title": "Tech Support Scams",
        "image": "https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=600&h=400&q=80",
        "desc": "Fake pop-ups appear on your computer claiming it is infected with a virus, urging you to call a toll-free number where scammers ask for remote access.",
        "tips": [
            "Never call numbers from browser pop-ups.",
            "Do not give remote desktop access to strangers.",
            "Use legitimate antivirus software."
        ]
    }
]

NEWS_DATA = [
    {
        "id": 1,
        "title": "I4C & RBI Join Forces to Curtail Mule Accounts using AI",
        "date": "May 12, 2026",
        "category": "Policy & Tech",
        "image": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=600&q=80",
        "summary": "The Indian Cyber Crime Coordination Centre (I4C) signed an MoU with the Reserve Bank Innovation Hub to use an AI-driven system to detect and cull hidden mule accounts used in cyber frauds.",
        "link": "https://pib.gov.in/"
    },
    {
        "id": 2,
        "title": "Alert: Malicious WhatsApp APK Scams Lead to Heavy Losses",
        "date": "May 16, 2026",
        "category": "Threat Alert",
        "image": "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?auto=format&fit=crop&w=600&q=80",
        "summary": "A homemaker in Bengaluru lost over ₹4.4 lakh after inadvertently downloading an APK file sent on WhatsApp. Authorities warn against downloading files outside official app stores.",
        "link": "https://cybercrime.gov.in/Webform/Crime_NodalGrivanceList.aspx"
    },
    {
        "id": 3,
        "title": "NCRB Data: Cybercrime Up by 18%, Fraud Biggest Motive",
        "date": "May 07, 2026",
        "category": "Report",
        "image": "https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&w=600&q=80",
        "summary": "Cases of cybercrime jumped by 18% in the latest reporting period. Financial frauds and cheating remain the highest motive, increasingly targeting Tier-2 and Tier-3 cities.",
        "link": "https://ncrb.gov.in/en/crime-in-india"
    },
    {
        "id": 4,
        "title": "New 'MuleHunter.ai' Deployed to Detect Digital Frauds",
        "date": "May 13, 2026",
        "category": "Innovation",
        "image": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=600&q=80",
        "summary": "A new AI tool helps in proactive detection of money laundering channels, severely crippling the infrastructure used by cybercriminals to move stolen funds quickly across different bank accounts.",
        "link": "https://i4c.mha.gov.in/"
    },
    {
        "id": 5,
        "title": "CERT-In Issues High Severity Warning for Android Users",
        "date": "May 15, 2026",
        "category": "Advisory",
        "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=600&q=80",
        "summary": "The Indian Computer Emergency Response Team (CERT-In) has reported multiple vulnerabilities in older Android versions, urging users to immediately update their devices.",
        "link": "https://www.cert-in.org.in/"
    },
    {
        "id": 6,
        "title": "CBI Busts International Tech Support Scam Call Center",
        "date": "May 10, 2026",
        "category": "Law Enforcement",
        "image": "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?auto=format&fit=crop&w=600&q=80",
        "summary": "A joint operation by the CBI and local police dismantled a massive illegal call center defrauding foreign and domestic nationals by posing as tech support representatives.",
        "link": "https://cbi.gov.in/press-releases"
    },
    {
        "id": 7,
        "title": "SEBI Proposes New Framework to Curb 'Finfluencer' Scams",
        "date": "May 05, 2026",
        "category": "Policy & Tech",
        "image": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=600&q=80",
        "summary": "The Securities and Exchange Board of India aims to strictly regulate unregistered financial influencers promoting high-risk crypto assets and unverified investment schemes on social media.",
        "link": "https://www.sebi.gov.in/"
    },
    {
        "id": 8,
        "title": "DoT Blocks 1.5 Lakh Numbers Linked to Cyber Fraud",
        "date": "April 28, 2026",
        "category": "Action Taken",
        "image": "https://images.unsplash.com/photo-1544654803-b69140b285a1?auto=format&fit=crop&w=600&q=80",
        "summary": "Under the Sanchar Saathi initiative, the Department of Telecom has deactivated thousands of SIM cards obtained using forged documents to conduct financial frauds.",
        "link": "https://sancharsaathi.gov.in/"
    },
    {
        "id": 9,
        "title": "500+ Fake E-Commerce Websites Taken Down Ahead of Sales",
        "date": "April 22, 2026",
        "category": "Threat Alert",
        "image": "https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?auto=format&fit=crop&w=600&q=80",
        "summary": "Cyber authorities have proactively blocked hundreds of fraudulent domains offering unbelievably heavy discounts on luxury items to protect consumers from phishing and financial theft.",
        "link": "https://cybercrime.gov.in/"
    }
]


# =========================
# UPLOAD FOLDER
# =========================

UPLOAD_FOLDER = "uploads"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# =========================
# DATABASE CONNECTION
# =========================

def get_db_connection():

    conn = sqlite3.connect('database.db')

    conn.row_factory = sqlite3.Row

    return conn


# =========================
# DATABASE TABLES
# =========================

def init_db():

    conn = get_db_connection()

    cur = conn.cursor()

    # USERS TABLE
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    ''')

    # ADMINS TABLE
    cur.execute('''
    CREATE TABLE IF NOT EXISTS admins(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    ''')

    # COMPLAINTS TABLE
    cur.execute('''
    CREATE TABLE IF NOT EXISTS complaints(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        complaint_id TEXT,
        category TEXT,
        priority TEXT,
        description TEXT,
        evidence TEXT,
        status TEXT DEFAULT 'Pending'
    )
    ''')

    # Ensure COMPLAINTS table has all columns (Migration for existing DBs)
    cur.execute("PRAGMA table_info(complaints)")
    columns = [row[1] for row in cur.fetchall()]
    
    new_cols = {
        'incident_date': 'TEXT DEFAULT ""',
        'suspect': 'TEXT DEFAULT ""',
        'amount': 'REAL DEFAULT 0.0',
        'resolution_note': 'TEXT DEFAULT ""',
        'action_taken': 'TEXT DEFAULT ""',
        'resolved_by': 'TEXT DEFAULT ""',
        'resolved_at': 'TEXT DEFAULT ""',
        'admin_comment': 'TEXT DEFAULT ""'
    }
    
    for col_name, col_type in new_cols.items():
        if col_name not in columns:
            cur.execute(f"ALTER TABLE complaints ADD COLUMN {col_name} {col_type}")

    # COMPLAINT UPDATES (HISTORY) TABLE
    cur.execute('''
    CREATE TABLE IF NOT EXISTS complaint_updates(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        complaint_id TEXT,
        status TEXT,
        note TEXT,
        updated_by TEXT,
        updated_at TEXT
    )
    ''')

    # COMPLAINT MESSAGES (CONVERSATION) TABLE
    cur.execute('''
    CREATE TABLE IF NOT EXISTS complaint_messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        complaint_id TEXT,
        sender TEXT,
        sender_name TEXT,
        message TEXT,
        sent_at TEXT
    )
    ''')
    
    # CONTACTS TABLE
    cur.execute('''
    CREATE TABLE IF NOT EXISTS contacts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        message TEXT
    )
    ''')
    
    # SAMPLE ADMIN
    admin = cur.execute(
        "SELECT * FROM admins WHERE username='admin'"
    ).fetchone()

    if not admin:

        cur.execute(
            "INSERT INTO admins(username,password) VALUES(?,?)",
            ('admin', 'admin123')
        )

    conn.commit()
    conn.close()


init_db()


# =========================
# JINJA TEMPLATE FILTERS
# =========================

@app.template_filter('file_md5')
def get_file_md5(filename):
    if not filename:
        return "N/A"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        try:
            hasher = hashlib.md5()
            with open(filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            return hasher.hexdigest().upper()
        except Exception:
            return "ERROR_COMPUTING_HASH"
    return "FILE_NOT_FOUND"


# =========================
# SERVE UPLOADED EVIDENCE
# =========================

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# =========================
# HOME PAGE
# =========================

@app.route('/')
def home():
    return render_template('index.html')


# =========================
# REGISTER
# =========================

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']

        email = request.form['email']

        password = request.form['password']

        conn = get_db_connection()

        cur = conn.cursor()

        try:

            cur.execute(
                "INSERT INTO users(name,email,password) VALUES(?,?,?)",
                (name, email, password)
            )

            conn.commit()

            flash("Registration Successful")

            return redirect('/login')

        except:

            flash("Email already exists")

        conn.close()

    return render_template('register.html')


# =========================
# USER LOGIN
# =========================

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']

        password = request.form['password']

        conn = get_db_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        ).fetchone()

        conn.close()

        if user:

            session['user_id'] = user['id']

            session['user_name'] = user['name']

            return redirect('/track')

        else:

            flash("Incorrect Email or Password")

    return render_template('login.html')


# =========================
# ADMIN LOGIN
# =========================

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():

    if request.method == 'POST':

        username = request.form['username']

        password = request.form['password']

        conn = get_db_connection()

        admin = conn.execute(
            "SELECT * FROM admins WHERE username=? AND password=?",
            (username, password)
        ).fetchone()

        conn.close()

        if admin:

            session['admin'] = admin['username']

            return redirect('/admin')

        else:

            flash("Incorrect Admin Credentials")

    return render_template('admin_login.html')


# =========================
# USER DASHBOARD
# =========================

@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db_connection()

    complaints = conn.execute(
        "SELECT * FROM complaints WHERE user_id=? ORDER BY id DESC",
        (session['user_id'],)
    ).fetchall()

    total = len(complaints)

    pending = len([
        c for c in complaints
        if c['status'] == 'Pending'
    ])

    resolved = len([
        c for c in complaints
        if c['status'] == 'Resolved'
    ])
    investigation = len([
    c for c in complaints
    if c["status"] == "Investigation"
])

    # Get history log for user's complaints
    updates = conn.execute(
        '''
        SELECT cu.* FROM complaint_updates cu
        JOIN complaints c ON cu.complaint_id = c.complaint_id
        WHERE c.user_id = ?
        ORDER BY cu.id DESC
        ''',
        (session['user_id'],)
    ).fetchall()

    updates_by_complaint = {}
    for u in updates:
        c_id = u['complaint_id']
        if c_id not in updates_by_complaint:
            updates_by_complaint[c_id] = []
        updates_by_complaint[c_id].append(u)

    conn.close()

    return render_template(
        'dashboard.html',
        complaints=complaints,
        total=total,
        pending=pending,
        resolved=resolved,
        investigation=investigation,
        updates_by_complaint=updates_by_complaint
    )


# =========================
# FILE COMPLAINT
# =========================

@app.route('/complaint', methods=['GET', 'POST'])
def complaint():

    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':

        category = request.form['category']
        priority = request.form['priority']
        description = request.form['description']
        incident_date = request.form.get('incident_date', '')
        suspect = request.form.get('suspect', '')
        amount_val = request.form.get('amount', '0')
        
        try:
            amount = float(amount_val) if amount_val else 0.0
        except ValueError:
            amount = 0.0

        complaint_id = "CC" + str(random.randint(1000,9999))

        file = request.files['evidence']

        filename = ""

        if file and file.filename != "":
            # Backend validation for format / extension
            allowed_extensions = {'png', 'jpg', 'jpeg', 'pdf', 'mp4'}
            orig_filename = file.filename
            if '.' not in orig_filename or orig_filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
                flash("Invalid file format. Allowed formats are: PNG, JPG, JPEG, PDF, MP4.")
                return redirect('/track')

            # Backend validation for file size (5MB limit)
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)
            if file_size > 5 * 1024 * 1024:
                flash("File size exceeds the 5MB limit. Please upload a smaller file.")
                return redirect('/track')

            filename = secure_filename(file.filename)

            file.save(
                os.path.join(
                    app.config['UPLOAD_FOLDER'],
                    filename
                )
            )

        conn = get_db_connection()
        
        conn.execute(
            '''
            INSERT INTO complaints
            (
                user_id,
                complaint_id,
                category,
                priority,
                description,
                evidence,
                incident_date,
                suspect,
                amount
            )
            VALUES(?,?,?,?,?,?,?,?,?)
            ''',
            (
                session['user_id'],
                complaint_id,
                category,
                priority,
                description,
                filename,
                incident_date,
                suspect,
                amount
            )
        )

        conn.commit()

        conn.close()

        flash("Complaint Submitted Successfully")

        return redirect('/track')

    return redirect('/track')


# =========================
# TRACK COMPLAINT
# =========================

@app.route('/track')
def track():

    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db_connection()

    complaints = conn.execute(
        '''
        SELECT complaints.*, users.name
        FROM complaints
        JOIN users ON complaints.user_id = users.id
        WHERE complaints.user_id=? ORDER BY complaints.id DESC
        ''',
        (session['user_id'],)
    ).fetchall()

    # Get history logs for track view
    updates = conn.execute(
        '''
        SELECT cu.* FROM complaint_updates cu
        JOIN complaints c ON cu.complaint_id = c.complaint_id
        WHERE c.user_id = ?
        ORDER BY cu.id DESC
        ''',
        (session['user_id'],)
    ).fetchall()

    updates_by_complaint = {}
    for u in updates:
        c_id = u['complaint_id']
        if c_id not in updates_by_complaint:
            updates_by_complaint[c_id] = []
        updates_by_complaint[c_id].append(u)

    # Get conversation messages for track view
    messages = conn.execute(
        '''
        SELECT cm.* FROM complaint_messages cm
        JOIN complaints c ON cm.complaint_id = c.complaint_id
        WHERE c.user_id = ?
        ORDER BY cm.id ASC
        ''',
        (session['user_id'],)
    ).fetchall()

    messages_by_complaint = {}
    for m in messages:
        c_id = m['complaint_id']
        if c_id not in messages_by_complaint:
            messages_by_complaint[c_id] = []
        messages_by_complaint[c_id].append(m)

    conn.close()

    return render_template(
        'track.html',
        complaints=complaints,
        updates_by_complaint=updates_by_complaint,
        messages_by_complaint=messages_by_complaint
    )


# =========================
# STANDALONE CITIZEN CASE VIEW
# =========================

@app.route('/track/case/<complaint_id>')
def citizen_case_detail(complaint_id):
    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db_connection()
    complaint = conn.execute(
        '''
        SELECT complaints.*, users.name
        FROM complaints
        JOIN users ON complaints.user_id = users.id
        WHERE complaints.complaint_id=? AND complaints.user_id=?
        ''',
        (complaint_id, session['user_id'])
    ).fetchone()

    if not complaint:
        conn.close()
        flash("Case not found or unauthorized access.")
        return redirect('/track')

    # Fetch updates for this complaint
    updates = conn.execute(
        "SELECT * FROM complaint_updates WHERE complaint_id=? ORDER BY id DESC",
        (complaint_id,)
    ).fetchall()

    # Fetch conversation messages for this complaint
    messages = conn.execute(
        "SELECT * FROM complaint_messages WHERE complaint_id=? ORDER BY id ASC",
        (complaint_id,)
    ).fetchall()

    conn.close()

    return render_template(
        'case_detail.html',
        c=complaint,
        updates=updates,
        messages=messages
    )


# =========================
# ADMIN DASHBOARD
# =========================

@app.route('/admin')
def admin_dashboard():

    if 'admin' not in session:
        return redirect('/admin_login')

    conn = get_db_connection()

    complaints = conn.execute(
        '''
        SELECT complaints.*, users.name
        FROM complaints
        JOIN users
        ON complaints.user_id = users.id
        ORDER BY complaints.id DESC
        '''
    ).fetchall()

    total = len(complaints)
    pending = len([
        c for c in complaints
        if c['status'] == 'Pending'
    ])

    resolved = len([
       c for c in complaints
       if c['status'] == 'Resolved'
    ])

    investigation = len([
       c for c in complaints
       if c['status'] == 'Investigation'
    ])

    # Fetch history of updates for all complaints to show timeline in admin
    updates = conn.execute("SELECT * FROM complaint_updates ORDER BY id DESC").fetchall()
    updates_by_complaint = {}
    for u in updates:
        c_id = u['complaint_id']
        if c_id not in updates_by_complaint:
            updates_by_complaint[c_id] = []
        updates_by_complaint[c_id].append(u)

    # Fetch all conversation messages for admin
    messages = conn.execute("SELECT * FROM complaint_messages ORDER BY id ASC").fetchall()
    messages_by_complaint = {}
    for m in messages:
        c_id = m['complaint_id']
        if c_id not in messages_by_complaint:
            messages_by_complaint[c_id] = []
        messages_by_complaint[c_id].append(m)

    conn.close()

    return render_template(
        'admin_dashboard.html',
        complaints=complaints,
        total=total,
        pending=pending,
        resolved=resolved,
        investigation=investigation,
        updates_by_complaint=updates_by_complaint,
        messages_by_complaint=messages_by_complaint
    )


# =========================
# STANDALONE ADMIN CASE VIEW
# =========================

@app.route('/admin/case/<complaint_id>')
def admin_case_detail(complaint_id):
    if 'admin' not in session:
        return redirect('/admin_login')

    conn = get_db_connection()
    complaint = conn.execute(
        '''
        SELECT complaints.*, users.name, users.email
        FROM complaints
        JOIN users ON complaints.user_id = users.id
        WHERE complaints.complaint_id=?
        ''',
        (complaint_id,)
    ).fetchone()

    if not complaint:
        conn.close()
        flash("Complaint dossier not found.")
        return redirect('/admin')

    # Fetch updates for this complaint
    updates = conn.execute(
        "SELECT * FROM complaint_updates WHERE complaint_id=? ORDER BY id DESC",
        (complaint_id,)
    ).fetchall()

    # Fetch messages for this complaint
    messages = conn.execute(
        "SELECT * FROM complaint_messages WHERE complaint_id=? ORDER BY id ASC",
        (complaint_id,)
    ).fetchall()

    conn.close()

    return render_template(
        'admin_case_detail.html',
        c=complaint,
        updates=updates,
        messages=messages
    )


# =========================
# UPDATE STATUS
# =========================

@app.route('/update_status/<int:id>', methods=['POST'])
def update_status(id):
    if 'admin' not in session:
        return redirect('/admin_login')

    status = request.form.get('status')
    action_taken = request.form.get('action_taken', '')
    resolution_note = request.form.get('resolution_note', '')
    admin_comment = request.form.get('admin_comment', '')
    
    import datetime
    resolved_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    resolved_by = session['admin']

    conn = get_db_connection()

    # Get complaint details to log history
    complaint = conn.execute(
         "SELECT complaint_id, user_id FROM complaints WHERE id=?",
         (id,)
    ).fetchone()
    if complaint:
        
        user = conn.execute(

          'SELECT email FROM users WHERE id = ?',

          (complaint['user_id'],)

        ).fetchone()

        user_email = user['email']
        complaint_id = complaint['complaint_id']
        
        # Update main complaint record
        conn.execute(
            '''
            UPDATE complaints
            SET status=?, action_taken=?, resolution_note=?, admin_comment=?, resolved_by=?, resolved_at=?
            WHERE id=?
            ''',
            (status, action_taken, resolution_note, admin_comment, resolved_by, resolved_at, id)
        )
       
        # =========================
        # DYNAMIC EMAIL SYSTEM
        # =========================

        subject = f"Complaint Status Updated - {status}"

        body = f"""

        Dear User,

        Your complaint status has been updated.

        Customer Request Number (CRN):
        {complaint_id}

        Current Status:
        {status}

        Action Taken:
        {action_taken}

        Resolution / Investigation Note:
        {resolution_note}

        Admin Instructions:
        {admin_comment}

        Updated By:
        {resolved_by}

        Updated At:
        {resolved_at}

        Cyber Secure Team

        """

        msg = Message(

            subject=subject,

            sender=app.config['MAIL_USERNAME'],

            recipients=[user_email]

        )

        msg.body = body

        mail.send(msg)
        
        # Log to timeline history table
        timeline_note = f"Action: {action_taken} | Note: {resolution_note} | User Instructions: {admin_comment}"
        conn.execute(
            '''
            INSERT INTO complaint_updates (complaint_id, status, note, updated_by, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ''',
            (complaint_id, status, timeline_note, resolved_by, resolved_at)
        )

        conn.commit()
        flash("Complaint resolution status updated successfully!")

    conn.close()

    referrer = request.referrer or ""
    if "/case/" in referrer:
        return redirect(referrer)
    return redirect('/admin')


# =========================
# SEND MESSAGE (CONVERSATION SYSTEM)
# =========================

@app.route('/send_message/<complaint_id>', methods=['POST'])
def send_message(complaint_id):
    if 'user_id' not in session and 'admin' not in session:
        return redirect('/login')

    message_text = request.form.get('message_text', '').strip()
    if not message_text:
        flash("Message content cannot be empty.")
        return redirect('/track' if 'user_id' in session else '/admin')

    import datetime
    sent_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    conn = get_db_connection()
    # Check if complaint exists
    complaint = conn.execute("SELECT user_id FROM complaints WHERE complaint_id=?", (complaint_id,)).fetchone()
    if not complaint:
        conn.close()
        flash("Complaint not found.")
        return redirect('/track' if 'user_id' in session else '/admin')

    if 'user_id' in session:
        sender = 'User'
        # Security check: User can only send messages to their own complaints
        if complaint['user_id'] != session['user_id']:
            conn.close()
            flash("Unauthorized access.")
            return redirect('/track')

        user = conn.execute("SELECT name FROM users WHERE id=?", (session['user_id'],)).fetchone()
        sender_name = user['name'] if user else session.get('user_name', 'Citizen')
    else:
        sender = 'Admin'
        sender_name = session['admin']

    conn.execute(
        '''
        INSERT INTO complaint_messages (complaint_id, sender, sender_name, message, sent_at)
        VALUES (?, ?, ?, ?, ?)
        ''',
        (complaint_id, sender, sender_name, message_text, sent_at)
    )

    # Human-like Auto-reply logic for User messages
    if sender == 'User':
        status_row = conn.execute("SELECT status FROM complaints WHERE complaint_id=?", (complaint_id,)).fetchone()
        if status_row:
            status = status_row['status']
            auto_reply = ""
            if status == 'Pending':
                auto_reply = "Thank you for the update. Your case is currently pending assignment. Our team will review your message shortly."
            elif status == 'Investigation':
                auto_reply = "We have received your update. The investigating officer will review this information as part of the ongoing investigation."
            elif status == 'Resolved':
                auto_reply = "This case has been marked as Resolved. Your message has been recorded for our records. If you require further assistance, please file a new complaint."
            
            if auto_reply:
                sent_at_auto = (datetime.datetime.now() + datetime.timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M")
                conn.execute(
                    '''
                    INSERT INTO complaint_messages (complaint_id, sender, sender_name, message, sent_at)
                    VALUES (?, ?, ?, ?, ?)
                    ''',
                    (complaint_id, 'Admin', 'System Auto-Reply', auto_reply, sent_at_auto)
                )

    conn.commit()
    conn.close()
    
    flash("Follow-up message sent successfully.")
    referrer = request.referrer or ""
    if "/case/" in referrer:
        return redirect(referrer)
    return redirect('/track' if 'user_id' in session else '/admin')


# =========================
# DELETE COMPLAINT
# =========================

@app.route('/delete/<int:id>')
def delete(id):

    conn = get_db_connection()

    # Get complaint_id first

    complaint = conn.execute(

        "SELECT complaint_id FROM complaints WHERE id=?",

        (id,)

    ).fetchone()


    if complaint:

        complaint_id = complaint['complaint_id']

        # Delete timeline history

        conn.execute(

            "DELETE FROM complaint_updates WHERE complaint_id=?",

            (complaint_id,)

        )

        # Delete conversation messages

        conn.execute(

            "DELETE FROM complaint_messages WHERE complaint_id=?",

            (complaint_id,)

        )

        # Delete main complaint

        conn.execute(

            "DELETE FROM complaints WHERE id=?",

            (id,)

        )

        conn.commit()

    conn.close()

    return redirect('/admin')


# =========================
# OTHER PAGES
# =========================

@app.route('/awareness')
def awareness():
    return render_template('awareness.html', scams=SCAMS_DATA)


@app.route('/sop')
def sop():
    return render_template('sop.html')


@app.route('/news')
def news():
    return render_template('news.html', news_list=NEWS_DATA)


@app.route('/about')
def about():
    return render_template('about.html')


# =========================
# CONTACT PAGE
# =========================

@app.route('/contact', methods=['GET', 'POST'])
def contact():

    if request.method == 'POST':

        name = request.form['name']

        email = request.form['email']

        message = request.form['message']

        conn = get_db_connection()

        conn.execute(
            '''
            INSERT INTO contacts
            (
                name,
                email,
                message
            )
            VALUES(?,?,?)
            ''',
            (
                name,
                email,
                message
            )
        )

        conn.commit()

        conn.close()

        flash("Message Submitted Successfully")

        return redirect('/contact')

    return render_template('contact.html')


# =========================
# LOGOUT
# =========================

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')


# =========================
# PRESENTATION SLIDES
# =========================

@app.route('/presentation')
def presentation():
    return render_template('presentation.html')


# =========================
# RUN FLASK
# =========================

if __name__ == '__main__':
    app.run(debug=True)