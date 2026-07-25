import urllib.request, urllib.parse, json
import sqlite3, sys

BASE = "https://ghoapi.azureedge.net/api"

INDICATORS = [
    # Mortality
    ("WHOSIS_000001", "Life expectancy at birth", "years"),
    ("WHOSIS_000002", "Healthy life expectancy at birth", "years"),
    ("WHOSIS_000003", "Neonatal mortality rate", "per_1000"),
    ("WHOSIS_000004", "Adult mortality rate (15-60)", "per_1000"),
    ("MDG_0000000001", "Infant mortality rate", "per_1000"),
    ("MDG_0000000007", "Under-5 mortality rate", "per_1000"),
    ("MDG_0000000026", "Maternal mortality ratio", "per_100k"),
    ("MORTADO", "Adolescent mortality rate", "per_1000"),
    ("CHILDMORT5TO14", "Child mortality 5-14", "per_1000"),
    ("WHOSIS_000015", "Stillbirth rate", "per_1000"),
    ("WHOSIS_000032", "Perinatal mortality rate", "per_1000"),
    ("SDGCAUSEOFDEATH", "Cause-specific mortality (NCD)", "per_100k"),
    ("MORTVIOLENCE", "Mortality from violence", "per_100k"),
    ("MORTROADTRAFFIC", "Road traffic mortality", "per_100k"),
    ("MORTSUICIDE", "Suicide mortality", "per_100k"),
    # NCD risk factors
    ("NCD_BMI_MEAN", "Mean BMI", "kg/m2"),
    ("NCD_BMI_PREVALENCE", "BMI prevalence", "percent"),
    ("NCD_GLUCOSE_MEAN", "Mean fasting blood glucose", "mmol/L"),
    ("NCD_CHOL_MEAN", "Mean total cholesterol", "mmol/L"),
    ("NCD_HYP_DIAGNOSIS_A", "Hypertension diagnosis coverage", "percent"),
    ("NCD_BMI_30", "Obesity prevalence", "percent"),
    ("NCD_TOBACCO_CURRENT", "Current tobacco use", "percent"),
    ("NCD_TOBACCO_DAILY", "Daily tobacco use", "percent"),
    ("NCD_ALCOHOL_CONSUMPTION", "Alcohol consumption per capita", "litres"),
    ("NCD_PHYSICAL_ACTIVITY", "Insufficient physical activity", "percent"),
    ("NCD_SALT_INTAKE", "Mean salt intake", "g/day"),
    # Reproductive / maternal health
    ("MDG_0000000025", "Births attended by skilled health personnel", "percent"),
    ("MDG_0000000030", "Contraceptive prevalence", "percent"),
    ("MDG_0000000035", "Adolescent birth rate", "per_1000"),
    ("MDG_0000000038", "Antenatal care coverage (4+ visits)", "percent"),
    ("MDG_0000000039", "Unmet need for family planning", "percent"),
    ("SDGDEMANDFP", "Demand for family planning satisfied", "percent"),
    # Immunization
    ("WHS4_543", "DTP3 immunization coverage", "percent"),
    ("WHS4_544", "Measles immunization coverage", "percent"),
    ("WHS4_545", "Polio immunization coverage", "percent"),
    ("WHS4_546", "HepB3 immunization coverage", "percent"),
    ("IMM_DTP3", "DTP3 coverage (admin)", "percent"),
    ("IMM_MCV1", "MCV1 coverage", "percent"),
    ("IMM_MCV2", "MCV2 coverage", "percent"),
    ("IMM_PNEUMO", "Pneumococcal conjugate vaccine", "percent"),
    ("IMM_ROTA", "Rotavirus vaccine", "percent"),
    ("IMM_HPV", "HPV vaccine coverage", "percent"),
    ("IMM_BCG", "BCG coverage", "percent"),
    ("IMM_POLIO", "Polio coverage (admin)", "percent"),
    # Nutrition
    ("NUTRITION_LOW_BIRTH_WEIGHT", "Low birth-weight newborns", "percent"),
    ("NUTRITION_WASTING", "Wasting prevalence (under-5)", "percent"),
    ("NUTRITION_STUNTING", "Stunting prevalence (under-5)", "percent"),
    ("NUTRITION_OVERWEIGHT", "Overweight prevalence (under-5)", "percent"),
    ("NUTRITION_BREASTFEEDING", "Exclusive breastfeeding (0-5 months)", "percent"),
    ("NUTRITION_ANEMIA_CHILD", "Anaemia prevalence (under-5)", "percent"),
    ("NUTRITION_ANEMIA_WOMEN", "Anaemia prevalence (women 15-49)", "percent"),
    ("NUTRITION_ANEMIA", "Anaemia prevalence", "percent"),
    ("NUTRITION_THINNESS", "Thinness prevalence (under-5)", "percent"),
    ("NUTRITION_UNDERWEIGHT", "Underweight prevalence (under-5)", "percent"),
    # WASH
    ("WSH_BASIC_WATER", "Basic drinking water coverage", "percent"),
    ("WSH_BASIC_SANITATION", "Basic sanitation coverage", "percent"),
    ("WSH_BASIC_HANDWASHING", "Basic handwashing facilities", "percent"),
    ("WSH_SAFE_MANAGED_WATER", "Safely managed drinking water", "percent"),
    ("WSH_SAFE_MANAGED_SANITATION", "Safely managed sanitation", "percent"),
    ("WSH_OPEN_DEFECATION", "Open defecation prevalence", "percent"),
    # UHC
    ("UHC_COVERAGE_INDEX", "UHC service coverage index", "index"),
    ("UHC_REPRODUCTIVE", "UHC reproductive health", "index"),
    ("UHC_MATERNAL_CHILD", "UHC maternal/child health", "index"),
    ("UHC_INFECTIOUS", "UHC infectious disease", "index"),
    ("UHC_NCD", "UHC NCD treatment", "index"),
    ("UHC_SERVICE_CAPACITY", "UHC service capacity", "index"),
    # HIV / TB / Malaria
    ("HIV_INCIDENCE", "HIV incidence rate", "per_1000"),
    ("HIV_PREVALENCE", "HIV prevalence (15-49)", "percent"),
    ("HIV_ART_COVERAGE", "HIV ART coverage", "percent"),
    ("HIV_MOTHER_CHILD", "PMTCT coverage", "percent"),
    ("HIV_MORTALITY", "HIV mortality", "per_100k"),
    ("TB_INCIDENCE", "TB incidence rate", "per_100k"),
    ("TB_MORTALITY", "TB mortality (HIV-negative)", "per_100k"),
    ("TB_TREATMENT_COVERAGE", "TB treatment coverage", "percent"),
    ("TB_TREATMENT_SUCCESS", "TB treatment success rate", "percent"),
    ("MALARIA_INCIDENCE", "Malaria incidence rate", "per_1000"),
    ("MALARIA_MORTALITY", "Malaria mortality rate", "per_100k"),
    ("MALARIA_CHILD_MORTALITY", "Malaria under-5 mortality", "per_100k"),
    ("MALARIA_ITN_COVERAGE", "Insecticide-treated nets coverage", "percent"),
    ("MALARIA_ACT_TREATMENT", "Malaria ACT treatment coverage", "percent"),
    # Health systems
    ("WHS6_102", "Hospital beds", "per_10k"),
    ("HWF_0006", "Nursing/midwifery personnel", "per_10k"),
    ("HWF_0024", "Community health workers", "number"),
    ("HWF_0001", "Physicians density", "per_10k"),
    ("HWF_0003", "Dentists density", "per_10k"),
    ("HWF_0008", "Pharmacists density", "per_10k"),
    ("HWF_0015", "Psychiatrists density", "per_10k"),
    # Health expenditure
    ("GHED_CHEGDP_SHA2011", "Current health expenditure (% GDP)", "percent"),
    ("GHED_GGHE-DGDP_SHA2011", "Govt health expenditure (% GDP)", "percent"),
    ("GHED_OOPSCHE_SHA2011", "Out-of-pocket health expenditure (% CHE)", "percent"),
    ("GHED_EXTCHE_SHA2011", "External health expenditure (% CHE)", "percent"),
    ("GHED_CHE_pc_US_SHA2011", "Health expenditure per capita", "USD"),
    ("GHED_GGHE_PC_US_SHA2011", "Govt health expenditure per capita", "USD"),
    ("GHED_PRIVATE_PC_US_SHA2011", "Private health expenditure per capita", "USD"),
]

