#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🚀 IoT Predictive Maintenance Dashboard - Setup${NC}"
echo "=================================================="

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo -e "${GREEN}Project directory: $SCRIPT_DIR${NC}"

# Change to project directory
cd "$SCRIPT_DIR" || exit 1

# Create virtual environment
echo -e "\n${YELLOW}1️⃣ Creating virtual environment...${NC}"
python3 -m venv venv

# Activate virtual environment
echo -e "${YELLOW}2️⃣ Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "${YELLOW}3️⃣ Upgrading pip...${NC}"
pip install --upgrade pip setuptools wheel

# Install requirements
echo -e "${YELLOW}4️⃣ Installing dependencies from requirements.txt...${NC}"
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠️ requirements.txt not found!${NC}"
    exit 1
fi

# Run setup.py
echo -e "${YELLOW}5️⃣ Initializing project structure...${NC}"
python setup.py

echo -e "\n${GREEN}✅ Setup complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Activate environment: source venv/bin/activate"
echo "2. Run app: streamlit run app.py"
echo ""
