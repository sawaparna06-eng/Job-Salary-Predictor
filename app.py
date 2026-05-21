import { useState } from "react";

const USERS_KEY = "salaryiq_users";

function getUsers() {
  try { return JSON.parse(localStorage.getItem(USERS_KEY) || "{}"); } catch { return {}; }
}
function saveUsers(u) { localStorage.setItem(USERS_KEY, JSON.stringify(u)); }
function hashPw(pw) {
  let h = 0;
  for (let i = 0; i < pw.length; i++) h = (Math.imul(31, h) + pw.charCodeAt(i)) | 0;
  return String(h);
}
function isValidEmail(e) { return /^[\w.\-]+@[\w.\-]+\.\w{2,}$/.test(e); }
function getInitials(name) {
  const p = name.trim().split(" ");
  return (p[0][0] + (p[1] ? p[1][0] : "")).toUpperCase();
}

// ─── Password strength ───
function pwStrength(pw) {
  let s = 0;
  if (pw.length >= 8) s++;
  if (/[A-Z]/.test(pw)) s++;
  if (/\d/.test(pw)) s++;
  if (/[^A-Za-z0-9]/.test(pw)) s++;
  return s;
}
const PW_COLORS = ["#ef4444", "#f97316", "#eab308", "#10b981"];
const PW_LABELS = ["Weak", "Fair", "Good", "Strong"];

