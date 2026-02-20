# Repository Setup Guide for Prof

**Purpose:** Archival and documentation of 6-month internship work at WTMH Lab, NCKU

---

## 🎯 Current Situation

- Work completed at WTMH Lab (August 2025 - January 2026)
- Prof requested documentation be organized in repository
- Prof does not have GitHub account
- Need to decide: Public or Private repository

---

## 📋 Recommendation: **START PRIVATE**

### Why Private First?

✅ **Safe default** - dapat review dulu sebelum public  
✅ **Control access** - hanya yang invited yang bisa lihat  
✅ **Easy to make public later** - bisa switch kapan saja  
✅ **Professional** - show Prof first before public  
✅ **No pressure** - tidak worry tentang inappropriate content

### Can Switch to Public Later If Needed

GitHub allows changing private → public anytime:
- Repository Settings → Danger Zone → Change visibility
- One-click process
- All history preserved

---

## 📤 How to Share with Prof (No GitHub Account)

### **Option 1: ZIP File via Email/Drive** ⭐ RECOMMENDED

Since Prof doesn't have GitHub, create a clean archive:

```bash
# Method A: Using command line (excludes large files)
cd "/Users/henri/Downloads"
zip -r internship-archive-wtmh-2025.zip "1DCNN 3" \
    -x "*/checkpoint_epoch/*" \
    -x "*/preprocessed_ecg/*" \
    -x "*/.git/*" \
    -x "*.pt" "*.pth"

# The ZIP will be in /Users/henri/Downloads/
```

**Then:**
1. Upload to Google Drive personal kamu
2. Share link dengan Prof via email
3. Write simple email:

```
Dear Prof,

Berikut dokumentasi lengkap hasil kerja selama magang di WTMH Lab 
(Agustus 2025 - Januari 2026) sesuai yang diminta.

Link: [Google Drive link]

Mohon review dan beri tahu jika ada yang perlu disesuaikan.

Terima kasih.
```

### **Option 2: Create GitHub Private Repo as Backup**

Even though Prof can't access GitHub directly, having backup is good:

**Step 1:** Create GitHub account (jika belum punya)
- Go to https://github.com/signup
- Free account is enough

**Step 2:** Create PRIVATE repository
```bash
# On GitHub.com:
# 1. Click "+" → "New repository"
# 2. Name: "wtmh-lab-internship-2025" (atau yang less specific)
# 3. Description: "Internship documentation (PRIVATE - internal use only)"
# 4. ✅ Check "Private"
# 5. Create repository
```

**Step 3:** Push your code
```bash
cd "/Users/henri/Downloads/1DCNN 3"

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Push
git push -u origin main
```

**Benefits:**
- ✅ Personal backup online
- ✅ Version control history preserved
- ✅ Can make public later if approved
- ✅ Professional portfolio piece (if made public)

---

## 🔒 Privacy Levels Explained

### Private Repository
- **Who can see:** Only you + people you invite
- **GitHub profile:** Repo name visible in your profile, but content hidden
- **Good for:** Internal documentation, work in progress
- **Cost:** FREE on GitHub

### Public Repository  
- **Who can see:** Everyone on internet
- **Searchable:** Via Google, GitHub search
- **Good for:** Portfolio, open source, sharing
- **Risk:** Prof atau lab members mungkin tidak nyaman dengan public

---

## ⚠️ Things to Consider Before Going Public

Ask yourself:

1. **Does lab allow public sharing?**
   - Some labs have policies about publishing work
   - Better ask Prof first

2. **Is all info appropriate?**
   - No sensitive information accidentally included
   - No internal lab notes or communications
   - Already sanitized via .gitignore

3. **Who owns the work?**
   - Work done during internship → lab has some rights
   - Better get approval before public

4. **Future implications?**
   - Public = permanent (even if deleted, copies exist)
   - Can affect future publications if data/methods are novel

---

## ✅ Recommended Workflow

