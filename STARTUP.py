import random
import re
import unicodedata

import sounddevice as sd
import speech_recognition as sr


duration = 5
sample_rate = 44100

words_by_level = {
    "facil": ["gato", "perro", "manzana", "leche", "sol"],
    "medio": ["banano", "escuela", "amigo", "ventana", "amarillo"],
    "dificil": ["tecnologia", "universidad", "informacion", "pronunciacion", "imaginacion"]
}

translations_by_word = {
    "gato": "cat",
    "perro": "dog",
    "manzana": "apple",
    "leche": "milk",
    "sol": "sun",
    "banano": "banana",
    "escuela": "school",
    "amigo": "friend",
    "ventana": "window",
    "amarillo": "yellow",
    "tecnologia": "technology",
    "universidad": "university",
    "informacion": "information",
    "pronunciacion": "pronunciation",
    "imaginacion": "imagination",
}


def normalize_answer(text):
    normalized = unicodedata.normalize("NFD", text.casefold())
    without_accents = "".join(
        character for character in normalized
        if unicodedata.category(character) != "Mn"
    )
    return re.sub(r"[^\w\s]", "", without_accents).strip()


def listen_answer():
    print("Habla ahora en inglés; tienes 5 segundos...")
    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16",
    )
    sd.wait()

    audio = sr.AudioData(recording.tobytes(), sample_rate, 2)
    recognizer = sr.Recognizer()
    try:
        return recognizer.recognize_google(audio, language="en-US")
    except sr.UnknownValueError:
        return None


def play_translation_game():
    print("Juego de traducción: español a inglés")
    print("Niveles disponibles:", ", ".join(words_by_level))

    while True:
        level_name = input("Elige un nivel (o escribe q para salir): ").strip().lower()
        if level_name == "q":
            return
        if level_name in words_by_level:
            break
        print("Ese nivel no existe. Elige uno de los niveles disponibles.")

    score = 0
    print("Di la traducción en inglés. Di 'quit' o 'exit' para terminar.")

    while True:
        spanish_word = random.choice(words_by_level[level_name])
        correct_translation = translations_by_word[spanish_word]
        print(f"Traduce '{spanish_word}'.")

        while True:
            try:
                answer = listen_answer()
            except sr.RequestError as error:
                print(f"No se pudo conectar al servicio de reconocimiento: {error}")
                print(f"Puntuación final: {score}")
                return
            except Exception as error:
                print(f"No se pudo grabar o procesar el audio: {error}")
                print(f"Puntuación final: {score}")
                return

            if answer is None:
                print("No se entendió lo que dijiste. Inténtalo de nuevo; no pierdes puntos.")
                continue

            print(f"Reconocí: {answer}")
            if normalize_answer(answer) in {"quit", "exit"}:
                print(f"Juego terminado. Puntuación final: {score}")
                return
            break

        if normalize_answer(answer) == normalize_answer(correct_translation):
            score += 1
            print("¡Correcto! +1 punto")
        else:
            score -= 1
            print(f"Incorrecto. La traducción era '{correct_translation}'. -1 punto")

        print(f"Puntuación: {score}\n")

    print(f"Juego terminado. Puntuación final: {score}")


if __name__ == "__main__":
    play_translation_game()
