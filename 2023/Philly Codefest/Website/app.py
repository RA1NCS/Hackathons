# import necessary libraries
import openai  # for accessing the OpenAI API
import pyttsx3  # for text-to-speech conversion
import speech_recognition as sr  # for speech recognition
import flask

# initialize Flask app
app = flask.Flask(__name__)

# initialize text-to-speech engine with a female voice
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)  # Use the ID of the desired female voice
engine.say("Hi, I'm Ava, how may I help you?")
engine.runAndWait()

# set up OpenAI API credentials
openai.api_key = "sk-"  # OPENAPI Token

# initialize speech recognizer
listener = sr.Recognizer()


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route("/input", methods=["POST"])
def listen_to_audio():
    """
    Uses the microphone to listen for audio input and returns the recognized text.
    """
    try:
        with sr.Microphone() as source:
            print("--------------------------")
            print("Waiting for you to talk :)")
            voice = listener.listen(source)
            result = listener.recognize_google(voice)
            print(f"You said: {result}\n")
            return result
    except sr.UnknownValueError:
        print("Sorry, I did not understand what you said.")
        return None
    except sr.RequestError as e:
        print("Sorry, my speech service is not available at the moment.")
        return None


@app.route("/output")
def process_text():
    """
    Sends the given prompt to the OpenAI API to generate a response, and returns the generated text.
    """
    prompt = flask.request.args.get("prompt", "")
    if prompt:
        # generate text using DaVinci's API
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=400,
            n=1,
            stop=None,
            temperature=0.5,
        )

        # extract text from API response
        text = response.choices[0].text.strip()

        # check if output is Python code
        if "def" in text or "class" in text or "import" in text or "except" in text:
            # print code with indentation
            code_lines = text.split("\n")
            indented_code = "\n".join(["    " + line for line in code_lines])
            print("------------C O D E-----------")
            print(indented_code + "\n")
            print("----------EXPLANATION---------")
            new_prompt = (
                "Explain the following code as precisely as you can, without using actual code functions, and explain it to a lay man:\n"
                + text
            )
            print(new_prompt)
            text = process_text(new_prompt)

        return text
    else:
        return "No prompt provided."


if __name__ == "__main__":
    app.run(debug=True)
