# LogIQ CLI Tool v1.7.0 Release Notes

## 📅 Release Date: October 12, 2025

## 🎯 Focus: UX polish, stability and minor performance improvements

This release refines the CLI user experience, strengthens stability on shutdown (especially on Windows), and applies light performance optimizations to status update paths.

## ✨ Highlights

### UX & Messaging

- Clearer `--help` output and error messages
- More consistent exit codes for scripts/automation

### Stability

- More resilient shutdown flow when Ctrl+C or terminal closes
- Addressed intermittent Windows-specific cleanup edge cases

### Performance

- Minor optimizations in status update paths

## 🧩 Technical Notes

- Validated dependency set with Python 3.12 compatibility
- Continued hardening around cleanup and status updates

## 📦 Installation

```bash
pip install logiq-cli==1.7.0
```

## 🔄 Upgrade Notes

- No breaking changes
- Recommended upgrade for improved UX and shutdown stability

## ✅ Verification

- Manual smoke tests for login, profile setup, monitoring start/stop
- Verified clean shutdown on Windows and Linux with Ctrl+C

## 📌 Files Updated in 1.7.0

- `setup.py` and `__init__.py` – version bump to 1.7.0
- `CHANGELOG.md` – added 1.7.0 section
- `README.md` – updated with 1.7.0 highlights

---

Thanks for using LogIQ CLI. Feedback welcome to keep polishing the experience!
