import os
import sqlite3
import threading
import random
from myelin_kernel import MyelinKernel

def setup_module():
    """Cleanup old test databases."""
    for f in ["test_memory.db", "test_decay.db", "test_threads.db", "test_tamper.db"]:
        if os.path.exists(f):
            os.remove(f)

def test_store_and_retrieve():
    memory = MyelinKernel("test_memory.db")
    memory.store("knowledge", "test fact", weight=0.6)
    # Using a query ensures we find the specific fact regardless of rank
    results = memory.retrieve(query="test fact", limit=5)
    assert "test fact" in results
    memory.close()

def test_decay_and_scoring():
    memory = MyelinKernel("test_decay.db")
    memory.store("knowledge", "fading memory", weight=0.2)
    memory.store("knowledge", "strong insight", weight=0.9)
    memory.apply_gentle_decay(days=30)
    # Stronger weights should still rank higher
    results = memory.retrieve(query="strong insight", limit=1)
    assert results[0] == "strong insight"
    memory.close()

def test_concurrency():
    memory = MyelinKernel("test_threads.db")
    def worker(i):
        memory.store("knowledge", f"thread data {i}")
        memory.retrieve(query="thread")
    threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
    for t in threads: t.start()
    for t in threads: t.join()
    results = memory.retrieve(query="thread", limit=10)
    assert len(results) > 0
    memory.close()

def test_tamper_detection():
    db_name = "test_tamper.db"
    memory = MyelinKernel(db_name)
    memory.store("knowledge", "secure principle", weight=0.5)
    raw_conn = sqlite3.connect(db_name)
    raw_conn.execute("UPDATE knowledge_store SET content = 'TAMPERED' WHERE content = 'secure principle'")
    raw_conn.commit()
    raw_conn.close()
    report = memory.verify_integrity()
    assert report["status"] == "tampered"
    memory.close()

def test_agent_simulation():
    """Test #5: Verifies the kernel's ability to handle iterative agent reflection."""
    memory = MyelinKernel("test_agent.db")
    insights = [
        "Breaking tasks into steps improves reasoning.",
        "Retrieval of prior knowledge improves decision making.",
        "Reflection compresses experience into reusable insight."
    ]

    # Simulate a high-frequency reflection loop
    for _ in range(15):
        memory.reflect_and_store(random.choice(insights))

    # Verify that the 'knowledge' layer is populating and retrieving
    recalled = memory.retrieve(limit=20)
    assert len(recalled) > 0
    # Check that at least one of our insights survived the scoring
    assert any(any(i in r for i in insights) for r in recalled)
    memory.close()

def test_store_empty_content():
    memory = MyelinKernel("test_empty_content.db")
    initial_count = len(memory.retrieve(limit=100)) # Get initial count of all memories
    memory.store("knowledge", "", weight=0.5)
    final_count = len(memory.retrieve(limit=100))
    assert initial_count == final_count, "Empty content should not be stored"
    memory.close()

def test_retrieve_no_match():
    memory = MyelinKernel("test_no_match.db")
    memory.store("knowledge", "unique fact", weight=0.5)
    results = memory.retrieve(query="nonexistent", limit=5)
    assert len(results) == 0, "Retrieving with no match should return empty list"
    memory.close()

def test_reflect_and_store_direct():
    memory = MyelinKernel("test_reflect_direct.db")
    insight = "Direct reflection works."
    memory.reflect_and_store(insight)
    results = memory.retrieve(query=insight, limit=1)
    assert insight in results, "Direct reflect_and_store should store and retrieve the insight"
    memory.close()

def test_export_to_markdown():
    memory = MyelinKernel("test_export.db")
    memory.store("knowledge", "exportable fact", weight=0.5)
    export_dir = "memory_test_export"
    export_file = "test_export.md"
    full_path = os.path.join(export_dir, export_file)

    if os.path.exists(full_path):
        os.remove(full_path)
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)

    memory.export_to_markdown(directory=export_dir, filename=export_file)
    assert os.path.exists(full_path), "Exported markdown file should exist"

    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "# Myelin Kernel Memory Export" in content
        assert "## Identity Principles" in content
        assert "## Top Knowledge" in content
        assert "exportable fact" in content

    os.remove(full_path)
    os.rmdir(export_dir) # Clean up directory if empty
    memory.close()

if __name__ == "__main__":
    setup_module()
    try:
        test_store_and_retrieve()
        print("✅ Store/Retrieve Passed")
        test_decay_and_scoring()
        print("✅ Decay/Scoring Passed")
        test_concurrency()
        print("✅ Thread-Safety Passed")
        test_tamper_detection()
        print("✅ Integrity/Tamper Passed")
        test_agent_simulation()
        print("✅ Agent Simulation Passed")
        test_store_empty_content()
        print("✅ Store Empty Content Passed")
        test_retrieve_no_match()
        print("✅ Retrieve No Match Passed")
        test_reflect_and_store_direct()
        print("✅ Reflect And Store Direct Passed")
        test_export_to_markdown()
        print("✅ Export To Markdown Passed")
        print("\n⭐ ALL SYSTEMS OPERATIONAL")
    except Exception as e:
        print(f"❌ Test Suite Failed: {e}")