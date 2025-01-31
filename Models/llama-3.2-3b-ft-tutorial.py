# !pip install -U -q transformers peft huggingface-hub

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from peft import PeftModel

from huggingface_hub import login

login(token="<Hugging face token>")

base_model_name = "meta-llama/Llama-3.2-3B-Instruct"
adapter_path = "chandrahas316/llama-3.2-3B-Instruct-ft-adapter"

tokenizer = AutoTokenizer.from_pretrained(base_model_name, device_map = "auto")
base_model = AutoModelForCausalLM.from_pretrained(base_model_name, device_map = "auto")

model = PeftModel.from_pretrained(base_model, adapter_path)
model = model.merge_and_unload()

def generate_prompt(license_text):
    instruction = '''Extract all License Terms from the Statement given below in the following JSON format:\njson{ ... }'''
    query = f'''Statement: {license_text}'''
    messages = [
        {"role": "system", "content": instruction},
        {"role": "user", "content": query}
    ]
    row = tokenizer.apply_chat_template(messages, tokenize=False)
    return row

def generate_completion(license_text, max_length=1024, temperature=0.9):
    prompt = generate_prompt(license_text)
    print("prompt - ",prompt)

    input_ids = tokenizer(prompt, return_tensors="pt", add_special_tokens=True).to("cuda")
    outputs = model.generate(
        **input_ids,
        max_new_tokens=max_length,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id,
        temperature=temperature,
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)


license_text = '''Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice (including the next paragraph) shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.'''
output = generate_completion(license_text)
print(output)
