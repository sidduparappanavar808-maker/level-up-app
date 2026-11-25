# LEVEL UP — Personal Productivity Tracker

A Flask + SQLite/PostgreSQL task tracker. This first version includes:
- A daily dashboard and completion percentage
- Date-based schedules that can differ from day to day
- Add, edit, complete and delete tasks
- Saved task history
- Daily motivational quotes
- Responsive dark UI

## Run on Windows

1. Install Python 3.10 or newer.
2. Open Command Prompt in this folder.
3. Create and activate a virtual environment:

   ```bat
   py -m venv .venv
   .venv\Scripts\activate
   ```

4. Install dependencies:

   ```bat
   pip install -r requirements.txt
   ```

5. Start the website:

   ```bat
   python app.py
   ```

6. Open http://127.0.0.1:5000

## Hosting plan

Recommended deployment path:
- Push this project to a private or public GitHub repository.
- Create a managed PostgreSQL database (for example, Supabase).
- Deploy the Flask web service on Render.
- Set the `DATABASE_URL` environment variable in Render to the PostgreSQL connection string.

Do not use SQLite on an ephemeral hosting filesystem for important data.

## Inactivity reminder (next development step)

The requested reminder is NOT a reminder for every task. It should trigger only when the user has not visited the website for a chosen period (for example, 24 hours).

A real reminder while the website is closed requires:
1. Browser push permission and a service worker.
2. A push subscription saved in the database.
3. A backend scheduled check (cron/job) that detects inactivity.
4. A Web Push sender configured with VAPID keys.

A normal webpage cannot reliably wake itself up or send a notification while closed. We will add this after the core app is running and hosted.

## Install on Android

After deploying the site to HTTPS:
1. Open the website in Chrome on your Android phone.
2. Open the browser menu (three dots).
3. Tap **Install app** or **Add to Home screen**.
4. Launch LEVEL UP from your phone like an app.

This PWA shell supports installation and basic offline caching. Task changes still need an internet connection to sync with the Flask server.

The app is responsive on phone screens. Tasks can be added, edited, completed, and deleted for individual dates. Push notifications for inactivity are a separate next step and need a hosted push service and notification permission.
