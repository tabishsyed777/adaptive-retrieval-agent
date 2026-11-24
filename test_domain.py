import unittest
import core

class DomainTests(unittest.TestCase):
    def test_fallback_tie(self):
        rows=core.read(core.DEFAULT)
        rows[2]["keywords"]=rows[0]["keywords"]
        self.assertIsNone(core.answer(rows,"find build archives for basic")["answer"])

    def test_missing_comparison(self):
        self.assertIsNone(core.answer(core.read(core.DEFAULT)[1:],"compare artifact retention across tiers")["answer"])

    def test_challenge_queries(self):
        rows=core.validate(core.read(core.DEFAULT))
        for query,expected in core.read(core.DEFAULT.parent.parent/"qa/challenge.json"):
            with self.subTest(query=query):
                self.assertEqual(core.answer(rows,query)["answer"],expected)
