import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "ascend50.db"

HDX_APP_ID = os.getenv("HDX_APP_IDENTIFIER", "")
HDX_BASE = "https://hapi.humdata.org/api/v2"
WB_BASE = "https://api.worldbank.org/v2/country/HTI/indicator"

WB_INDICATORS = {
    "NY.GDP.MKTP.CD": "GDP (current US$)",
    "NY.GDP.MKTP.KD.ZG": "GDP growth (annual %)",
    "NY.GNP.PCAP.CD": "GNI per capita (current US$)",
    "SP.POP.TOTL": "Population, total",
    "FP.CPI.TOTL.ZG": "Inflation, consumer prices (annual %)",
    "EG.ELC.ACCS.ZS": "Access to electricity (% of population)",
    "SL.UEM.TOTL.ZS": "Unemployment (% of labor force)",
    "SH.XPD.CHEX.GD.ZS": "Health expenditure (% of GDP)",
    "SI.POV.NAHC": "Poverty headcount ratio (% of population)",
    "IT.NET.USER.ZS": "Internet users (% of population)",
    "AG.LND.FRST.ZS": "Forest area (% of land area)",
    "IQ.CPA.TRAN.XQ": "CPIA transparency rating",
    "IQ.CPA.BREG.XQ": "CPIA business regulatory quality",
    "BX.TRF.PWKR.CD.DT": "Personal remittances received (US$)",
    "BX.TRF.PWKR.DT.GD.ZS": "Personal remittances (% of GDP)",
}
