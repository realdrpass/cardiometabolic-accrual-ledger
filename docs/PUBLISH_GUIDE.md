# Publish guide: v1.0.0

*Plain-language note: this guide takes the ledger from a private GitHub repository to a public dataset with a permanent DOI (citation number). It takes about 20 minutes in one sitting. Claude can't do these steps, because they change settings on your GitHub and Zenodo accounts.*

## Copy-ready text

**Release title**
```
Cardiometabolic Trial Accrual Ledger v1.0.0
```

**Release notes**
```
First public release.

2,834 US interventional drug trials (Phase 2 to 4, first posted 2008 to 2025, at least one US site) in diabetes, obesity, hypertension, heart failure and dyslipidemia, from ClinicalTrials.gov (accessed 13 October 2026). For each trial: actual enrollment, status, dates, sites, sponsor class and phase. For the 468 trials that stopped early: the stated reason, classified into six groups with published coding rules. Poor enrollment is the most common stated reason (151 of 468).

Start with README.md. The rules are in docs/CODING_RULES.md and the limitations in docs/LIMITATIONS.md.

Next: v1.1 (December 2026) adds planned enrollment and the enrollment ratio.
```

## Step 1: Rename the branch to main (1 min)

1. Open https://github.com/realdrpass/cardiometabolic-accrual-ledger and click **Settings** (gear tab, top right).
2. Under **Default branch**, which shows `claude/v1.0.0`, click the pencil icon.
3. Type `main` and click **Rename branch**.

**What you should see:** the branch dropdown on the front page says `main`, and the history shows one entry: "Cardiometabolic Trial Accrual Ledger v1.0.0".

## Step 2: Confirm the repository is public (30 seconds)

The repository was created as public, so there's nothing to change. Check for the "Public" label next to the repository name. If it says "Private", go to **Settings → General → Danger Zone → Change visibility → Change to public**.

## Step 3: Switch on Zenodo for the repository (5 min)

1. Go to https://zenodo.org and click **Log in**. Choose **Log in with ORCID**, so your ORCID attaches automatically.
2. Click your name or email at the top right, then **GitHub**.
3. If asked, click **Connect** and approve Zenodo's access to your GitHub account.
4. In the list of repositories, find `realdrpass/cardiometabolic-accrual-ledger` and flip its switch to **On**. If it isn't listed, click **Sync now** and wait a minute.

**What you should see:** the switch is green next to the repository.

## Step 4: Create the release (5 min)

The release triggers Zenodo, so do Step 3 first.

1. On the repository's front page, click **Releases** in the right-hand column, then **Create a new release**. On some screens the button is worded slightly differently; it is the one that starts a new release.
2. Click **Choose a tag**, type `v1.0.0`, and click **Create new tag: v1.0.0 on publish**.
3. Check that **Target** is `main`.
4. Paste the release title and release notes from the top of this guide.
5. Leave "Set as a pre-release" unticked. Click **Publish release**.

**What you should see:** a release page titled "Cardiometabolic Trial Accrual Ledger v1.0.0", with zip and tar.gz downloads.

## Step 5: Get the DOI and check the record (5 min)

1. After 2 to 10 minutes, go back to **zenodo.org → your name → GitHub**. The repository now shows a DOI badge. Click it to open the Zenodo record.
2. Check the record:
   - The title is "Cardiometabolic Trial Accrual Ledger".
   - The creator is Ogunbayo, Olufisayo, with the ORCID icon.
   - The resource type is Dataset.
   - The license is Creative Commons Attribution 4.0.
   - The version is 1.0.0.
3. Find the DOI on the right of the record page, starting `10.5281/zenodo.`. Zenodo shows two DOIs:
   - **This version** cites exactly v1.0.0. Use it in your petition and papers.
   - **All versions** always points to the newest release.
4. Save the Zenodo record page as a PDF: in your browser, choose Print, then Save as PDF. Do the same for the GitHub release page. These are your evidence copies.

## Step 6: Send Claude the DOIs (1 min)

Reply with both DOIs. Claude will:
- add them to the README and `CITATION.cff`
- fill in your evidence log row with today's date
- update the AACT plan for v1.1.

If anything on screen doesn't match what this guide says, stop and tell Claude what you see.