// ─── Styles ───
const S = {
  page: {
    minHeight: "100vh", display: "flex", alignItems: "center",
    justifyContent: "center",
    background: "radial-gradient(ellipse 90% 70% at 15% 10%, rgba(92,61,232,.45) 0%, transparent 55%), radial-gradient(ellipse 60% 50% at 85% 85%, rgba(245,200,66,.10) 0%, transparent 55%), #0e0a25",
    padding: "32px 16px", boxSizing: "border-box", fontFamily: "'Inter', sans-serif",
  },
  card: {
    display: "flex", width: "100%", maxWidth: 820, minHeight: 540,
    borderRadius: 20, overflow: "hidden",
    boxShadow: "0 32px 80px rgba(0,0,0,.6)",
  },
  left: {
    width: "42%", minWidth: 240,
    background: "linear-gradient(160deg,#7c5af0 0%,#5c3de8 55%,#4a2abf 100%)",
    padding: "48px 36px 36px", display: "flex", flexDirection: "column",
    justifyContent: "space-between", position: "relative", overflow: "hidden",
  },
  leftOverlay: {
    position: "absolute", inset: 0,
    backgroundImage: "repeating-linear-gradient(-45deg,transparent,transparent 16px,rgba(255,255,255,.05) 16px,rgba(255,255,255,.05) 32px)",
    pointerEvents: "none",
  },
  leftInner: { position: "relative", zIndex: 1 },
  logo: { fontSize: 11, fontWeight: 800, letterSpacing: "2.5px", textTransform: "uppercase", color: "rgba(255,255,255,.5)", marginBottom: 40 },
  logoEm: { color: "#f5c842" },
  leftH2: { fontSize: 36, fontWeight: 800, color: "#fff", lineHeight: 1.15, marginBottom: 14, marginTop: 0 },
  leftP: { fontSize: 13, color: "rgba(255,255,255,.55)", lineHeight: 1.7, marginBottom: 0 },
  switchLbl: { fontSize: 12, color: "rgba(255,255,255,.38)", marginBottom: 10, marginTop: 28 },
  switchBtn: {
    display: "inline-block", padding: "9px 22px",
    border: "1.5px solid rgba(255,255,255,.45)", borderRadius: 8,
    fontSize: 13, fontWeight: 600, color: "#fff", cursor: "pointer",
    background: "transparent", fontFamily: "inherit",
  },
  stats: { display: "flex", gap: 24, paddingTop: 24, borderTop: "1px solid rgba(255,255,255,.12)", position: "relative", zIndex: 1 },
  statNum: { fontSize: 20, fontWeight: 800, color: "#f5c842", fontFamily: "inherit" },
  statLbl: { fontSize: 10, color: "rgba(255,255,255,.38)", textTransform: "uppercase", letterSpacing: ".7px", marginTop: 2 },
  right: {
    flex: 1, background: "#fff", padding: "44px 40px 36px",
    display: "flex", flexDirection: "column", justifyContent: "center", overflowY: "auto",
  },
  arHelp: { fontSize: 12, color: "#94a3b8", textAlign: "right", marginBottom: 20 },
  arTitle: { fontSize: 26, fontWeight: 800, color: "#5c3de8", marginBottom: 4, marginTop: 0 },
  arSub: { fontSize: 13, color: "#94a3b8", marginBottom: 20 },
  label: { fontSize: 12, fontWeight: 500, color: "#475569", display: "block", marginBottom: 6 },
  input: {
    width: "100%", padding: "11px 14px", fontSize: 14, color: "#0f172a",
    background: "#f8fafc", border: "1.5px solid #e2e8f0", borderRadius: 9,
    outline: "none", boxSizing: "border-box", marginBottom: 14, fontFamily: "inherit",
    transition: "border-color .2s",
  },
  inputFocus: { borderColor: "#5c3de8", boxShadow: "0 0 0 3px rgba(92,61,232,.10)", background: "#fff" },
  submitBtn: {
    width: "100%", padding: "13px", fontSize: 15, fontWeight: 600,
    background: "#5c3de8", color: "#fff", border: "none", borderRadius: 9,
    cursor: "pointer", fontFamily: "inherit", transition: "background .2s",
    boxShadow: "0 4px 18px rgba(92,61,232,.32)", marginBottom: 12,
  },
  orDiv: { textAlign: "center", color: "#cbd5e1", fontSize: 11, margin: "2px 0 10px", position: "relative" },
  linkBtn: {
    width: "100%", padding: "11px", fontSize: 13, fontWeight: 500,
    background: "transparent", color: "#5c3de8", border: "1.5px solid #e2e8f0",
    borderRadius: 9, cursor: "pointer", fontFamily: "inherit",
  },
  error: { background: "#fef2f2", border: "1px solid #fecaca", color: "#b91c1c", borderRadius: 8, padding: "10px 14px", fontSize: 13, marginBottom: 12 },
  success: { background: "#f0fdf4", border: "1px solid #bbf7d0", color: "#15803d", borderRadius: 8, padding: "10px 14px", fontSize: 13, marginBottom: 12 },
  // Main app
  appWrap: { minHeight: "100vh", background: "#f8f9fc", fontFamily: "'Inter', sans-serif" },
  topNav: {
    background: "#1a2236", padding: "0 clamp(16px,4vw,48px)",
    display: "flex", alignItems: "center", justifyContent: "space-between",
    height: 64, boxShadow: "0 2px 12px rgba(0,0,0,.25)", position: "sticky", top: 0, zIndex: 999,
  },
  navBrand: { fontSize: 22, fontWeight: 800, color: "#fff", fontFamily: "inherit" },
  navBrandEm: { color: "#f5a623" },
  navLinks: { display: "flex", alignItems: "center", gap: 24, flex: 1, justifyContent: "center" },
  navLink: { fontSize: 14, fontWeight: 500, color: "rgba(255,255,255,.75)", cursor: "pointer", padding: "4px 2px", borderBottom: "2px solid transparent", transition: "all .2s" },
  navLinkActive: { color: "#f5a623", borderBottomColor: "#f5a623" },
  navAvatar: { width: 32, height: 32, borderRadius: "50%", background: "linear-gradient(135deg,#f5a623,#e07b10)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 12, fontWeight: 700, color: "#fff" },
  logoutBtn: { background: "transparent", color: "#fff", border: "1.5px solid rgba(255,255,255,.45)", borderRadius: 6, padding: "7px 16px", fontSize: 13, fontWeight: 600, cursor: "pointer", fontFamily: "inherit" },
  pageWrap: { padding: "clamp(16px,3vw,28px) clamp(12px,3vw,36px)", maxWidth: 1100, margin: "0 auto" },
  pageTitle: { fontSize: 24, fontWeight: 800, color: "#0f172a", marginBottom: 4, marginTop: 0 },
  pageSub: { fontSize: 14, color: "#64748b", marginBottom: 20 },
  card: { background: "#fff", borderRadius: 16, border: "1px solid #e2e8f0", padding: "clamp(14px,2vw,22px)", boxShadow: "0 1px 3px rgba(0,0,0,.04)", marginBottom: 16 },
  cardTitle: { fontSize: 11, fontWeight: 700, color: "#6366f1", textTransform: "uppercase", letterSpacing: 1, marginBottom: 16, marginTop: 0 },
  heroResult: {
    background: "linear-gradient(135deg,#6366f1,#8b5cf6)", borderRadius: 20,
    padding: "clamp(20px,4vw,36px) clamp(16px,4vw,32px)", textAlign: "center",
    marginBottom: 20, boxShadow: "0 8px 32px rgba(99,102,241,.3)",
  },
  heroLbl: { fontSize: 12, color: "rgba(255,255,255,.7)", letterSpacing: "1.5px", textTransform: "uppercase" },
  heroAmt: { fontSize: "clamp(36px,8vw,56px)", fontWeight: 800, color: "#fff", margin: "8px 0" },
  heroSub: { fontSize: 13, color: "rgba(255,255,255,.6)" },
};

// ─── Input with focus state ───
function FInput({ label, ...props }) {
  const [focused, setFocused] = useState(false);
  return (
    <div>
      {label && <label style={S.label}>{label}</label>}
      <input
        style={{ ...S.input, ...(focused ? S.inputFocus : {}) }}
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
        {...props}
      />
    </div>
  );
}

// ─── LOGIN PAGE ───
function LoginPage({ onLogin, goSignup }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  function handleLogin() {
    setError("");
    if (!email || !password) return setError("Please fill in all fields.");
    if (!isValidEmail(email)) return setError("Please enter a valid email.");
    const users = getUsers();
    if (!users[email.toLowerCase()]) return setError("No account found with this email.");
    if (users[email.toLowerCase()].password !== hashPw(password)) return setError("Incorrect password.");
    onLogin(users[email.toLowerCase()].name, email.toLowerCase());
  }

  return (
    <div style={S.page}>
      <div style={S.card}>
        {/* LEFT */}
        <div style={S.left}>
          <div style={S.leftOverlay} />
          <div style={S.leftInner}>
            <div style={S.logo}>Salary<em style={S.logoEm}>IQ</em> Pro</div>
            <h2 style={S.leftH2}>Welcome<br />Back!</h2>
            <p style={S.leftP}>Sign in to your career intelligence dashboard and discover your true market value.</p>
            <div style={S.switchLbl}>Don't have an account?</div>
            <button style={S.switchBtn} onClick={goSignup}>Sign Up →</button>
          </div>
          <div style={S.stats}>
            {[["95%","Accuracy"],["50K+","Predictions"],["120+","Job Roles"]].map(([n,l]) => (
              <div key={l}><div style={S.statNum}>{n}</div><div style={S.statLbl}>{l}</div></div>
            ))}
          </div>
        </div>
        {/* RIGHT */}
        <div style={S.right}>
          <div style={S.arHelp}>Need help?</div>
          <h3 style={S.arTitle}>Log in</h3>
          <p style={S.arSub}>Enter your credentials to continue</p>
          {error && <div style={S.error}>{error}</div>}
          <FInput label="Email address" type="email" placeholder="you@example.com" value={email} onChange={e => setEmail(e.target.value)} />
          <FInput label="Password" type="password" placeholder="Your password" value={password} onChange={e => setPassword(e.target.value)} />
          <button style={S.submitBtn} onClick={handleLogin}>Log in</button>
          <div style={S.orDiv}>— or —</div>
          <button style={S.linkBtn} onClick={goSignup}>New user? Create a free account</button>
          <p style={{ textAlign: "center", fontSize: 11, color: "#94a3b8", marginTop: 14 }}>🔒 Your data is private and never shared.</p>
        </div>
      </div>
    </div>
  );
}

// ─── SIGNUP PAGE ───
function SignupPage({ onLogin, goLogin }) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [error, setError] = useState("");
  const [msg, setMsg] = useState("");

  const strength = password ? pwStrength(password) : 0;
  const pwColor = PW_COLORS[Math.max(0, strength - 1)];
  const pwLabel = PW_LABELS[Math.max(0, strength - 1)];

  function handleSignup() {
    setError(""); setMsg("");
    if (!name || !email || !password || !confirm) return setError("Please fill in all fields.");
    if (!isValidEmail(email)) return setError("Invalid email address.");
    if (password.length < 8) return setError("Password must be at least 8 characters.");
    if (password !== confirm) return setError("Passwords do not match.");
    const users = getUsers();
    if (users[email.toLowerCase()]) return setError("An account with this email already exists.");
    users[email.toLowerCase()] = { name: name.trim(), email: email.toLowerCase(), password: hashPw(password), createdAt: new Date().toISOString(), predictions: [] };
    saveUsers(users);
    setMsg("Account created! Logging you in…");
    setTimeout(() => onLogin(name.trim(), email.toLowerCase()), 800);
  }

  return (
    <div style={S.page}>
      <div style={S.card}>
        {/* LEFT */}
        <div style={S.left}>
          <div style={S.leftOverlay} />
          <div style={S.leftInner}>
            <div style={S.logo}>Salary<em style={S.logoEm}>IQ</em> Pro</div>
            <h2 style={S.leftH2}>Get<br />Started!</h2>
            <p style={S.leftP}>Join professionals discovering their true market value. Free forever, no credit card needed.</p>
            <div style={S.switchLbl}>Already have an account?</div>
            <button style={S.switchBtn} onClick={goLogin}>← Log In</button>
          </div>
          <div style={{ ...S.stats, visibility: "hidden" }}>
            <div><div style={S.statNum}>—</div></div>
          </div>
        </div>
        {/* RIGHT */}
        <div style={S.right}>
          <div style={S.arHelp}>Need help?</div>
          <h3 style={S.arTitle}>Create Account</h3>
          <p style={S.arSub}>Fill in your details to get started</p>
          {error && <div style={S.error}>{error}</div>}
          {msg   && <div style={S.success}>{msg}</div>}
          <FInput label="Full Name"        type="text"     placeholder="John Doe"             value={name}     onChange={e => setName(e.target.value)} />
          <FInput label="Email Address"    type="email"    placeholder="you@example.com"      value={email}    onChange={e => setEmail(e.target.value)} />
          <FInput label="Password"         type="password" placeholder="Min. 8 characters"    value={password} onChange={e => setPassword(e.target.value)} />
          {password && (
            <div style={{ marginTop: -10, marginBottom: 12 }}>
              <div style={{ height: 3, background: "#e2e8f0", borderRadius: 99, overflow: "hidden" }}>
                <div style={{ height: "100%", width: `${strength * 25}%`, background: pwColor, borderRadius: 99, transition: "width .3s" }} />
              </div>
              <span style={{ fontSize: 12, color: pwColor, fontWeight: 600 }}>{pwLabel}</span>
            </div>
          )}
          <FInput label="Confirm Password" type="password" placeholder="Repeat your password" value={confirm}  onChange={e => setConfirm(e.target.value)} />
          <button style={S.submitBtn} onClick={handleSignup}>Create Account →</button>
          <div style={S.orDiv}>— or —</div>
          <button style={S.linkBtn} onClick={goLogin}>Already have an account? Sign In</button>
        </div>
      </div>
    </div>
  );
}

