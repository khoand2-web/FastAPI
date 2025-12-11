from app.database import engine

try:
    with engine.connect() as conn:
        print("Kết nối PostgreSQL thành công!")
except Exception as e:
    print("Lỗi kết nối:", e)

