import os
import sys
from tempfile import mkdtemp
import logging


sys.path.insert(0, os.path.abspath('..'))


if "cbac_test_products" in os.environ:
    product_dir = os.environ["cbac_test_products"]
else:
    logging.warning("You have'nt set cbac_test_products path in your environment variables.")
    product_dir = mkdtemp()
    

if not os.path.exists(product_dir):
    os.makedirs(product_dir)
