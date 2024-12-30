import unittest
import logging
from statreader import StatReader

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        # logging.FileHandler("log.txt"),
        logging.StreamHandler()
    ],
)


# Test cases
class TestStatReader(unittest.TestCase):

    def test_Alice(self):
        sr = StatReader()

        sr.ReadFileImage("./unittests/Alice Head.png")
        sr.ReadFileImage("./unittests/Alice Torso.png")
        sr.ReadFileImage("./unittests/Alice Arm.jpg")
        sr.ReadFileImage("./unittests/Alice Leg.jpg")

        self.assertEqual(f"{sr.totals['element damage dealt']:.2f}", "31.69")
        self.assertEqual(f"{sr.totals['max ammunition capacity']:.2f}", "292.16")
        self.assertEqual(f"{sr.totals['critical damage']:.2f}", "0.00")
        self.assertEqual(f"{sr.totals['critical rate']:.2f}", "2.64")
        self.assertEqual(f"{sr.totals['charge damage']:.2f}", "0.00")
        self.assertEqual(f"{sr.totals['charge speed']:.2f}", "10.43")
        self.assertEqual(f"{sr.totals['hit rate']:.2f}", "0.00")
        self.assertEqual(f"{sr.totals['atk']:.2f}", "0.00")
        self.assertEqual(f"{sr.totals['def']:.2f}", "5.47")

    def test_Emilia(self):
        sr = StatReader()

        sr.ReadFileImage("./unittests/Emilia Head.jpg")
        sr.ReadFileImage("./unittests/Emilia Torso.jpg")
        sr.ReadFileImage("./unittests/Emilia Arm.jpg")
        sr.ReadFileImage("./unittests/Emilia Leg.jpg")

        self.assertEqual(f"{sr.totals['element damage dealt']:.2f}", "16.55")
        self.assertEqual(f"{sr.totals['max ammunition capacity']:.2f}", "190.36")
        self.assertEqual(f"{sr.totals['critical damage']:.2f}", "16.44")
        self.assertEqual(f"{sr.totals['critical rate']:.2f}", "10.06")
        self.assertEqual(f"{sr.totals['charge damage']:.2f}", "0.00")
        self.assertEqual(f"{sr.totals['charge speed']:.2f}", "0.00")
        self.assertEqual(f"{sr.totals['hit rate']:.2f}", "0.00")
        self.assertEqual(f"{sr.totals['atk']:.2f}", "9.00")
        self.assertEqual(f"{sr.totals['def']:.2f}", "0.00")

    def test_Biscuit(self):
        sr = StatReader()

        sr.ReadFileImage("./unittests/Biscuit Torso.jpg")
        sr.ReadFileImage("./unittests/Biscuit Leg.jpg")

        self.assertEqual(f"{sr.totals['element damage dealt']:.2f}", "38.71")
        self.assertEqual(f"{sr.totals['max ammunition capacity']:.2f}", "27.84")
        self.assertEqual(f"{sr.totals['critical damage']:.2f}", "0.00")
        self.assertEqual(f"{sr.totals['critical rate']:.2f}", "0.00")
        self.assertEqual(f"{sr.totals['charge damage']:.2f}", "0.00")
        self.assertEqual(f"{sr.totals['charge speed']:.2f}", "4.92")
        self.assertEqual(f"{sr.totals['hit rate']:.2f}", "0.00")
        self.assertEqual(f"{sr.totals['atk']:.2f}", "0.00")
        self.assertEqual(f"{sr.totals['def']:.2f}", "11.81")


if __name__ == "__main__":
    unittest.main()
