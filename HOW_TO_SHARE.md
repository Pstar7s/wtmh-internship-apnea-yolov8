# How to Share This Repository

This guide explains different methods to share your research repository with advisors, colleagues, or for publication.

---

## 🔒 Option 1: GitHub Private Repository (Recommended for Collaboration)

### Requirements
- Target person **MUST have a GitHub account**
- You need a GitHub account

### Steps

1. **Create GitHub Repository**
   ```bash
   # On GitHub.com, create a new PRIVATE repository
   # Name: sleep-apnea-ecg-frequency-exploration
   ```

2. **Add Remote and Push**
   ```bash
   cd "/Users/henri/Downloads/1DCNN 3"
   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

3. **Invite Collaborators**
   - Go to: Repository → Settings → Collaborators
   - Click "Add people"
   - Enter GitHub username or email
   - Choose access level:
     - **Read**: Can view and clone only
     - **Write**: Can push changes
     - **Admin**: Full control

### ✅ Pros
- Version control and collaboration
- Easy updates for all collaborators
- Professional presentation
- Issue tracking and discussions

### ❌ Cons
- Requires GitHub account for all viewers
- Public profile (even for private repos)

---

## 📦 Option 2: ZIP Archive (Recommended for Non-GitHub Users)

### Best For
- Advisors without GitHub
- Submitting with thesis/paper
- Email attachments

### Steps

```bash
# Create clean archive (excludes data and git history)
cd "/Users/henri/Downloads"
zip -r sleep-apnea-research-faiz.zip "1DCNN 3" \
    -x "*/checkpoint_epoch/*" \
    -x "*/preprocessed_ecg/*" \
    -x "*/.git/*" \
    -x "*.pt" "*.pth" "*.edf" "*.xml" "*.npy"
```

**Or manually:**
1. Copy entire folder to new location
2. Delete sensitive folders:
   - `checkpoint_epoch/`
   - `preprocessed_ecg/`
   - `.git/` (optional, removes git history)
3. ZIP the folder
4. Share via email/Google Drive/OneDrive

### ✅ Pros
- No account needed
- Simple and familiar
- Works everywhere

### ❌ Cons
- No version control
- Large file size
- Manual updates needed

---

## 🌐 Option 3: GitHub Pages (Public Documentation)

### Best For
- Public portfolio
- Sharing documentation only (no code)
- Professional presentation

### Steps

1. **Create Public Repository for Docs Only**
   ```bash
   # Create new repo with only documentation
   mkdir sleep-apnea-docs
   cp -r docs/* sleep-apnea-docs/
   cp README.md sleep-apnea-docs/
   # Initialize and push
   ```

2. **Enable GitHub Pages**
   - Repository → Settings → Pages
   - Source: main branch
   - Theme: Choose a theme

3. **Share Link**
   - URL: `https://YOUR_USERNAME.github.io/REPO_NAME`

### ✅ Pros
- Beautiful presentation
- No GitHub account needed to view
- Good for portfolio

### ❌ Cons
- Documentation only (no code)
- Public access

---

## 📤 Option 4: Google Drive + Git Bundle

### Best For
- WTMH Lab internal sharing
- Maintaining git history without GitHub

### Steps

1. **Create Git Bundle**
   ```bash
   cd "/Users/henri/Downloads/1DCNN 3"
   git bundle create ../sleep-apnea-research.bundle --all
   ```

2. **Upload to Google Drive**
   - Upload `sleep-apnea-research.bundle`
   - Share link with specific people

3. **Recipient Clones from Bundle**
   ```bash
   git clone sleep-apnea-research.bundle sleep-apnea-research
   cd sleep-apnea-research
   ```

### ✅ Pros
- Maintains full git history
- No GitHub needed
- Private sharing

### ❌ Cons
- Requires git knowledge
- Larger file size

---

## 📧 Option 5: Selective Sharing (Custom Package)

### Best For
- Different audiences (advisor vs. public)
- Customized content

### Package Variants

#### For Advisor/Lab (Complete)
```
✅ All code and notebooks
✅ Documentation
✅ Results and figures
✅ Final presentation
❌ Raw data (never share)
❌ Model checkpoints (too large)
```

#### For Publication/Public (Minimal)
```
✅ README and methodology
✅ Key code snippets
✅ Aggregated results
✅ Architecture diagrams
❌ Full notebooks
❌ Internal documentation
```

---

## ⚠️ Important Reminders

### NEVER Include These Files

```
❌ *.edf, *.EDF           # Raw ECG data
❌ *.xml, *.XML           # Patient annotations
❌ preprocessed_ecg/*.npy # Processed segments
❌ Any patient identifiers
```

### Safe to Share

```
✅ Code (.py, .ipynb)
✅ Documentation (.md)
✅ Aggregated results (.csv tables)
✅ Visualizations (confusion matrices, plots)
✅ Model architectures (code only, not weights)
✅ requirements.txt, .gitignore
```

---

## 🎯 Recommended Approach by Audience

| Audience | Method | Why |
|----------|--------|-----|
| **Advisor/Prof. Lin** | ZIP + Drive | Simple, complete access |
| **Lab Members (WTMH)** | Private GitHub | Collaboration, version control |
| **Future Employers** | Public GitHub (sanitized) | Professional portfolio |
| **Paper Reviewers** | ZIP with paper submission | Standard practice |
| **Public/Portfolio** | GitHub Pages | Beautiful presentation |

---

## 📝 Quick Commands Reference

### Check What Will Be Committed
```bash
git status
git status --ignored  # See ignored files
```

### Create Clean Archive
```bash
zip -r archive.zip "1DCNN 3" -x "*/checkpoint_epoch/*" "*/preprocessed_ecg/*" "*/.git/*"
```

### Push to GitHub (if you create repo)
```bash
git remote add origin https://github.com/USERNAME/REPO.git
git push -u origin main
```

### Create Git Bundle
```bash
git bundle create research.bundle --all
```

---

## 🆘 Help

**For WTMH Lab members:** Contact lab IT support  
**For GitHub issues:** See [GitHub Docs](https://docs.github.com)  
**For data privacy questions:** Contact NCKUHSC IRB

---

**Last Updated:** February 2026  
**Prepared by:** Faiz Henri Kurniawan
