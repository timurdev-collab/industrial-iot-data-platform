import tempfile, unittest
from pathlib import Path
import json
from pipeline.generate import generate
from pipeline.load import load, validate

class PipelineTests(unittest.TestCase):
    def test_generation_is_deterministic(self):
        self.assertEqual(generate(10), generate(10))
    def test_invalid_readings_rejected(self):
        row = generate(1)[0]
        row['pressure_bar'] = -100
        self.assertFalse(validate(row))
    def test_load_is_idempotent(self):
        with tempfile.TemporaryDirectory() as d:
            src = Path(d)/'events.jsonl'
            db = Path(d)/'data.db'
            src.write_text(''.join(json.dumps(r)+'\n' for r in generate(30)))
            self.assertEqual(load(src,db)['inserted'],30)
            self.assertEqual(load(src,db)['inserted'],0)

if __name__ == '__main__':
    unittest.main()