// ─── MAIN APP (post-login) ───
const NAV_TABS = [
  ["predict","Predict"],["insights","Insights"],["roadmap","Roadmap"],
  ["dashboard","Dashboard"],["compare","Compare"],["leaderboard","Leaderboard"],
];

function MainApp({ userName, userEmail, onLogout }) {
  const [tab, setTab] = useState("predict");
  const initials = getInitials(userName);

  return (
    <div style={S.appWrap}>
      {/* Top Nav */}
      <div style={S.topNav}>
        <div style={S.navBrand}>💼 Salary<em style={S.navBrandEm}>IQ</em></div>
        <nav style={S.navLinks}>
          {NAV_TABS.map(([k, l]) => (
            <span key={k} onClick={() => setTab(k)}
              style={{ ...S.navLink, ...(tab === k ? S.navLinkActive : {}) }}>{l}</span>
          ))}
        </nav>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <div style={S.navAvatar}>{initials}</div>
          <span style={{ fontSize: 13, color: "rgba(255,255,255,.85)", whiteSpace: "nowrap" }}>{userName}</span>
          <button style={S.logoutBtn} onClick={onLogout}>Logout</button>
        </div>
      </div>

      {/* Tab Content */}
      {tab === "predict"     && <PredictTab userEmail={userEmail} />}
      {tab === "insights"    && <InsightsTab />}
      {tab === "roadmap"     && <RoadmapTab />}
      {tab === "dashboard"   && <DashboardTab userEmail={userEmail} userName={userName} />}
      {tab === "compare"     && <ComparePlaceholder />}
      {tab === "leaderboard" && <LeaderboardTab userEmail={userEmail} userName={userName} />}
    </div>
  );
}

