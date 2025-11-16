import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import warnings
import os
warnings.filterwarnings('ignore')


class ResNetFeatureExtractor(nn.Module):
    def __init__(self):
        super(ResNetFeatureExtractor, self).__init__()
        resnet = models.resnet50(pretrained=True)
        self.features = nn.Sequential(*list(resnet.children())[:-1])
        self.features.eval()
    
    def forward(self, x):
        with torch.no_grad():
            features = self.features(x)
            features = features.view(features.size(0), -1)
        return features


class VGGFeatureExtractor(nn.Module):
    def __init__(self):
        super(VGGFeatureExtractor, self).__init__()
        vgg = models.vgg16(pretrained=True)
        self.features = vgg.features
        self.avgpool = vgg.avgpool
        self.classifier = nn.Sequential(*list(vgg.classifier.children())[:-1])
        self.features.eval()
        self.classifier.eval()
    
    def forward(self, x):
        with torch.no_grad():
            x = self.features(x)
            x = self.avgpool(x)
            x = torch.flatten(x, 1)
            x = self.classifier(x)
        return x


class RNNDecoder(nn.Module):
    def __init__(self, embed_size, hidden_size, vocab_size, num_layers=1):
        super(RNNDecoder, self).__init__()
        self.embed = nn.Embedding(vocab_size, embed_size)
        self.lstm = nn.LSTM(embed_size, hidden_size, num_layers, batch_first=True)
        self.linear = nn.Linear(hidden_size, vocab_size)
        self.hidden_size = hidden_size
    
    def forward(self, features, captions):
        embeddings = self.embed(captions)
        embeddings = torch.cat((features.unsqueeze(1), embeddings), 1)
        hiddens, _ = self.lstm(embeddings)
        outputs = self.linear(hiddens)
        return outputs


class ImageCaptioner:
    def __init__(self, model_type='blip'):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model_type = model_type
        
        if model_type == 'blip':
            self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
            self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
            self.model.to(self.device)
            self.model.eval()
            
        elif model_type == 'vit-gpt2':
            self.model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
            self.feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
            self.tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
            self.model.to(self.device)
            self.model.eval()
            
        elif model_type == 'resnet-rnn':
            self.encoder = ResNetFeatureExtractor().to(self.device)
            self.transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])
            self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
            self.decoder = GPT2LMHeadModel.from_pretrained('gpt2').to(self.device)
            self.decoder.eval()
            
        elif model_type == 'vgg-rnn':
            self.encoder = VGGFeatureExtractor().to(self.device)
            self.transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])
            self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
            self.decoder = GPT2LMHeadModel.from_pretrained('gpt2').to(self.device)
            self.decoder.eval()
    
    def generate_caption(self, image_path, max_length=50, num_beams=4):
        image = Image.open(image_path).convert('RGB')
        
        if self.model_type == 'blip':
            inputs = self.processor(image, return_tensors="pt").to(self.device)
            outputs = self.model.generate(**inputs, max_length=max_length, num_beams=num_beams, early_stopping=True)
            caption = self.processor.decode(outputs[0], skip_special_tokens=True)
            
        elif self.model_type == 'vit-gpt2':
            pixel_values = self.feature_extractor(images=image, return_tensors="pt").pixel_values
            pixel_values = pixel_values.to(self.device)
            output_ids = self.model.generate(pixel_values, max_length=max_length, num_beams=num_beams, early_stopping=True)
            caption = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
            
        elif self.model_type in ['resnet-rnn', 'vgg-rnn']:
            img_tensor = self.transform(image).unsqueeze(0).to(self.device)
            features = self.encoder(img_tensor)
            
            prompt = "This image shows"
            input_ids = self.tokenizer.encode(prompt, return_tensors='pt').to(self.device)
            
            with torch.no_grad():
                output = self.decoder.generate(
                    input_ids,
                    max_length=max_length,
                    num_beams=num_beams,
                    early_stopping=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            caption = self.tokenizer.decode(output[0], skip_special_tokens=True)
        
        return caption
    
    def generate_multiple_captions(self, image_path, num_captions=3):
        image = Image.open(image_path).convert('RGB')
        captions = []
        
        if self.model_type == 'blip':
            inputs = self.processor(image, return_tensors="pt").to(self.device)
            outputs = self.model.generate(**inputs, max_length=50, num_beams=num_captions, 
                                         num_return_sequences=num_captions, early_stopping=True)
            for output in outputs:
                caption = self.processor.decode(output, skip_special_tokens=True)
                captions.append(caption)
        
        elif self.model_type == 'vit-gpt2':
            pixel_values = self.feature_extractor(images=image, return_tensors="pt").pixel_values
            pixel_values = pixel_values.to(self.device)
            output_ids = self.model.generate(pixel_values, max_length=50, num_beams=num_captions, 
                                            num_return_sequences=num_captions, early_stopping=True)
            for output in output_ids:
                caption = self.tokenizer.decode(output, skip_special_tokens=True)
                captions.append(caption)
        
        elif self.model_type in ['resnet-rnn', 'vgg-rnn']:
            img_tensor = self.transform(image).unsqueeze(0).to(self.device)
            features = self.encoder(img_tensor)
            
            for _ in range(num_captions):
                prompt = "This image shows"
                input_ids = self.tokenizer.encode(prompt, return_tensors='pt').to(self.device)
                
                with torch.no_grad():
                    output = self.decoder.generate(
                        input_ids,
                        max_length=50,
                        num_beams=4,
                        do_sample=True,
                        temperature=0.7,
                        pad_token_id=self.tokenizer.eos_token_id
                    )
                
                caption = self.tokenizer.decode(output[0], skip_special_tokens=True)
                captions.append(caption)
        
        return captions
    
    def conditional_caption(self, image_path, text_prompt):
        if self.model_type != 'blip':
            return "Conditional captioning only supported with BLIP model"
        
        image = Image.open(image_path).convert('RGB')
        inputs = self.processor(image, text_prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(**inputs, max_length=50)
        caption = self.processor.decode(outputs[0], skip_special_tokens=True)
        
        return caption


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python image_captioning.py <image_path> [model_type]")
        print("Model types: blip, vit-gpt2, resnet-rnn, vgg-rnn")
        sys.exit(1)
    
    image_path = sys.argv[1]
    model_type = sys.argv[2] if len(sys.argv) > 2 else 'blip'
    
    if not os.path.exists(image_path):
        print(f"Error: Image not found: {image_path}")
        sys.exit(1)
    
    print(f"Loading {model_type.upper()} model...")
    captioner = ImageCaptioner(model_type=model_type)
    
    print(f"Generating caption for: {image_path}")
    caption = captioner.generate_caption(image_path)
    
    print(f"\nCaption: {caption}")
    
    print("\nGenerating multiple captions...")
    captions = captioner.generate_multiple_captions(image_path, num_captions=3)
    for i, cap in enumerate(captions, 1):
        print(f"{i}. {cap}")


if __name__ == "__main__":
    main()
