#!/bin/bash
set -e

echo "================================================================================"
echo "Framework + Iteration Protocol Tests"
echo "3 rounds each, mock readers, sequential execution"
echo "================================================================================"

# Activate venv
cd writers && source .venv/bin/activate && cd ..

# Backup existing configs
mkdir -p /tmp/backup_configs
mv writers/config/writer_configs/writer_00*.yaml /tmp/backup_configs/ 2>/dev/null || true

echo ""
echo "TEST 1: Claude 7-Step Framework + Claude Iteration Protocol"
echo "================================================================================"
cp /tmp/backup_configs/writer_00*.yaml writers/config/writer_configs/ 2>/dev/null || true
mv writers/config/writer_configs/writer_claude_test.yaml writers/config/writer_configs/writer_001.yaml
python end_to_end_v0.1.py --mock --llm 1 --rounds 3 --data-dir data/claude_framework_test
mv writers/config/writer_configs/writer_001.yaml writers/config/writer_configs/writer_claude_test.yaml
rm writers/config/writer_configs/writer_00*.yaml 2>/dev/null || true

echo ""
echo "TEST 2: Gemini 2.5 Pro Framework + Gemini Iteration Protocol"
echo "================================================================================"
mv writers/config/writer_configs/writer_gemini_test.yaml writers/config/writer_configs/writer_001.yaml
python end_to_end_v0.1.py --mock --llm 1 --rounds 3 --data-dir data/gemini_framework_test
mv writers/config/writer_configs/writer_001.yaml writers/config/writer_configs/writer_gemini_test.yaml

echo ""
echo "TEST 3: ChatGPT 5.1 Framework + ChatGPT Iteration Protocol"
echo "================================================================================"
mv writers/config/writer_configs/writer_chatgpt_test.yaml writers/config/writer_configs/writer_001.yaml
python end_to_end_v0.1.py --mock --llm 1 --rounds 3 --data-dir data/chatgpt_framework_test
mv writers/config/writer_configs/writer_001.yaml writers/config/writer_configs/writer_chatgpt_test.yaml

# Restore original configs
mv /tmp/backup_configs/writer_00*.yaml writers/config/writer_configs/ 2>/dev/null || true
rmdir /tmp/backup_configs 2>/dev/null || true

echo ""
echo "================================================================================"
echo "All Tests Complete!"
echo "================================================================================"
echo "Data locations:"
echo "  - data/claude_framework_test/"
echo "  - data/gemini_framework_test/"
echo "  - data/chatgpt_framework_test/"