// ─── PREDICT TAB ───
const JOB_OPTIONS = ["Data Scientist","Software Engineer","AI Engineer","Data Analyst","Machine Learning Engineer","DevOps Engineer","Cloud Engineer","Cybersecurity Analyst","Product Manager","Business Analyst","Frontend Developer","Backend Developer","Other"];
const EDU_OPTIONS = ["High School","Diploma","Bachelor's","Master's","PhD","Other"];
const LOC_OPTIONS = ["Bangalore","Mumbai","Delhi","Hyderabad","Chennai","Pune","Remote","Other"];
const IND_OPTIONS = ["Technology","Finance","Healthcare","Consulting","Manufacturing","Education","Retail","Media","Telecom","Government","Other"];
const CO_OPTIONS  = ["Startup (1–50)","Small (51–200)","Medium (201–1000)","Large (1001–5000)","Enterprise (5000+)"];
const REM_OPTIONS = ["On-site","Hybrid","Fully Remote"];

function SelectField({ label, options, value, onChange }) {
  return (
    <div style={{ marginBottom: 14 }}>
      <label style={S.label}>{label}</label>
      <select value={value} onChange={e => onChange(e.target.value)}
        style={{ ...S.input, marginBottom: 0, cursor: "pointer" }}>
        {options.map(o => <option key={o}>{o}</option>)}
      </select>
    </div>
  );
}
function NumField({ label, value, onChange, min = 0, max = 50 }) {
  return (
    <div style={{ marginBottom: 14 }}>
      <label style={S.label}>{label}</label>
      <input type="number" min={min} max={max} value={value} onChange={e => onChange(Number(e.target.value))}
        style={{ ...S.input, marginBottom: 0 }} />
    </div>
  );
}

// Simple salary estimator (replaces pickle model for React demo)
function estimateSalary({ exp, skills, cert, job, edu, loc, ind, remote }) {
  let base = 60000;
  base += exp * 8500;
  base += skills * 2200;
  base += cert * 4000;
  const jobMult = { "AI Engineer": 1.35, "Machine Learning Engineer": 1.3, "Data Scientist": 1.25, "Software Engineer": 1.2, "Cloud Engineer": 1.18, "DevOps Engineer": 1.15, "Product Manager": 1.18, "Cybersecurity Analyst": 1.1, "Backend Developer": 1.12, "Frontend Developer": 1.08, "Data Analyst": 1.05, "Business Analyst": 1.0, "Other": 0.95 };
  const eduMult = { "PhD": 1.25, "Master's": 1.15, "Bachelor's": 1.0, "Diploma": 0.88, "High School": 0.78, "Other": 0.9 };
  const locMult = { "Bangalore": 1.18, "Mumbai": 1.12, "Delhi": 1.08, "Hyderabad": 1.1, "Chennai": 1.05, "Pune": 1.05, "Remote": 1.2, "Other": 0.92 };
  const indMult = { "Technology": 1.2, "Finance": 1.15, "Consulting": 1.12, "Healthcare": 1.08, "Telecom": 1.05, "Manufacturing": 0.9, "Education": 0.82, "Retail": 0.85, "Media": 0.9, "Government": 0.8, "Other": 0.95 };
  const remMult = { "Fully Remote": 1.12, "Hybrid": 1.05, "On-site": 1.0 };
  return Math.round(base * (jobMult[job] || 1) * (eduMult[edu] || 1) * (locMult[loc] || 1) * (indMult[ind] || 1) * (remMult[remote] || 1));
}

