from transformers import pipeline

# Carregamos um modelo pré-treinado (BERT, por exemplo) e definimos a tarefa de classificação de texto
classifier = pipeline('zero-shot-classification', model="facebook/bart-large-mnli")

# Definimos as possíveis categorias (diagnósticos)
labels = [
    "depression",
    "anxiety",
    "panic disorder",
    "burnout",
    "borderline personality disorder",
    "bipolar disorder"
]

# Função que classifica o texto de entrada nos possíveis diagnósticos
def classify_symptoms(symptom_description):
    result = classifier(symptom_description, labels)
    return result

# Exemplo de uso
if __name__ == "__main__":
    symptom_input = "My emotions change so quickly; one moment I’m fine, and the next, I feel empty or angry for no reason"

    # Classifica o sintoma de acordo com as categorias
    diagnosis = classify_symptoms(symptom_input)

    print("Possible Diagnoses: ", diagnosis['labels'])
    print("Confidence Scores: ", diagnosis['scores'])
