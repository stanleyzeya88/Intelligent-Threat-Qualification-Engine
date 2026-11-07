import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


class BriefWriter:
    def __init__(self, model_dir: str = 'models/fine_tuned_distilgpt2_security'):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
            self.model = AutoModelForCausalLM.from_pretrained(model_dir).to(self.device)
            self.model.eval()
            print(f"✅ P5 Model loaded from {model_dir} on {self.device.type.upper()}")
        except Exception as e:
            print(f"⚠️ Could not load P5 model: {e}. Using stub generator.")
            self.model = None

    def generate_brief(self, telemetry_dict: dict) -> str:
        display_attack = telemetry_dict.get('label', 'Unknown')
        prompt = (
            f"[TELEMETRY PROMPT] Protocol: {str(telemetry_dict['protocol_type']).upper()} | "
            f"Service: {str(telemetry_dict['service']).upper()} | "
            f"Attack: {display_attack} | "
            f"Category: {telemetry_dict.get('Category', 'Unknown')} | "
            f"Severity: {telemetry_dict.get('severity', 'High')} | "
            f"Serror: {float(telemetry_dict['serror_rate']):.2f} | "
            f"Rerror: {float(telemetry_dict['rerror_rate']):.2f} | "
            f"Flag: {telemetry_dict['flag']} | "
            f"SrcBytes: {int(float(telemetry_dict['src_bytes']))} | "
            f"DstBytes: {int(float(telemetry_dict['dst_bytes']))}\n"
            f"[INCIDENT REPORT]\n"
        )

        if self.model:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs, max_new_tokens=90, do_sample=False,
                    repetition_penalty=1.3, 
                    pad_token_id=self.tokenizer.eos_token_id,
                )
            full_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return full_text[len(prompt):].strip()
        else:
            return (f"CRITICAL SECURITY ALERT: A "
                    f"{telemetry_dict.get('severity', 'High')}-severity event "
                    f"({display_attack}) was detected. "
                    f"Recommended Action: Investigate immediately.")
