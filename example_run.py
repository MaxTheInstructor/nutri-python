from nutri_calc import load_data, check_requirements, optimize_daily_ration

products, reqs = load_data()
check_requirements(products, reqs)

print("\nОптимизация рациона...")
optimize_daily_ration(products, reqs)