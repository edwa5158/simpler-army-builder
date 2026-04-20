from warscroll import load_warscrolls

def list_warscrolls():
    warscrolls = load_warscrolls()
    result = []
    for k, ws in warscrolls:
        result.append(f"{k}: ws")
    
def create_unit(warscroll: dict) -> dict:

    return {"warscroll": warscroll, "other_stuff": "tbd"}