### Phase 1: Documentation & Share (NOW)

```bash
# 1. Create ZIP for Prof
cd "/Users/henri/Downloads"
zip -r internship-wtmh-2025.zip "1DCNN 3" \
    -x "*/checkpoint_epoch/*" \
    -x "*/preprocessed_ecg/*" \
    -x "*/.git/*"

# 2. Upload to your Google Drive
# 3. Email Prof with link
# 4. Wait for feedback
```

### Phase 2: Create Private GitHub Backup (OPTIONAL)

```bash
# Only if you want version control backup
# Create private repo on GitHub.com first, then:
cd "/Users/henri/Downloads/1DCNN 3"
git remote add origin https://github.com/YOUR_USERNAME/REPO.git
git push -u origin main
```

### Phase 3: Consider Public (LATER, IF APPROVED)

- Wait for Prof's feedback on ZIP
- Ask if making it public is okay
- If yes, switch private → public on GitHub
- If no, keep private or just keep ZIP as archive

---

## 📧 Sample Email to Prof

```
Subject: Dokumentasi Magang WTMH Lab (Agustus 2025 - Januari 2026)

Dear Prof,

Sesuai permintaan, saya telah menyusun dokumentasi lengkap 
hasil kerja selama magang di WTMH Lab.

Dokumentasi mencakup:
- Complete code dan notebooks
- Methodology dan hasil eksperimen  
- Final presentation
- Weekly progress summary

Link Google Drive: [INSERT LINK]

Mohon review dan beri tahu jika ada yang perlu disesuaikan 
atau jika ada concern mengenai konten yang di-share.

Terima kasih atas bimbingan selama 6 bulan di WTMH Lab.

Best regards,
[Your name]
```

---

## 🎯 My Specific Recommendation for You

Based on your situation:

### DO THIS:

1. ✅ **Keep current local Git repo** (already done ✓)
   - Good for your own version control
   - Can track changes if Prof asks revisions

2. ✅ **Create ZIP and share with Prof via Drive**
   - Use command above
   - Simple, no GitHub needed
   - Prof can review everything

3. ✅ **Wait for Prof's feedback**
   - Maybe ada yang harus diubah
   - Maybe ada concern tentang certain info

4. ⏸️ **Hold on GitHub upload** (for now)
   - Create private repo ONLY IF you want online backup
   - Or wait until Prof approves

### DON'T DO (YET):

- ❌ Don't make public repository yet
- ❌ Don't share publicly until Prof sees it
- ❌ Don't mention personal name prominently (✓ already fixed)

---

## 🆘 Quick Commands

### Create ZIP (no large files, no git history)
```bash
cd "/Users/henri/Downloads"
zip -r internship-archive.zip "1DCNN 3" \
    -x "*/checkpoint_epoch/*" \
    -x "*/preprocessed_ecg/*" \
    -x "*/.git/*" \
    -x "*.pt"
```

### If Prof Approves GitHub Later:
```bash
# Create private repo on GitHub.com, then:
cd "/Users/henri/Downloads/1DCNN 3"
git remote add origin https://github.com/USERNAME/REPONAME.git
git push -u origin main
```

### If Prof Wants Modifications:
```bash
# Make changes, then:
git add .
git commit -m "Update based on Prof feedback"
# Re-create ZIP with updated version
```

---

## 💡 Final Thoughts

This is **your internship work documentation**, not a publication:
- Focus: Archive and record what was done
- Audience: Prof, lab, possibly future reference
- Goal: Organized documentation, not public showcase

**Safe approach:**
1. Share with Prof privately first (ZIP via Drive)
2. Get feedback
3. Decide public/private based on Prof's input
4. You still have full control over GitHub decisions

---

**Remember:** Better to be cautious than regret later. Start private, can always go public if appropriate.

**Current status:** Repository ready, just need to decide sharing method. I recommend ZIP to Prof first! 📦

---

**Updated:** February 2026
