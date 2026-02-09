import sqlite3
import secrets
from engine import get_db

POOL_SIZE = 100


class Repository_short_url:

    def refill_pool(self, n: int = POOL_SIZE):
        # генератор в пулл см engine
        with get_db() as conn:
            for _ in range(n):
                key = secrets.token_urlsafe(6)
                try:
                    conn.execute(
                        "INSERT INTO idempotency_pool (key, status) VALUES (?, 'available')",
                        (key,)
                    )
                except sqlite3.IntegrityError:
                    # ключ уже есть, пропускаем
                    continue

    def create_short_url(self, url: str) -> str:
        with get_db() as conn:
            #Берём ключ из pool key
            row = conn.execute(
                "SELECT key FROM idempotency_pool WHERE status='available' LIMIT 1"
            ).fetchone()

            if row is None:

                self.refill_pool()
                row = conn.execute(
                    "SELECT key FROM idempotency_pool WHERE status='available' LIMIT 1"
                ).fetchone()

            key = row[0]

            # переводим в reserved ключ
            conn.execute(
                "UPDATE idempotency_pool SET status='reserved' WHERE key=?",
                (key,)
            )

            #сокращение
            try:
                conn.execute(
                    "INSERT INTO reduction_url_model (idempotency_key, url) VALUES (?, ?)",
                    (key, url)
                )
            except sqlite3.IntegrityError:
                # если кто-то успел вставить — берём существующую ссылку
                url = conn.execute(
                    "SELECT url FROM reduction_url_model WHERE idempotency_key=?",
                    (key,)
                ).fetchone()[0]

            # Помечаем used в idempotency_pool
            conn.execute(
                "UPDATE idempotency_pool SET status='used' WHERE key=?",
                (key,)
            )

        return key

    def get_short_url(self, code: str) -> str | None:
        with get_db() as conn:
            row = conn.execute(
                "SELECT url FROM reduction_url_model where idempotency_key=?", (code,)
            ).fetchone()

            if row is None:
                return None

            return row[0]
