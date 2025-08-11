from argparse import ArgumentParser
from Main_OCR import OcrChain

def parse_arguments():
    """Separate function to handle argument parsing"""
    parser = ArgumentParser(description='OCR Processing Tool')
    parser.add_argument(
        "--model",
        type=str,
        default="gemma3:4b-it-q4_K_M",
        help="The model to use for the chat."
    )
    parser.add_argument(
        "--base-url",
        type=str,
        default="http://localhost:11434",
        help="The base URL of the Ollama server."
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="The temperature to use for the chat."
    )
    parser.add_argument(
        "--input-image",
        type=str,
        required=True,
        help="The image to perform OCR on."
    )
    return parser.parse_args()

def main():
    try:
        args = parse_arguments()
        
        # Create OCR chain with argument unpacking for cleaner code
        ocr_chain = OcrChain(**{
            'model': args.model,
            'base_url': args.base_url,
            'temperature': args.temperature
        })
        
        # Process image
        result = ocr_chain.invoke(args.input_image)
        print(f"OCR result: {result}")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())