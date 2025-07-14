import json
import random  # нужно для выбора случайного продукта

def compute_totals(ration):
            totals = {"calories": 0, "protein": 0, "fat": 0, "carbs": 0}
            for item in ration:
                factor = item["grams"] / 100
                totals["calories"] += item["nutrients"]["calories"] * factor
                totals["protein"]  += item["nutrients"]["protein"]  * factor
                totals["fat"]      += item["nutrients"]["fat"]      * factor
                totals["carbs"]    += item["nutrients"]["carbs"]    * factor
            return totals

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
        n = p["nutrients"]
        print(f"- {p['name']}: {n['protein']}г белка, {n['fat']}г жиров, {n['carbs']}г углеводов, {n['calories']} ккал")

def classify_products(products):
    classified = []
    for p in products:
        n = p["nutrients"]
        total = n["protein"] * 4 + n["fat"] * 9 + n["carbs"] * 4
        if total == 0:
            total = 1  # чтобы избежать деления на ноль
        classified.append({
            "name": p["name"],
            "nutrients": p["nutrients"],
            "grams": 100,
            "protein_share": n["protein"] * 4 / total,
            "fat_share":     n["fat"] * 9 / total,
            "carbs_share":   n["carbs"] * 4 / total,
            "calories_share": 1.0  # добавляем всегда 1 для калорий
        })
    return classified

def optimize_daily_ration(products, requirements):
    # Ограничения массы продуктов в граммах
    limits = {
        "Куриная грудка": 400,
        "Овсяные хлопья": 150,
        "Яйцо куриное": 150,
        "Лосось": 200,
        "Масло растительное": 50,
        "Масло сливочное": 50,
        "Хлеб пшеничный": 200,
        "Картофель отварной": 400,
        "Йогурт (3.2% жирности)": 300,
        "Огурцы": 300,
        "Помидоры": 300,
        "Яблоки": 300
    }

    # Шаг 1: Классификация продуктов + стартовый рацион по 100 г
    ration = []
    for p in products:
        grams = min(100, limits.get(p["name"], 300))  # не больше лимита даже на старте
        n = p["nutrients"]
        ratio = (n["protein"] * 4 + n["fat"] * 9 + n["carbs"] * 4) / n["calories"] if n["calories"] else 0
        ration.append({
            "name": p["name"],
            "nutrients": n,
            "grams": grams,
            "protein_share": (n["protein"] * 4) / n["calories"] if n["calories"] else 0,
            "fat_share":     (n["fat"] * 9) / n["calories"] if n["calories"] else 0,
            "carbs_share":   (n["carbs"] * 4) / n["calories"] if n["calories"] else 0
        })

    totals = compute_totals(ration)

    for _ in range(300):  # максимум 300 итераций
        adjusted = False

        for nutrient in ["calories", "protein", "fat", "carbs"]:
            if totals[nutrient] < requirements[nutrient] * 0.99:
                # Увеличиваем продукт с наибольшей долей нужного нутриента и не превышающий лимит
                candidates = sorted(
                    [x for x in ration if x["grams"] < limits.get(x["name"], 300)],
                    key=lambda x: x[f"{nutrient}_share"] if nutrient != "calories" else 1,
                    reverse=True
                )
                if candidates:
                    candidates[0]["grams"] += 10
                    adjusted = True

            elif totals[nutrient] > requirements[nutrient] * 1.01:
                # Уменьшаем продукт с наибольшей долей этого нутриента и массой > 20 г
                candidates = sorted(
                    [x for x in ration if x["grams"] > 20],
                    key=lambda x: x[f"{nutrient}_share"] if nutrient != "calories" else 1,
                    reverse=True
                )
                if candidates:
                    candidates[0]["grams"] -= 10
                    adjusted = True

        totals = compute_totals(ration)
        if not adjusted:
            break

    # Вывод результата
    print("\nОптимизированный рацион (масса в граммах):")
    for item in ration:
        print(f"- {item['name']}: {item['grams']} г")

    print("\nИтого по рациону:")
    print(f"Калории: {totals['calories']:.1f} / {requirements['calories']} ккал")
    print(f"Белки:   {totals['protein']:.1f} / {requirements['protein']} г")
    print(f"Жиры:    {totals['fat']:.1f} / {requirements['fat']} г")
    print(f"Углеводы:{totals['carbs']:.1f} / {requirements['carbs']} г")