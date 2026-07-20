# Lookouts McDouble Alert

Checks each day whether the Chattanooga Lookouts hit a double in their most
recent home game, and pushes a free phone notification if so.

## One-time setup (about 5 minutes)

1. **Install the ntfy app** on your phone (free, no account needed):
   - iOS: search "ntfy" in the App Store
   - Android: search "ntfy" on Google Play, or get it from F-Droid
   - Open the app and **subscribe to a topic** — pick any unique, hard-to-guess
     name, e.g. `lookouts-mcdouble-yourname-4471`. Topics are public, so avoid
     anything guessable or sensitive.

2. **Create a GitHub account** if you don't have one (free): github.com

3. **Create a new repository**:
   - Go to github.com/new, name it e.g. `lookouts-mcdouble`, keep it private
     or public (doesn't matter), and create it.
   - Upload these three files, keeping the same folder structure:
     - `check_lookouts.py`
     - `.github/workflows/check-lookouts.yml`
     - `README.md` (optional)
   - Easiest way: on the repo page, click "Add file" → "Upload files" and
     drag all three in (GitHub will recreate the `.github/workflows/` folder
     automatically if you drag the whole folder).

4. **Add your ntfy topic as a secret**:
   - In your new repo: Settings → Secrets and variables → Actions → New
     repository secret
   - Name: `NTFY_TOPIC`
   - Value: the topic name you picked in step 1 (e.g. `lookouts-mcdouble-yourname-4471`)

5. **Test it**: Go to the "Actions" tab in your repo → "Check Lookouts
   McDouble Deal" → "Run workflow" → Run workflow. After ~30 seconds, check
   the run log to confirm it worked. If there was a double recently, you
   should also get a push notification.

That's it — from then on it runs automatically every day at ~7-8am Eastern
and only notifies you when there's actually a double to celebrate.

## Notes
- The schedule is in UTC and doesn't auto-adjust for daylight saving; nudge
  the cron hour in the workflow file by ±1 if the timing drifts.
- No servers, no cost — GitHub Actions is free for this kind of light use.
