import torch
from vllm import LLM, SamplingParams

class HuggingFaceModel():
    def __init__(self, args):
        pass

    def generate(self, processed_prompts): 
        pass




import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

class HuggingFaceModel():
    def __init__(self, args):
        # Load the tokenizer and the model
        self.tokenizer = AutoTokenizer.from_pretrained(args.model_dir, trust_remote_code=args.trust_remote_code)
        self.model = AutoModelForCausalLM.from_pretrained(args.model_dir, torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32, trust_remote_code=args.trust_remote_code)

        # Check if the tokenizer has a pad_token, otherwise set it to eos_token
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        # Move the model to GPU if available
        if torch.cuda.is_available():
            self.model = self.model.cuda()

        # Setup the generation configuration
        self.generation_config = GenerationConfig(
            temperature=args.temperature,
            top_p=args.top_p,
            max_new_tokens=args.max_tokens,
            repetition_penalty=args.presence_penalty,
            frequency_penalty=args.frequency_penalty
        )
        print(">>>>>> Hugging Face model loaded")

    def generate(self, processed_prompts):
        # Tokenize the input prompts
        inputs = self.tokenizer(processed_prompts, return_tensors='pt', padding=True, truncation=True)
        
        # Move inputs to GPU if available
        if torch.cuda.is_available():
            inputs = {k: v.cuda() for k, v in inputs.items()}

        # Generate output using the model
        outputs = self.model.generate(**inputs, **self.generation_config.__dict__)

        # Decode the output into text
        decoded_outputs = [self.tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
        print(">>>>>> generation done")

        return decoded_outputs


# checkpoint = "mistralai/Mathstral-7b-v0.1"
# tokenizer = AutoTokenizer.from_pretrained(checkpoint)
# model = AutoModelForCausalLM.from_pretrained(checkpoint, device_map="auto", torch_dtype=torch.bfloat16)

# prompt = [{"role": "user", "content": "What are the roots of unity?"}]
# tokenized_prompt = tokenizer.apply_chat_template(prompt, add_generation_prompt=True, return_dict=True, return_tensors="pt").to(model.device)

# out = model.generate(**tokenized_prompt, max_new_tokens=512)
# tokenizer.decode(out[0])
# >>> '<s>[INST] What are the roots of unity?[/INST] The roots of unity are the complex numbers that satisfy the equation $z^n = 1$, where $n$ is a positive integer. These roots are evenly spaced around the unit circle in the complex plane, and they have a variety of interesting properties and applications in mathematics and physics.</s>'
