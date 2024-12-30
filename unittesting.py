import unittest
import logging
from statreader import StatReader

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=
    [
        #logging.FileHandler("log.txt"),
        logging.StreamHandler()
    ]
)

# Test cases
class TestOCR(unittest.TestCase):


    def test_Alice(self):
        sr = StatReader()

        sr.ReadFileImage("./unittests/Alice Head.png")
        sr.ReadFileImage("./unittests/Alice Torso.png")
        sr.ReadFileImage("./unittests/Alice Arm.jpg")
        sr.ReadFileImage("./unittests/Alice Leg.jpg")

        self.assertEqual(sr.totals["increase element damage dealt"], 31.69)
        self.assertEqual(sr.totals["increase max ammunition capacity"], 292.16)
        self.assertEqual(sr.totals["increase critical damage"], 0.0)
        self.assertEqual(sr.totals["increase critical rate"], 2.64)
        self.assertEqual(sr.totals["increase charge damage"], 0.0)
        self.assertEqual(sr.totals["increase charge speed"], 10.43)
        self.assertEqual(sr.totals["increase hit rate"], 0.0)
        self.assertEqual(sr.totals["increase atk"], 0.0)
        self.assertEqual(sr.totals["increase def"], 5.47)


    def test_Emilia(self):
        sr = StatReader()

        sr.ReadFileImage("./unittests/Emilia Head.jpg")
        sr.ReadFileImage("./unittests/Emilia Torso.jpg")
        sr.ReadFileImage("./unittests/Emilia Arm.jpg")
        sr.ReadFileImage("./unittests/Emilia Leg.jpg")

        self.assertEqual(sr.totals["increase element damage dealt"], 16.55)
        self.assertEqual(sr.totals["increase max ammunition capacity"], 190.36)
        self.assertEqual(sr.totals["increase critical damage"], 16.44)
        self.assertEqual(sr.totals["increase critical rate"], 10.06)
        self.assertEqual(sr.totals["increase charge damage"], 0.0)
        self.assertEqual(sr.totals["increase charge speed"], 0.0)
        self.assertEqual(sr.totals["increase hit rate"], 0.0)
        self.assertEqual(sr.totals["increase atk"], 9.00)
        self.assertEqual(sr.totals["increase def"], 0.0)


    def test_Biscuit(self):
        sr = StatReader()

        sr.ReadFileImage("./unittests/Biscuit Torso.jpg")
        sr.ReadFileImage("./unittests/Biscuit Leg.jpg")

        self.assertEqual(sr.totals["increase element damage dealt"], 38.71)
        self.assertEqual(sr.totals["increase max ammunition capacity"], 27.84)
        self.assertEqual(sr.totals["increase critical damage"], 0.0)
        self.assertEqual(sr.totals["increase critical rate"], 0.0)
        self.assertEqual(sr.totals["increase charge damage"], 0.0)
        self.assertEqual(sr.totals["increase charge speed"], 4.92)
        self.assertEqual(sr.totals["increase hit rate"], 0.0)
        self.assertEqual(sr.totals["increase atk"], 0.0)
        self.assertEqual(sr.totals["increase def"], 11.81)


if __name__ == "__main__":
    unittest.main()
