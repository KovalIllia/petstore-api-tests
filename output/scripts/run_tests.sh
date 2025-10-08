#!/bin/bash

set -e

BASE_DIR="./output/allure"
RESULTS_DIR="$BASE_DIR/allure-results"
REPORT_DIR="$BASE_DIR/allure-report"
HISTORY_DIR="$BASE_DIR/history"

echo "🚀 Запуск Allure з правильною історією..."

# Створюємо директорії
mkdir -p "$RESULTS_DIR" "$HISTORY_DIR"

# Очищаємо результати, але зберігаємо історію
rm -rf "$RESULTS_DIR"/* "$REPORT_DIR"

echo "📊 Перевірка історії..."
if [ -d "$HISTORY_DIR" ] && [ "$(ls -A $HISTORY_DIR)" ]; then
    echo "✅ Знайдено існуючу історію"
    # Копіюємо історію до результатів для Allure
    cp -r "$HISTORY_DIR" "$RESULTS_DIR/" 2>/dev/null || true
else
    echo "🆕 Створюємо нову історію"
fi

# Запускаємо тести
echo "🧪 Запуск тестів..."
pytest --alluredir="$RESULTS_DIR" -v --tb=short

# Перевіряємо результати
if [ ! -d "$RESULTS_DIR" ] || [ -z "$(ls -A $RESULTS_DIR)" ]; then
    echo "❌ Немає результатів тестів!"
    exit 1
fi

echo "📈 Генерація Allure звіту..."
# Генеруємо звіт - Allure автоматично оновить історію
allure generate "$RESULTS_DIR" \
    --clean \
    -o "$REPORT_DIR"

# Тепер копіюємо оновлену історію з звіту назад
if [ -d "$REPORT_DIR/history" ]; then
    echo "💾 Оновлення локальної історії..."
    rm -rf "$HISTORY_DIR"/*
    cp -r "$REPORT_DIR/history"/* "$HISTORY_DIR/" 2>/dev/null

    # Перевіряємо чи заповнились файли історії
    echo "🔍 Перевірка оновленої історії:"
    for history_file in "$HISTORY_DIR"/*.json; do
        if [ -f "$history_file" ]; then
            file_size=$(stat -f%z "$history_file" 2>/dev/null || stat -c%s "$history_file" 2>/dev/null || echo "0")
            if [ "$file_size" -gt 100 ]; then
                echo "   ✅ $(basename "$history_file"): $file_size bytes"
            else
                echo "   ⚠️  $(basename "$history_file"): $file_size bytes (малий розмір)"
            fi
        fi
    done
fi

echo "🌐 Відкриття звіту..."
allure open "$REPORT_DIR"