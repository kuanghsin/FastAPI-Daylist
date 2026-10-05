import os
import secrets


# 優先使用執行環境的連線設定；預設值僅供本機無密碼的 MySQL 練習環境使用。
# 若密碼含有特殊字元，請先對連線字串中的密碼進行 URL 編碼。
DATABASE_URL = os.getenv(
    "DATABASE_URL", "mysql+pymysql://root:@localhost:3306/fastapi_db"
)

# 未設定時使用每次啟動都不同的金鑰（重啟後需重新登入）。
SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY") or secrets.token_urlsafe(32)
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"
