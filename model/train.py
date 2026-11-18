import json
from pathlib import Path
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from app.features import extract_features

# Balanced labelled dataset (0 = legitimate, 1 = phishing)
DATASET = [
    ("https://www.google.com", 0), ("https://github.com/login", 0),
    ("https://www.microsoft.com/en-in", 0), ("https://docs.python.org/3/", 0),
    ("https://www.amazon.in/dp/B09G9BL5CP", 0), ("https://stackoverflow.com/questions", 0),
    ("https://www.wikipedia.org/wiki/DevOps", 0), ("https://www.linkedin.com/feed/", 0),
    ("https://www.icicibank.com/personal-banking", 0), ("https://www.hdfcbank.com/", 0),
    ("https://fastapi.tiangolo.com/tutorial/", 0), ("https://kubernetes.io/docs/home/", 0),
    ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", 0), ("https://www.reddit.com/r/MachineLearning/", 0),
    ("https://www.apple.com/in/macbook-air/", 0), ("https://www.cloudflare.com/learning/", 0),
    ("https://scikit-learn.org/stable/index.html", 0), ("https://www.jenkins.io/doc/", 0),
    ("https://www.coursera.org/browse/data-science", 0), ("https://www.nytimes.com/section/technology", 0),
    ("http://paypa1-secure-login-update.xyz/verify", 1), ("http://192.168.1.45/banking/login.php", 1),
    ("http://amazon-account-confirm-bonus.tk/signin", 1), ("http://secure-hdfc-kyc-update.ml/login", 1),
    ("http://www.google.com@evil-phish-site.ru/auth", 1), ("http://apple-id-verify-suspended123.ga/account", 1),
    ("http://free-bonus-claim-paypal-secure.cf/login", 1), ("http://10.0.0.88/icici-netbanking-confirm", 1),
    ("http://microsoft-365-password-update-alert.xyz", 1), ("http://signin-amazon-prime-free-gift99.top", 1),
    ("http://verify-your-bank-account-now-secure.info/id", 1), ("http://login.paypal.com.user-verify-1029.net", 1),
    ("http://update-billing-apple-support-team.club", 1), ("http://172.16.254.1/secure/login/verify", 1),
    ("http://account-locked-confirm-details-fast.biz", 1), ("http://netflix-payment-update-required-88.xyz", 1),
    ("http://sbi-online-kyc-bonus-update.online/signin", 1), ("http://www.dropbox.com@malicious-download.cc", 1),
    ("http://secure-login-github-token-verify.site", 1), ("http://claim-free-iphone-amazon-survey77.win", 1),
]

def train():
    X = [extract_features(url) for url, _ in DATASET]
    y = [label for _, label in DATASET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    clf = RandomForestClassifier(n_estimators=50, random_state=42)
    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    metrics = {
        "model_type": "RandomForestClassifier",
        "version": "1.0.0",
        "accuracy": round(accuracy_score(y_test, preds), 4),
        "precision": round(precision_score(y_test, preds), 4),
        "recall": round(recall_score(y_test, preds), 4),
        "f1_score": round(f1_score(y_test, preds), 4),
    }

    out_dir = Path(__file__).parent
    joblib.dump(clf, out_dir / "model.joblib")
    (out_dir / "metrics.json").write_text(json.dumps(metrics, indent=2))
    print("Training complete! Metrics:", json.dumps(metrics, indent=2))

if __name__ == "__main__":
    train()