function PredictTab({ userEmail }) {
  const [exp, setExp]     = useState(3);
  const [skills, setSkills] = useState(6);
  const [cert, setCert]   = useState(1);
  const [job, setJob]     = useState("Software Engineer");
  const [edu, setEdu]     = useState("Bachelor's");
  const [loc, setLoc]     = useState("Bangalore");
  const [ind, setInd]     = useState("Technology");
  const [company, setCompany] = useState("Medium (201–1000)");
  const [remote, setRemote]   = useState("Hybrid");
  const [result, setResult]   = useState(null);

  function predict() {
    const salary = estimateSalary({ exp, skills, cert, job, edu, loc, ind, remote });
    const prediction = { salary, job, exp, skills, date: new Date().toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric" }) };
    // Save to localStorage
    const users = getUsers();
    if (users[userEmail]) {
      if (!users[userEmail].predictions) users[userEmail].predictions = [];
      users[userEmail].predictions.push(prediction);
      saveUsers(users);
    }
    // Also store globally for other tabs
    localStorage.setItem("salaryiq_last", JSON.stringify({ salary, job, exp, skills, cert, edu, ind }));
    setResult(salary);
  }

  const monthly = result ? `₹${Math.round(result / 12).toLocaleString("en-IN")}` : null;
  const potential = result ? `₹${Math.round(result * 1.35).toLocaleString("en-IN")}` : null;
  const pct = result ? Math.min(95, Math.max(30, Math.round(30 + (result / 220000) * 65))) : null;

  return (
    <div style={S.pageWrap}>
      <div style={S.pageTitle}>Salary Prediction</div>
      <p style={S.pageSub}>Fill in your profile to get your estimated market salary instantly.</p>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>
        <div>
          <div style={S.card}>
            <div style={S.cardTitle}>📊 Experience & Skills</div>
            <NumField label="Years of Experience" value={exp}    onChange={setExp}    max={40} />
            <NumField label="Number of Skills"    value={skills} onChange={setSkills} min={1} max={50} />
            <NumField label="Certifications"      value={cert}   onChange={setCert}   max={20} />
          </div>
          <div style={S.card}>
            <div style={S.cardTitle}>🎓 Education & Role</div>
            <SelectField label="Job Role"        options={JOB_OPTIONS} value={job} onChange={setJob} />
            <SelectField label="Education Level" options={EDU_OPTIONS} value={edu} onChange={setEdu} />
          </div>
        </div>
        <div>
          <div style={S.card}>
            <div style={S.cardTitle}>🏢 Company & Location</div>
            <SelectField label="Location"     options={LOC_OPTIONS} value={loc}     onChange={setLoc} />
            <SelectField label="Industry"     options={IND_OPTIONS} value={ind}     onChange={setInd} />
            <SelectField label="Company Size" options={CO_OPTIONS}  value={company} onChange={setCompany} />
            <SelectField label="Remote Work"  options={REM_OPTIONS} value={remote}  onChange={setRemote} />
          </div>
          <div style={{ ...S.card, background: "linear-gradient(135deg,#eef2ff,#f5f3ff)", border: "1px solid #c7d2fe" }}>
            <div style={{ ...S.cardTitle, color: "#4f46e5" }}>✨ What you'll get</div>
            {["💰 Instant salary prediction","💡 Personalised growth tips","🗺️ Step-by-step career roadmap","📈 Industry trends & benchmarks","⚖️ Compare vs market salaries"].map(t => (
              <div key={t} style={{ fontSize: 13, color: "#475569", marginBottom: 8 }}>{t}</div>
            ))}
          </div>
        </div>
      </div>
      <div style={{ maxWidth: 360, margin: "0 auto 8px" }}>
        <button style={S.submitBtn} onClick={predict}>🔍  Predict My Salary</button>
      </div>

      {result && (
        <>
          <div style={S.heroResult}>
            <div style={S.heroLbl}>Your Estimated Annual Salary</div>
            <div style={S.heroAmt}>₹{result.toLocaleString("en-IN")}</div>
            <div style={S.heroSub}>≈ {monthly} / month · Powered by intelligent estimation</div>
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: 12, marginBottom: 12 }}>
            {[
              ["Seniority Level", exp <= 2 ? "Fresher" : exp <= 5 ? "Junior" : exp <= 10 ? "Mid-Level" : "Senior"],
              ["Monthly Salary", monthly],
              ["Growth Potential", potential],
              ["Market Percentile", `${pct}th`],
            ].map(([l, v]) => (
              <div key={l} style={{ background: "#fff", borderRadius: 14, border: "1px solid #e2e8f0", padding: "16px 14px" }}>
                <div style={{ fontSize: 12, color: "#94a3b8", marginBottom: 6 }}>{l}</div>
                <div style={{ fontSize: 20, fontWeight: 800, color: "#0f172a" }}>{v}</div>
              </div>
            ))}
          </div>
          <div style={{ background: "#f0fdf4", border: "1px solid #bbf7d0", borderRadius: 12, padding: "14px 20px" }}>
            <span style={{ fontSize: 14, color: "#15803d", fontWeight: 600 }}>✅ Prediction saved!</span>
            <span style={{ fontSize: 13, color: "#166534" }}> · Now explore your Insights, Roadmap, and Dashboard tabs.</span>
          </div>
        </>
      )}
    </div>
  );
}

