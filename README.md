# BBPupdater

A small Python script that monitors **HackerOne bounty program scope changes** and sends updates to a **Discord webhook**.

The script checks all available programs through the HackerOne API, compares the latest structured scopes against a locally stored snapshot, and posts any newly added or recently updated bounty-eligible domains/URLs to Discord every 30 minutes.

---

## Functionality

* Pulls program data from the HackerOne API
* Filters for bounty-eligible `URL` and `Domain` scope types
* Stores the latest scope snapshot locally
* Detects:

  * newly added programs
  * newly added scopes
  * updated scope timestamps
* Sends detected changes to a Discord webhook as a text file
* Runs automatically every 30 minutes

---

## Requirements

Install the required packages before running:

```bash
pip install requests discord.py scheduler
```

> Depending on the `scheduler` package you use, make sure it matches the import used in the script.

---

## Setup

Before running the script, replace the placeholder credentials inside `BBPupdater.py`.

### HackerOne API credentials

Replace:

```python
login = ('-H1_USERNAME-', '-H1_API_KEY-')
```

with your actual HackerOne username and API key.

Example:

```python
login = ('your_username', 'your_api_key'
```

### Discord webhook

Replace:

```python
webhook = discord.SyncWebhook.from_url("-DISCORD_WEBHOOK_LINK-")
```

with your Discord webhook URL.

Example:

```python
webhook = discord.SyncWebhook.from_url("https://discord.com/api/webhooks/...")
```

---

## File structure

The script automatically creates a `scriptFiles` folder in the same directory.

```text
project/
│
├── BBPupdater.py
└── scriptFiles/
    ├── currentScopesJSON.txt
    └── currentScopesMsg.txt
```

### Generated files

* `currentScopesJSON.txt` → stores the latest scope snapshot
* `currentScopesMsg.txt` → temporary update message sent to Discord

---

## How it works

On startup, the script:

1. Creates the `scriptFiles` directory if it does not exist
2. Fetches all HackerOne programs
3. Pulls structured scopes for each program
4. Compares results with the previously saved snapshot
5. Sends updates to Discord
6. Repeats every **30 minutes**

---

## Running

Start the script with:

```bash
python BBPupdater.py
```

The process will continue running in the background until stopped.

---

## Disclaimer

Make sure your usage complies with HackerOne’s API terms and rate limits.
Only use your own API credentials and keep webhook URLs private.
