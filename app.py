# This code was inspired by https://huggingface.co/nlpconnect/vit-gpt2-image-captioning

import torch
from flask import Flask, request
from PIL import Image
from transformers import AutoTokenizer, VisionEncoderDecoderModel, ViTImageProcessor

app = Flask(__name__)

model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
image_processor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


@app.route("/", methods=["POST"])
def home():
    img = Image.open(request.files["file"])

    pixel_values = image_processor(images=[img], return_tensors="pt").pixel_values
    pixel_values = pixel_values.to(device)

    MAX_LENGTH = 16
    NUM_BEAMS = 4
    gen_kwargs = {"max_length": MAX_LENGTH, "num_beams": NUM_BEAMS}
    output_ids = model.generate(pixel_values, **gen_kwargs)

    preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
    preds = [pred.strip() for pred in preds]
    return preds[0]


if __name__ == "__main__":
    app.run()