// ─── INSIGHTS TAB ───
function InsightsTab() {
  const last = JSON.parse(localStorage.getItem("salaryiq_last") || "null");
  if (!last) return <EmptyState icon="💡" msg="Run a prediction first" />;
  const { salary, job, exp, skills, cert, edu, ind } = last;
  const SKILLS_MAP = {
    "Data Scientist": ["Python","Machine Learning","Deep Learning","SQL","Statistics","TensorFlow"],
    "Software Engineer": ["System Design","DSA","Cloud","Docker","Kubernetes","CI/CD"],
    "AI Engineer": ["LLMs","PyTorch","MLOps","Vector DBs","Prompt Eng","Transformers"],
    "Other": ["Communication","Project Mgmt","Data Analysis","Cloud Basics","Agile","Python"],
  };
  const topSkills = (SKILLS_MAP[job] || SKILLS_MAP["Other"]).slice(0, 6);
  const boosts = ["+₹8K–15K","+₹10K–20K","+₹6K–12K","+₹12K–25K","+₹5K–10K","+₹15K–30K"];

  return (
    <div style={S.pageWrap}>
      <div style={S.pageTitle}>Career Insights</div>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>
        <div style={S.card}>
          <div style={S.cardTitle}>🛠️ Top Skills to Learn</div>
          {topSkills.map((sk, i) => (
            <div key={sk} style={{ marginBottom: 12 }}>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: 13, marginBottom: 4 }}>
                <span style={{ fontWeight: 500, color: "#0f172a" }}>{sk}</span>
                <span style={{ color: "#10b981", fontWeight: 600 }}>{boosts[i]}/yr</span>
              </div>
              <div style={{ height: 8, background: "#f1f5f9", borderRadius: 99 }}>
                <div style={{ height: "100%", width: `${90 - i * 10}%`, background: "linear-gradient(90deg,#6366f1,#8b5cf6)", borderRadius: 99 }} />
              </div>
            </div>
          ))}
        </div>
        <div style={S.card}>
          <div style={S.cardTitle}>⚡ What-If Salary Simulator</div>
          {[["Extra Experience", 2, 10, "exp", 0.055], ["Extra Skills", 3, 10, "sk", 0.028], ["Certifications", 1, 5, "cert", 0.04]].map(([lbl, def, max, key, mult]) => {
            const [val, setVal] = useState(def);
            const sim = Math.round(salary * (1 + val * mult));
            return (
              <div key={key} style={{ marginBottom: 18 }}>
                <div style={{ display: "flex", justifyContent: "space-between", fontSize: 13, marginBottom: 6 }}>
                  <span style={{ color: "#475569" }}>+{val} {lbl}</span>
                  <span style={{ fontWeight: 700, color: "#4f46e5" }}>₹{sim.toLocaleString("en-IN")}</span>
                </div>
                <input type="range" min={0} max={max} value={val} onChange={e => setVal(Number(e.target.value))} style={{ width: "100%" }} />
                <span style={{ fontSize: 12, color: "#10b981", fontWeight: 600 }}>+₹{(sim - salary).toLocaleString("en-IN")}</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

// ─── ROADMAP TAB ───
const ROADMAP = {
  "Data Scientist": ["Junior Data Analyst","Data Scientist","Senior Data Scientist","Lead / Staff DS","Head of Data Science"],
  "Software Engineer": ["Junior Developer","Software Engineer","Senior Engineer","Staff Engineer","Principal / VP Eng"],
  "AI Engineer": ["ML Engineer","AI Engineer","Senior AI Engineer","AI Tech Lead","AI Research Director"],
  "Other": ["Entry Level","Mid Level","Senior Level","Lead / Manager","Director / VP"],
};
function RoadmapTab() {
  const last = JSON.parse(localStorage.getItem("salaryiq_last") || "null");
  if (!last) return <EmptyState icon="🗺️" msg="Run a prediction first" />;
  const { job, exp } = last;
  const steps = ROADMAP[job] || ROADMAP["Other"];
  const curr  = exp <= 2 ? 0 : exp <= 5 ? 1 : exp <= 10 ? 2 : exp <= 15 ? 3 : 4;
  const salRanges = ["₹40K–70K","₹70K–1.1L","₹1.1L–1.6L","₹1.6L–2.0L","₹2.0L+"];
  const expRanges = ["0–2 yrs","2–5 yrs","5–10 yrs","10–15 yrs","15+ yrs"];

  return (
    <div style={S.pageWrap}>
      <div style={S.pageTitle}>Career Roadmap</div>
      <div style={S.card}>
        <div style={S.cardTitle}>🗺️ Your Career Path — {job}</div>
        {steps.map((step, i) => {
          const done = i < curr, active = i === curr;
          return (
            <div key={step} style={{ display: "flex", gap: 16, alignItems: "flex-start", padding: "16px 0", borderBottom: i < steps.length - 1 ? "1px solid #f1f5f9" : "none" }}>
              <div style={{ width: 36, height: 36, borderRadius: "50%", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 13, fontWeight: 700, flexShrink: 0, background: done ? "#6366f1" : active ? "linear-gradient(135deg,#6366f1,#8b5cf6)" : "#f1f5f9", color: done || active ? "#fff" : "#94a3b8", border: active ? "none" : "none", boxShadow: active ? "0 0 0 4px rgba(99,102,241,.2)" : "none" }}>{i + 1}</div>
              <div>
                <div style={{ fontSize: 15, fontWeight: 600, color: "#0f172a" }}>{step}</div>
                <div style={{ fontSize: 13, color: "#64748b", marginTop: 3 }}>{expRanges[i]} · {salRanges[i]}</div>
                <span style={{ display: "inline-block", fontSize: 11, fontWeight: 600, padding: "2px 10px", borderRadius: 99, marginTop: 6, background: done ? "#f0fdf4" : active ? "#eef2ff" : "#f8fafc", color: done ? "#15803d" : active ? "#4f46e5" : "#94a3b8" }}>
                  {done ? "✓ Completed" : active ? "📍 You are here" : `Next · ${expRanges[i]}`}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ─── DASHBOARD TAB ───
function DashboardTab({ userEmail, userName }) {
  const users = getUsers();
  const preds = users[userEmail]?.predictions || [];
  if (!preds.length) return <EmptyState icon="📊" msg="No predictions yet — go to Predict tab!" />;
  const salaries = preds.map(p => p.salary);
  const best = Math.max(...salaries), avg = Math.round(salaries.reduce((a, b) => a + b, 0) / salaries.length);
  return (
    <div style={S.pageWrap}>
      <div style={S.pageTitle}>My Dashboard</div>
      <p style={S.pageSub}>Your personal prediction history and statistics.</p>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: 12, marginBottom: 16 }}>
        {[["Total Predictions", preds.length],["Latest Salary",`₹${salaries[salaries.length-1].toLocaleString("en-IN")}`],["Average Salary",`₹${avg.toLocaleString("en-IN")}`],["Best Prediction",`₹${best.toLocaleString("en-IN")}`]].map(([l,v]) => (
          <div key={l} style={{ background: "#fff", borderRadius: 14, border: "1px solid #e2e8f0", padding: 16 }}>
            <div style={{ fontSize: 12, color: "#94a3b8", marginBottom: 6 }}>{l}</div>
            <div style={{ fontSize: 20, fontWeight: 800, color: "#0f172a" }}>{v}</div>
          </div>
        ))}
      </div>
      <div style={S.card}>
        <div style={S.cardTitle}>📋 Prediction History</div>
        {[...preds].reverse().slice(0, 10).map((p, i) => (
          <div key={i} style={{ display: "flex", gap: 12, padding: "11px 0", borderBottom: "1px solid #f8fafc", alignItems: "center" }}>
            <span style={{ flex: ".4", fontSize: 13, color: "#94a3b8" }}>{i + 1}</span>
            <span style={{ flex: 2, fontSize: 13, fontWeight: 500, color: "#0f172a" }}>{p.job || "—"}</span>
            <span style={{ flex: 1, fontSize: 13, color: "#64748b" }}>{p.exp} yrs</span>
            <span style={{ flex: 1, fontSize: 13, color: "#64748b" }}>{p.skills} skills</span>
            <span style={{ flex: 1.5, fontSize: 14, fontWeight: 700, color: "#4f46e5" }}>₹{p.salary.toLocaleString("en-IN")}{p.salary === best ? " ⭐" : ""}</span>
            <span style={{ flex: 1.5, fontSize: 12, color: "#94a3b8" }}>{p.date || "—"}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── COMPARE PLACEHOLDER ───
function ComparePlaceholder() {
  const last = JSON.parse(localStorage.getItem("salaryiq_last") || "null");
  if (!last) return <EmptyState icon="⚖️" msg="Run a prediction first" />;
  const { salary, job } = last;
  const base = Math.max(40000, salary - 15000);
  const benchmarks = [
    ["Entry Level (0–2 yrs)", Math.round(base * 0.6), "#e2e8f0"],
    ["Mid Level (3–6 yrs)",   Math.round(base * 0.85), "#c7d2fe"],
    ["Your Salary",           salary, "#6366f1"],
    ["Top 25% in your role",  Math.round(salary * 1.22), "#8b5cf6"],
    ["Top 10% in your role",  Math.round(salary * 1.48), "#7c3aed"],
    ["Top 5% — Elite earner", Math.round(salary * 1.75), "#4338ca"],
  ];
  const maxV = benchmarks[benchmarks.length - 1][1];
  return (
    <div style={S.pageWrap}>
      <div style={S.pageTitle}>Compare Yourself</div>
      <p style={S.pageSub}>See how your predicted salary stacks up against market benchmarks.</p>
      <div style={{ display: "grid", gridTemplateColumns: "3fr 2fr", gap: 20 }}>
        <div style={S.card}>
          <div style={S.cardTitle}>📊 Salary Benchmarks — {job}</div>
          {benchmarks.map(([label, val, color]) => {
            const isYou = label === "Your Salary";
            const pct   = Math.round((val / maxV) * 100);
            return (
              <div key={label} style={{ marginBottom: 14, ...(isYou ? { background: "#eef2ff", borderRadius: 8, padding: "8px 10px", border: "1px solid #c7d2fe" } : {}) }}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 5 }}>
                  <span style={{ fontSize: 13, fontWeight: isYou ? 700 : 500, color: isYou ? "#4f46e5" : "#374151" }}>{isYou ? "📍 " : ""}{label}</span>
                  <span style={{ fontSize: 13, fontWeight: 600, color: isYou ? "#4f46e5" : "#0f172a" }}>₹{val.toLocaleString("en-IN")}</span>
                </div>
                <div style={{ height: 8, background: "#f1f5f9", borderRadius: 99 }}>
                  <div style={{ height: "100%", width: `${pct}%`, background: color, borderRadius: 99 }} />
                </div>
              </div>
            );
          })}
        </div>
        <div>
          <div style={{ ...S.card, textAlign: "center", marginBottom: 12 }}>
            <div style={S.cardTitle}>🎯 Your Market Position</div>
            <div style={{ fontSize: 52, fontWeight: 800, color: "#6366f1" }}>{Math.min(95, Math.max(25, Math.round(30 + (salary / (salary * 1.75)) * 65)))}th</div>
            <div style={{ fontSize: 14, color: "#64748b" }}>percentile in your field</div>
          </div>
        </div>
      </div>
    </div>
  );
}

// ─── LEADERBOARD ───
function LeaderboardTab({ userEmail, userName }) {
  const users = getUsers();
  const lb = Object.values(users)
    .filter(u => u.predictions?.length)
    .map(u => { const best = Math.max(...u.predictions.map(p => p.salary)); const p = u.predictions.find(x => x.salary === best); return { name: u.name, salary: best, job: p?.job || "Professional", exp: p?.exp || 0 }; })
    .sort((a, b) => b.salary - a.salary).slice(0, 10);

  const myBest = Math.max(...(users[userEmail]?.predictions?.map(p => p.salary) || [0]));
  const myRank = lb.filter(e => e.salary > myBest).length + 1;

  const medals = ["🥇","🥈","🥉"];
  const rowColors = [
    { background: "linear-gradient(135deg,#fffbeb,#fef3c7)", border: "1px solid #fde68a" },
    { background: "linear-gradient(135deg,#f8fafc,#f1f5f9)", border: "1px solid #e2e8f0" },
    { background: "linear-gradient(135deg,#fff7ed,#ffedd5)", border: "1px solid #fed7aa" },
  ];

  return (
    <div style={S.pageWrap}>
      <div style={S.pageTitle}>Leaderboard</div>
      <p style={S.pageSub}>Top predicted salaries across all SalaryIQ Pro users.</p>
      {myBest > 0 && (
        <div style={{ background: "linear-gradient(135deg,#eef2ff,#f5f3ff)", border: "1px solid #c7d2fe", borderRadius: 14, padding: "18px 24px", marginBottom: 20, display: "flex", justifyContent: "space-between", flexWrap: "wrap", gap: 12 }}>
          <div><div style={{ fontSize: 11, color: "#6366f1", fontWeight: 700, textTransform: "uppercase" }}>Your Position</div><div style={{ fontSize: 22, fontWeight: 800, color: "#1e1b4b" }}>#{myRank} <span style={{ fontSize: 14, color: "#64748b", fontWeight: 400 }}>out of {lb.length} users</span></div></div>
          <div style={{ textAlign: "right" }}><div style={{ fontSize: 11, color: "#6366f1", fontWeight: 700, textTransform: "uppercase" }}>Your Best</div><div style={{ fontSize: 22, fontWeight: 800, color: "#4f46e5" }}>₹{myBest.toLocaleString("en-IN")}</div></div>
        </div>
      )}
      {lb.length === 0
        ? <div style={{ textAlign: "center", padding: 40, color: "#94a3b8", fontSize: 14 }}>No predictions yet. Be the first!</div>
        : lb.map((e, i) => {
          const isMe = e.name === userName;
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 12, padding: "12px 14px", borderRadius: 12, marginBottom: 8, ...(rowColors[i] || { background: "#f8fafc", border: "1px solid #f1f5f9" }), ...(isMe ? { border: "2px solid #6366f1" } : {}) }}>
              <span style={{ fontSize: 16, fontWeight: 800, minWidth: 28 }}>{i < 3 ? medals[i] : `#${i+1}`}</span>
              <div style={{ flex: 1, minWidth: 100 }}>
                <div style={{ fontSize: 14, fontWeight: 600, color: "#0f172a" }}>{e.name}{isMe && <span style={{ marginLeft: 6, fontSize: 11, background: "#eef2ff", color: "#4f46e5", padding: "2px 8px", borderRadius: 99, fontWeight: 600 }}>You</span>}</div>
                <div style={{ fontSize: 12, color: "#64748b" }}>{e.job} · {e.exp} yrs exp</div>
              </div>
              <span style={{ fontSize: 16, fontWeight: 800, color: "#4f46e5" }}>₹{e.salary.toLocaleString("en-IN")}</span>
            </div>
          );
        })
      }
    </div>
  );
}

// ─── EMPTY STATE ───
function EmptyState({ icon, msg }) {
  return (
    <div style={{ textAlign: "center", padding: "80px 20px" }}>
      <div style={{ fontSize: 48 }}>{icon}</div>
      <div style={{ fontSize: 18, fontWeight: 600, color: "#0f172a", marginTop: 12 }}>{msg}</div>
    </div>
  );
}

// ─── ROOT ───
export default function App() {
  const [page, setPage] = useState("login");
  const [userName, setUserName]   = useState("");
  const [userEmail, setUserEmail] = useState("");
  const [loggedIn, setLoggedIn]   = useState(false);

  function handleLogin(name, email) { setUserName(name); setUserEmail(email); setLoggedIn(true); }
  function handleLogout() { setLoggedIn(false); setUserName(""); setUserEmail(""); setPage("login"); }

  if (loggedIn) return <MainApp userName={userName} userEmail={userEmail} onLogout={handleLogout} />;
  if (page === "login")  return <LoginPage  onLogin={handleLogin} goSignup={() => setPage("signup")} />;
  if (page === "signup") return <SignupPage onLogin={handleLogin} goLogin={()  => setPage("login")} />;
}
