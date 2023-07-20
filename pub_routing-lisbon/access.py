from andyamo import types


def is_accessible(feature, profile: types.Profile):
    feature_type = feature["feature"]["properties"]["type"]
    feature_attributes = feature["attr"]

    # |-------------- foot / crosswalk, sidewalk, stairs
    if profile.value == "foot":
        return True

    elif profile.value == "manual_wheelchair":

        # |-------------- manual_wheelchair / crosswalk
        if feature_type == "passage_pieton":
            predicates = [
                feature_attributes["Hauteur"] == "Non abaissé",
                feature_attributes["Marquage"] == "Non"
                and feature_attributes["Feu tricolore"] == "Non",
                feature_attributes["Feu tricolore"] == "Non"
                and feature_attributes["Croisement"]
                == "Piste cyclable bidirectionnelle",
            ]
            not_accessible = sum(predicates) > 0
            if not_accessible:
                return False

        # |-------------- manual_wheelchair / sidewalk
        elif feature_type == "segment":

            predicates = [
                feature_attributes["Largeur"] == "Passe pas",
                feature_attributes["Largeur"] == "Passe seul"
                and feature_attributes["Obstacle"] == "Oui qui bloque le passage",
                feature_attributes["Type de revêtement"] == "Impraticable",
                feature_attributes["Type de revêtement"] == "Carrossable",
                feature_attributes["Etat"] == "Très abimé",
                feature_attributes["Inclinaison"] == "Très pentu",
                feature_attributes["Dévers"] == "Très pentu",
                feature_attributes["A vérifier"] == "En travaux",
            ]
            not_accessible = sum(predicates) > 0
            if not_accessible:
                return False

        # |-------------- manual_wheelchair / stairs
        elif feature_type == "escalier":
            return False

        # |-------------- manual_wheelchair / catch all
        else:
            raise Exception(f"Unknown feature: {feature_type}")

        return True

    elif profile.value == "electric_wheelchair":

        # |-------------- electric_wheelchair / crosswalk
        if feature_type == "passage_pieton":
            predicates = [
                feature_attributes["Hauteur"] == "Non abaissé",
                feature_attributes["Marquage"] == "Non"
                and feature_attributes["Feu tricolore"] == "Non",
                feature_attributes["Feu tricolore"] == "Non"
                and feature_attributes["Croisement"]
                == "Piste cyclable bidirectionnelle",
            ]
            not_accessible = sum(predicates) > 0
            if not_accessible:
                return False

        # |-------------- electric_wheelchair / sidewalk
        elif feature_type == "segment":

            predicates = [
                feature_attributes["Largeur"] == "Passe pas",
                feature_attributes["Largeur"] == "Passe seul"
                and feature_attributes["Obstacle"] == "Oui qui bloque le passage",
                feature_attributes["Type de revêtement"] == "Impraticable",
                feature_attributes["Etat"] == "Très abimé",
                feature_attributes["Inclinaison"] == "Très pentu",
                feature_attributes["Dévers"] == "Très pentu",
                feature_attributes["A vérifier"] == "En travaux",
            ]
            not_accessible = sum(predicates) > 0
            if not_accessible:
                return False

        # |-------------- electric_wheelchair / stairs
        elif feature_type == "escalier":
            return False

        # |-------------- electric_wheelchair / catch all
        else:
            raise Exception(f"Unknown feature: {feature_type}")

        return True
