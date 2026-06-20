import logging
import json
from deep_translator import GoogleTranslator

logger = logging.getLogger(__name__)

# Map standard language codes to AI4Bharat IndicTrans2 language codes
INDIC_LANG_MAP = {
    "hi": "hin_Deva",  # Hindi
    "bn": "ben_Beng",  # Bengali
    "mr": "mar_Deva",  # Marathi
    "ta": "tam_Taml",  # Tamil
    "te": "tel_Telu",  # Telugu
    "gu": "guj_Gujr",  # Gujarati
    "kn": "kan_Knda",  # Kannada
    "or": "ory_Orya",  # Odia
    "ml": "mal_Mlym",  # Malayalam
    "pa": "pan_Guru",  # Punjabi
    "ur": "urd_Arab",  # Urdu
    "as": "asm_Beng",  # Assamese
}


class TranslationService:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.tried_loading = False

    def _load_indictrans2(self):
        if self.tried_loading:
            return
        self.tried_loading = True
        try:
            import torch
            from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
            logger.info("Attempting to load IndicTrans2 model 'ai4bharat/indictrans2-en-indic-dist-200m'...")
            
            # Use small distilled model to run fast on CPU/GPU
            model_name = "ai4bharat/indictrans2-en-indic-dist-200m"
            self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name, trust_remote_code=True)
            
            if torch.cuda.is_available():
                self.model = self.model.cuda()
            logger.info("IndicTrans2 model loaded successfully!")
        except Exception as e:
            logger.warning("Could not load IndicTrans2 model locally: %s. Using GoogleTranslator fallback.", e)
            self.model = None
            self.tokenizer = None

    def translate(self, text: str, target_lang: str) -> str:
        if not text or not text.strip():
            return ""
        
        lang_code = target_lang.lower().strip()
        indic_code = INDIC_LANG_MAP.get(lang_code, lang_code)
        
        # Attempt IndicTrans2 local model
        try:
            self._load_indictrans2()
            if self.model and self.tokenizer:
                import torch
                # Standard IndicTrans2 format: translate to <lang>: <text>
                input_text = f"translate to {indic_code}: {text}"
                inputs = self.tokenizer(input_text, return_tensors="pt", padding=True, truncation=True, max_length=512)
                
                device = self.model.device
                inputs = {k: v.to(device) for k, v in inputs.items()}
                
                with torch.no_grad():
                    generated_tokens = self.model.generate(
                        **inputs,
                        max_length=512,
                        num_beams=4,
                        length_penalty=1.0,
                        early_stopping=True
                    )
                
                translations = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
                if translations:
                    logger.info("Translated text using IndicTrans2 model.")
                    return translations[0].strip()
        except Exception as e:
            logger.warning("IndicTrans2 translation failed: %s. Falling back to GoogleTranslator.", e)
            
        # Fallback to GoogleTranslator (via deep-translator)
        try:
            # Map standard codes for GoogleTranslator (hin_Deva -> hi, etc.)
            google_lang = lang_code
            for k, v in INDIC_LANG_MAP.items():
                if v == lang_code:
                    google_lang = k
                    break
            
            logger.info("Translating text to '%s' using GoogleTranslator fallback...", google_lang)
            translator = GoogleTranslator(source='en', target=google_lang)
            translated = translator.translate(text)
            return translated
        except Exception as e:
            logger.error("Fallback translation failed: %s", e)
            return f"[Translation Offline] {text}"
