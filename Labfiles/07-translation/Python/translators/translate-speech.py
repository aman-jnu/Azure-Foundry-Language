import os
from dotenv import load_dotenv


# Import namespaces
from azure.identity import DefaultAzureCredential
import azure.cognitiveservices.speech as speech_sdk



def main():
    try:

        # Clear the console 
        os.system('cls' if os.name == 'nt' else 'clear')

        # Get Configuration Settings
        load_dotenv()
        foundry_endpoint = os.getenv('FOUNDRY_ENDPOINT')


        # Configure translation
        credential = DefaultAzureCredential()
        translation_cfg = speech_sdk.translation.SpeechTranslationConfig(
                token_credential=credential,
                endpoint=foundry_endpoint
        )
        translation_cfg.speech_recognition_language = 'en-US'
        translation_cfg.add_target_language('fr')
        translation_cfg.add_target_language('es')
        translation_cfg.add_target_language('hi')
        audio_in_cfg = speech_sdk.AudioConfig(use_default_microphone=True)
        translator = speech_sdk.translation.TranslationRecognizer(
            translation_config=translation_cfg,
            audio_config=audio_in_cfg
        )
        print('Ready to translate from',translation_cfg.speech_recognition_language)
        


        # Configure speech for synthesis of translations
        speech_cfg = speech_sdk.SpeechConfig(
            token_credential=credential, endpoint=foundry_endpoint)
        audio_out_cfg = speech_sdk.audio.AudioOutputConfig(use_default_speaker=True)
        voices = {
            "fr": "fr-FR-HenriNeural",
            "es": "es-ES-ElviraNeural",
            "hi": "hi-IN-MadhurNeural"
        }
        print('Ready to use speech service.')
                


        # Translate user speech
        print("Speak now...")
        translation_results = translator.recognize_once_async().get()
        print(f"Translating '{translation_results.text}'")
                
        

        # Print and speak the translation results
        for language in translation_results.translations:
            translation = translation_results.translations[language]
            print(f"'{translation_results.text}' was translated to {language} as '{translation}'")
            speech_cfg.speech_synthesis_voice_name = voices[language]
            synthesizer = speech_sdk.SpeechSynthesizer(speech_config=speech_cfg, audio_config=audio_out_cfg)
            synthesizer.speak_text_async(translation).get()



    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
