# Project-Exam-Portal

<h1>📝 Online Examination Platform </h1> <br>
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------<br>
A full-featured online examination system built using Django, supporting secure, timed exams with automated Excel-based question uploads and randomized exam sets.<br>
This platform provides separate workflows for students and examiners, enforces single attempts, and evaluates results deterministically and securely.<br>
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------<br>
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------<br>
<br>
<h1> 🚀 Features </h1> <br>
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------<br>
<h2> 👨‍🎓 Student </h2>
<ul>
  <li>Secure Login</li>
  <li> Dashboard showing Available exams</li>
  <li>single attempt per exam</li>
  <li>Server-side enforced timer for exam</li>
  <li>auto submit on timeup</li>
  <li>Detailed result evaluations</li>
</ul>

<h2> 👩‍🏫 Examiner </h2>
<ul>
  <li>Examiner dashboard</li>
  <li>Create exams (via admin shortcut)</li>
  <li>Upload questions using Excel</li>
  <li>Automatic exam set generation</li>
  <li>Randomized question order per student</li>
  <li>View student submissions & scores</li>
</ul>

<h2> ⚙️ System </h2>
<ul>
  <li>Excel-based bulk upload</li>
  <li>Randomized exam sets (A/B/C/D)</li>
  <li>Atomic regeneration of derived data</li>
  <li>Immutable submissions</li>
  <li>Role-aware navigation</li>
  <li>Bootstrap 5 + crispy-forms UI</li>
</ul>

<h2>🧠 Architecture Highlights</h2>
<ul>
  <li>ExamSet & SetQuestion treated as derived data</li>
  <li>Sets are regenerated automatically after uploads</li>
  <li>Server-side timing (refresh-safe & tamper-proof)</li>
  <li>Django Admin used only as a control panel</li>
  <li>No shell/manual intervention required after setup</li>
</ul>


<h2>🛠️ Tech Stack</h2>
<ul>
  <li>Backend: Django</li>
  <li>Database: MySQL</li>
  <li>Frontend: Bootstrap 5, Django Crispy Forms</li>
  <li>Auth: Django built-in authentication</li>
  <li>Data Upload: Excel (openpyxl / pandas)</li>
  <li> Environment: Python Virtualenv </li>
</ul>

<h2>🧪 Application Flow</h2>
<ul>
  <li>Examiner creates exam (DRAFT)</li>
  <li>Examiner uploads Excel sheet</li>
  <li>Exam sets generated automatically</li>
  <li>Exam marked LIVE</li>
  <li>Students attempt exam (timed)</li>
  <li>Auto evaluation & result generation</li>
  <li>Examiner reviews submissions</li>
</ul>

<h2>🔐 Security & Integrity</h2>
<ul>
  <li>POST-based logout (CSRF-safe)</li>
  <li>Single attempt enforced</li>
  <li>Exam state locking (DRAFT / LIVE / CLOSED)</li>
  <li>Backend-authoritative evaluation</li>
  <li>No client-side trust</li>
</ul>

<h3> ScreenShots are Available in Screenshot folder </h3>