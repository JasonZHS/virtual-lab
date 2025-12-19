import unittest
from alzkb.ingestion.haplotype_computer import compute_haplotype

class TestHaplotypeComputer(unittest.TestCase):

    def test_e3e4_standard(self):
        # rs429358 (C/T) + rs7412 (C/C) -> e3/e4
        result = compute_haplotype('C/T', 'C/C')
        self.assertEqual(result['label'], 'e3/e4')
        self.assertEqual(result['confidence'], 0.99)

    def test_e4e4_high_risk(self):
        # rs429358 (C/C) + rs7412 (C/C) -> e4/e4
        result = compute_haplotype('C/C', 'C/C')
        self.assertEqual(result['label'], 'e4/e4')
        self.assertEqual(result['risk_uri'], 'alzkb:Risk_VeryHigh')

    def test_strand_flip(self):
        # rs429358 (A/G) should flip to T/C
        # rs7412 (G/G) should flip to C/C
        # Result: T/C + C/C -> e3/e4
        result = compute_haplotype('A/G', 'G/G')
        self.assertEqual(result['label'], 'e3/e4')
    
    def test_confidence_decay(self):
        # Low GQ score inputs
        result = compute_haplotype('C/T', 'C/C', rs429358_gq=50.0)
        self.assertEqual(result['confidence'], 0.5)

    def test_phasing_penalty_e2e4(self):
        # e2/e4 (C/T + C/T) has ambiguity penalty
        result = compute_haplotype('C/T', 'C/T')
        self.assertEqual(result['label'], 'e2/e4')
        self.assertLess(result['confidence'], 0.99) # Should be penalized

if __name__ == '__main__':
    unittest.main()
