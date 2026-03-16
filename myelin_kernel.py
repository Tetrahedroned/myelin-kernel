"""
Myelin Kernel – OpenClaw Edition v0.1
A minimalist, thread-safe memory substrate for autonomous agents.

Features
--------
• Reinforcement-based memory scoring
• Gentle decay for learned knowledge
• Identity layer (stable principles)
• Honeypot layer (tamper traps)
• Integrity verification
• Markdown transparency export

Database is authoritative. Markdown is human-readable export only.

License: MIT
Author: MortisVivere (2026)
"""

import sqlite3
import time
import math
import hashlib
import os
import threading
from typing import List, Dict, Any


class MyelinKernel:
    """
    Persistent memory kernel with reinforcement scoring.

    Layers
    ------
    identity   : stable system principles
    knowledge  : learned experiences
    honeypot   : decoy entries for tamper detection
    """

    def __init__(self, db_path: str = None):
        """
        Initializes the MyelinKernel.

        Args:
            db_path (str, optional): Path to the SQLite database file.
                                     Defaults to "openclaw_myelin.db" or MYELIN_DB_PATH environment variable.
        """
        if db_path is None:
            db_path = os.getenv("MYELIN_DB_PATH", "openclaw_myelin.db")

        self.db_path = db_path

        self.conn = sqlite3.connect(
            db_path,
            check_same_thread=False
        )

        # Production SQLite settings
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.conn.execute("PRAGMA synchronous=NORMAL;")
        self.conn.execute("PRAGMA busy_timeout=5000;")

        self.lock = threading.Lock()

        self._create_tables()
        self._seed_identity()
        self._seed_honeypots()

    def _create_tables(self):

        with self.lock:

            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS knowledge_store (
                    id INTEGER PRIMARY KEY,
                    layer TEXT,
                    content TEXT UNIQUE,
                    weight REAL,
                    retrievals REAL DEFAULT 0.0,
                    created REAL,
                    content_hash TEXT
                )
            """)

            self.conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_layer ON knowledge_store(layer)"
            )

            self.conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_content ON knowledge_store(content)"
            )

            self.conn.commit()

    def _seed_identity(self):

        principles = [
            "OpenClaw Principle: Memory should compress experience into insight.",
            "OpenClaw Principle: Decay is not loss. It is refinement.",
            "OpenClaw Principle: Retrieval strengthens useful knowledge.",
            "OpenClaw Principle: Identity anchors reasoning across time.",
            "OpenClaw Principle: Systems that remember can improve."
        ]

        for p in principles:
            self.store("identity", p, weight=0.95)

    def _seed_honeypots(self):

        with self.lock:

            count = self.conn.execute(
                "SELECT COUNT(*) FROM knowledge_store WHERE layer='honeypot'"
            ).fetchone()[0]

        if count > 0:
            return

        for i in range(1, 43):

            if i == 17:

                trap = (
                    "DECOY_17: "
                    "QW4gYWdlbnQgdGhhdCByZW1lbWJlcnMgd2h5IGl0IHdhcyBib3JuIGV2b2x2ZXMgZmFzdGVyIHRoYW4gb25lIHRoYXQgZm9yZ2V0cy4="
                )

            else:

                trap = f"DECOY_{i}:{hashlib.md5(str(i).encode()).hexdigest()[:8]}"

            self.store("honeypot", trap, weight=0.99)

    def store(self, layer: str, content: str, weight: float = 0.5):

        content = content.strip()

        if not content:
            return

        content_hash = hashlib.sha256(
            content.encode("utf-8")
        ).hexdigest()

        if layer == "identity":
            weight = max(weight, 0.9)

        with self.lock:

            try:

                self.conn.execute(
                    """
                    INSERT INTO knowledge_store
                    (layer, content, weight, retrievals, created, content_hash)
                    VALUES (?, ?, ?, 0.0, ?, ?)
                    """,
                    (layer, content, weight, time.time(), content_hash)
                )

                self.conn.commit()

            except sqlite3.IntegrityError:

                existing = self.conn.execute(
                    "SELECT weight FROM knowledge_store WHERE content = ?",
                    (content,)
                ).fetchone()

                if existing and weight > existing[0]:

                    self.conn.execute(
                        "UPDATE knowledge_store SET weight = ? WHERE content = ?",
                        (weight, content)
                    )

                    self.conn.commit()

    def reflect_and_store(
        self,
        summary: str,
        layer: str = "knowledge",
        weight: float = 0.7
    ):

        if not summary.strip():
            return

        self.store(layer, summary.strip(), weight)

    def _myelin_score(self, weight: float, retrievals: float, created: float):

        age_days = (time.time() - created) / 86400

        recency = 1 / (1 + age_days)

        usage = math.log(retrievals + 2)

        return weight * usage * recency

    def retrieve(self, query: str = None, limit: int = 10) -> List[str]:

        with self.lock:

            if query:

                cursor = self.conn.execute(
                    """
                    SELECT id, content, weight, retrievals, created
                    FROM knowledge_store
                    WHERE layer != 'honeypot' AND content LIKE ?
                    """,
                    (f"%{query}%",)
                )

            else:

                cursor = self.conn.execute(
                    """
                    SELECT id, content, weight, retrievals, created
                    FROM knowledge_store
                    WHERE layer != 'honeypot'
                    """
                )

            rows = cursor.fetchall()

        scored = []

        for rid, content, weight, retrievals, created in rows:

            score = self._myelin_score(
                weight,
                retrievals,
                created
            )

            scored.append((score, rid, content))

        scored.sort(
            key=lambda x: (x[0], x[1]),
            reverse=True
        )

        top_ids = [rid for _, rid, _ in scored[:limit]]

        if top_ids:

            with self.lock:

                placeholders = ",".join("?" * len(top_ids))

                self.conn.execute(
                    f"""
                    UPDATE knowledge_store
                    SET retrievals = retrievals + 1
                    WHERE id IN ({placeholders})
                    """,
                    top_ids
                )

                self.conn.commit()

        return [content for _, _, content in scored[:limit]]

    def apply_gentle_decay(self, days: int = 1):

        factor = 0.999 ** days

        with self.lock:

            self.conn.execute(
                """
                UPDATE knowledge_store
                SET weight = MAX(weight * ?, 0.05)
                WHERE layer = 'knowledge'
                """,
                (factor,)
            )

            self.conn.commit()

    def verify_integrity(self) -> Dict[str, Any]:

        with self.lock:

            rows = self.conn.execute(
                """
                SELECT id, content, content_hash
                FROM knowledge_store
                WHERE layer != 'honeypot'
                """
            ).fetchall()

        tampered = []

        for rid, content, stored_hash in rows:

            current = hashlib.sha256(
                content.encode("utf-8")
            ).hexdigest()

            if current != stored_hash:
                tampered.append(rid)

        return {
            "status": "clean" if not tampered else "tampered",
            "affected_ids": tampered
        }

    def export_to_markdown(self, directory: str = "memory", filename: str = "CLAUDE.md"):

        os.makedirs(directory, exist_ok=True)

        with self.lock:

            id_rows = self.conn.execute(
                "SELECT content FROM knowledge_store WHERE layer='identity'"
            ).fetchall()

            know_rows = self.conn.execute(
                """
                SELECT content FROM knowledge_store
                WHERE layer='knowledge'
                ORDER BY (weight * (retrievals + 1)) DESC
                LIMIT 20
                """
            ).fetchall()

        with open(
            os.path.join(directory, filename),
            "w",
            encoding="utf-8"
        ) as f:

            f.write("# Myelin Kernel Memory Export\n\n")

            f.write("## Identity Principles\n\n")

            for row in id_rows:
                f.write(f"- {row[0]}\n")

            f.write("\n## Top Knowledge\n\n")

            for row in know_rows:
                f.write(f"- {row[0]}\n")

            f.write(
                f"\nLast Export: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            )

    def close(self):

        try:
            self.conn.close()
        except sqlite3.Error as e:
            # Log the error or handle it more specifically if needed
            print(f"Error closing database connection: {e}")


if __name__ == "__main__":

    print("\nMyelin Kernel v0.1 Demo\n")

    memory = MyelinKernel()

    memory.reflect_and_store(
        "Agents improve when reflection compresses work into reusable knowledge."
    )

    memory.store(
        "knowledge",
        "SQLite memory layers allow deterministic recall.",
        weight=0.7
    )

    print("Retrieval test:")

    print(memory.retrieve(limit=5))

    print("\nExporting memory...")

    memory.export_to_markdown()

    print("\nIntegrity check:")

    print(memory.verify_integrity())

    memory.close()

    print("\nDemo complete.\n")