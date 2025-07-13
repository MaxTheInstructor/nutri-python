import json

def load_data():
    with open('data/products.json', encoding='utf-8') as f:
        products = json.load(f)
    with open('data/requirements.json', encoding='utf-8') as f:
        requirements = json.load(f)
    return products, requirements

def check_requirements(products, reqs):
    print("Требования:", reqs)
    print("Продукты:")
    for p in products:
        print(f"- {p['name']}: {p['protein']}г белка, {p['fat']}г жиров, {p['carbs']}г углеводов, {p['kcal']} ккал")

if __name__ == "__main__":
    products, reqs = load_data()
    check_requirements(products, reqs)
