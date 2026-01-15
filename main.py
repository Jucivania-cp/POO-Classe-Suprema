from src.interface.cli import main
import sys
import os

# Garante que o diretório 'src' seja reconhecido pelo Python para as importações
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

if __name__ == "__main__":
    main()


