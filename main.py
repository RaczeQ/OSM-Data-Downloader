from src.relation import load_area

for city in ["Wrocław, PL"]:
    relation = load_area(city)
    relation.load_relations()