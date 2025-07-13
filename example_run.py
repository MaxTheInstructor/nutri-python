from nutri_calc import load_data, check_requirements

products, reqs = load_data()
check_requirements(products, reqs)