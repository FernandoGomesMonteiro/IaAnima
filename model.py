from transformers import pipeline

# Carregar o pipeline de detecção de linguagem usando XLM-RoBERTa-base
language_detector = pipeline("text-classification", model="papluca/xlm-roberta-base-language-detection")

# Função para detectar a linguagem de um texto
def detect_language(text):
    """
    Detecta a linguagem do texto usando o modelo XLM-RoBERTa-base.

    Args:
        text (str): Texto a ser analisado.

    Returns:
        str: Código do idioma detectado.
    """
    result = language_detector(text)
    language = result[0]['label']
    score = result[0]['score']
    return f"Linguagem: {language}, Confiança: {score:.2f}"

# Exemplo de uso
texto_exemplo = "Eu estou muito ansioso e não consigo me concentrar."
detected_language = detect_language(texto_exemplo)
print(detected_language)