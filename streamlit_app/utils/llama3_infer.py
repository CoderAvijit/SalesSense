# utils/llama3_infer.py
import os
import together

together.api_key = os.getenv("TOGETHER_API_KEY")

def query_llama3(prompt, system_prompt):
    try:
        response = together.Complete.create(
            prompt=f"<|begin_of_text|><|system|>\n{system_prompt}\n<|user|>\n{prompt}<|assistant|>",
            model="meta-llama/Llama-3-70b-chat-hf",
            max_tokens=1024,
            temperature=0.7,
            top_p=0.9,
            stop=["<|user|>"]
        )
        return response['output']['choices'][0]['text'].strip()
    except Exception as e:
        return f"❌ LLaMA error: {e}"
