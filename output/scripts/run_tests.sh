#!/bin/bash

BASE_DIR="./output/allure"
RESULTS_DIR="$BASE_DIR/allure-results"
REPORT_DIR="$BASE_DIR/allure-report"
HISTORY_DIR="$BASE_DIR/history"

mkdir -p "$BASE_DIR" "$HISTORY_DIR"


if [ -d "$RESULTS_DIR" ]; then
    rm -rf "$RESULTS_DIR"
fi

if [ -d "$REPORT_DIR" ]; then
    rm -rf "$REPORT_DIR"
fi

mkdir -p "$RESULTS_DIR"

if [ -d "$HISTORY_DIR" ] && [ "$(ls -A $HISTORY_DIR)" ]; then
echo "Copying history from previous run..."
cp -r "$HISTORY_DIR" "$RESULTS_DIR/"
fi

echo "Running pytest, checking for test_result creation..."
pytest --alluredir="$RESULTS_DIR" -v

if [ -d "$RESULTS_DIR" ] && [ "$(ls -A $RESULTS_DIR)" ]; then
echo "Generating Allure report..."
allure generate "$RESULTS_DIR" --clean -o "$REPORT_DIR"
else
    echo "No test results were found to generate a report."
fi

if [ -d "$REPORT_DIR/history" ]; then
echo "Saving updated history..."
rm -rf "$HISTORY_DIR"
cp -r "$REPORT_DIR/history" "$HISTORY_DIR"
fi

allure open "$REPORT_DIR"

# Перевірка наявності test_result після запуску
if [ -d "test_result" ]; then
    echo "Warning: test_result folder was created at $(pwd)/test_result"
fi