#!/bin/bash
clear
# Màu sắc cho console
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Banner
echo -e "${RED}"
echo "╔════════════════════════════════════════╗" 
echo "║             U16ToolChain               ║"
echo "╚════════════════════════════════════════╝"
echo -e "${NC}"

# Hiển thị danh sách file
echo -e "${BLUE}Available files in 580vnx_ropchain:${NC}"
echo "----------------------------------------"
files=(./580vnx_ropchain/*)
count=1
for file in "${files[@]}"; do
    filename=$(basename "$file")
    echo -e "${GREEN}$count)${NC} $filename"
    ((count++))
done
echo "----------------------------------------"

# Nhập tên file
echo -e "${YELLOW}Enter name: ${NC}"
read name

# Kiểm tra file tồn tại
if [ -f "./580vnx_ropchain/$name" ]; then
    echo -e "${GREEN}Processing $name...${NC}"
    python ./580vnx/compiler_.py -f hex < "./580vnx_ropchain/$name"
else
    echo -e "${RED}Error: File $name not found!${NC}"
fi
