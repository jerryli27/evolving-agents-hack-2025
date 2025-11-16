#!/bin/bash

# Run three end-to-end tests in parallel with different framework combinations
# Each test: 1 writer, 3 rounds, mock readers

echo "================================================================================"
echo "Starting Parallel End-to-End Tests"
echo "================================================================================"
echo ""
echo "Test 1: Claude 7-Step Framework + Claude Iteration Protocol"
echo "Test 2: Gemini 2.5 Pro Framework + Gemini Iteration Protocol"
echo "Test 3: ChatGPT 5.1 Framework + ChatGPT Iteration Protocol"
echo ""
echo "Configuration: 3 rounds, 1 reader (mock), parallel execution"
echo "================================================================================"
echo ""

# Create temporary config directories for each test
mkdir -p /tmp/claude_test_configs
mkdir -p /tmp/gemini_test_configs
mkdir -p /tmp/chatgpt_test_configs

# Copy only the specific writer config to each temp directory
cp writers/config/writer_configs/writer_claude_test.yaml /tmp/claude_test_configs/
cp writers/config/writer_configs/writer_gemini_test.yaml /tmp/gemini_test_configs/
cp writers/config/writer_configs/writer_chatgpt_test.yaml /tmp/chatgpt_test_configs/

# Activate virtual environment
cd writers && source .venv/bin/activate && cd ..

# Run all three tests in parallel, each writing to its own log
echo "Launching tests..."

# Test 1: Claude
python end_to_end_v0.1.py \
  --mock \
  --llm 1 \
  --rounds 3 \
  --num-readers 1 \
  --data-dir data/claude_test \
  --config-dir /tmp/claude_test_configs \
  > logs/claude_test_$(date +%Y%m%d_%H%M%S).log 2>&1 &
PID1=$!
echo "  ✓ Test 1 (Claude) started (PID: $PID1)"

# Test 2: Gemini
python end_to_end_v0.1.py \
  --mock \
  --llm 1 \
  --rounds 3 \
  --num-readers 1 \
  --data-dir data/gemini_test \
  --config-dir /tmp/gemini_test_configs \
  > logs/gemini_test_$(date +%Y%m%d_%H%M%S).log 2>&1 &
PID2=$!
echo "  ✓ Test 2 (Gemini) started (PID: $PID2)"

# Test 3: ChatGPT
python end_to_end_v0.1.py \
  --mock \
  --llm 1 \
  --rounds 3 \
  --num-readers 1 \
  --data-dir data/chatgpt_test \
  --config-dir /tmp/chatgpt_test_configs \
  > logs/chatgpt_test_$(date +%Y%m%d_%H%M%S).log 2>&1 &
PID3=$!
echo "  ✓ Test 3 (ChatGPT) started (PID: $PID3)"

echo ""
echo "All tests launched. Waiting for completion..."
echo ""

# Wait for all to complete
wait $PID1
STATUS1=$?
echo "  ✓ Test 1 (Claude) completed with status $STATUS1"

wait $PID2
STATUS2=$?
echo "  ✓ Test 2 (Gemini) completed with status $STATUS2"

wait $PID3
STATUS3=$?
echo "  ✓ Test 3 (ChatGPT) completed with status $STATUS3"

echo ""
echo "================================================================================"
echo "All Tests Complete!"
echo "================================================================================"
echo ""
echo "Results:"
echo "  - Claude test:   Exit code $STATUS1"
echo "  - Gemini test:   Exit code $STATUS2"
echo "  - ChatGPT test:  Exit code $STATUS3"
echo ""
echo "Data directories:"
echo "  - data/claude_test/"
echo "  - data/gemini_test/"
echo "  - data/chatgpt_test/"
echo ""
echo "Log files:"
echo "  - logs/claude_test_*.log"
echo "  - logs/gemini_test_*.log"
echo "  - logs/chatgpt_test_*.log"
echo ""

# Cleanup temp directories
rm -rf /tmp/claude_test_configs
rm -rf /tmp/gemini_test_configs
rm -rf /tmp/chatgpt_test_configs

exit 0