def fetch_who(db):
    cur = db.execute("SELECT location_id FROM locations WHERE admin_level=0")
    row = cur.fetchone()
    if not row:
        print("  WHO: no national location found")
        return
    loc_id = row[0]

    inserted = 0
    for code, ind_name, unit in INDICATORS:
        q = "$filter=SpatialDim eq 'HTI'&$format=json".replace(" ", "%20")
        url = f"{BASE}/{code}?{q}"
        try:
            resp = urllib.request.urlopen(url, timeout=15)
            data = json.loads(resp.read())
        except:
            continue

        for obs in data.get("value", []):
            val = obs.get("NumericValue")
            if val is None:
                continue
            yr = obs.get("TimeDim")
            if not yr:
                continue
            period_id = db.execute(
                "SELECT period_id FROM time_periods WHERE year=?",
                (int(yr),)
            ).fetchone()
            if not period_id:
                db.execute("INSERT OR IGNORE INTO time_periods (period_type, year) VALUES ('year', ?)", (int(yr),))
                period_id = db.execute(
                    "SELECT period_id FROM time_periods WHERE year=?",
                    (int(yr),)
                ).fetchone()
            pid = period_id[0]

            disag = obs.get("Dim1", "") or obs.get("Dim2", "") or obs.get("Dim3", "")
            if disag == "SEX_BTSX" or disag == "":
                disag = "both"

            db.execute("""INSERT OR IGNORE INTO social_institutional_data
                (location_id, period_id, domain, indicator, value, unit, disaggregation, source)
                VALUES (?,?,?,?,?,?,?,?)""",
                (loc_id, pid, "health", ind_name, val, unit, disag, "WHO GHO"))
            inserted += 1

    db.commit()
    print(f"  WHO GHO: {inserted} health indicator rows inserted")

if __name__ == "__main__":
    from config import DB_PATH
    db = sqlite3.connect(DB_PATH)
    fetch_who(db)
    db.close()
