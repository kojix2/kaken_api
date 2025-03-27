#!/bin/bash

# 対象のExcelファイル一覧
files=(
  "kaken_definition/KAKEN_API_parameters_document_En.xlsx"
  "kaken_definition/KAKEN_API_parameters_document_Ja.xlsx"
  "kaken_definition/KAKEN_XML_definition_document_En.xlsx"
  "kaken_definition/KAKEN_XML_definition_document_Ja.xlsx"
  "kaken_definition/KAKEN_researcher_JSON_definition_document_En.xlsx"
  "kaken_definition/KAKEN_researcher_JSON_definition_document_Ja.xlsx"
)

# 出力ディレクトリ
output_dir="assets/kaken_definition"
mkdir -p "$output_dir"

# 各ファイルに対して処理
for file in "${files[@]}"; do
  echo "Processing $file..."
  
  # JSONメタデータを取得
  metadata=$(qsv excel --metadata json "$file")
  
  # シート情報を jq で抽出
  sheet_count=$(echo "$metadata" | jq '.sheet_count')
  for i in $(seq 0 $((sheet_count - 1))); do
    # シート名を取得してファイル名として使えるよう整形
    sheet_name=$(echo "$metadata" | jq -r ".sheet[$i].name" | sed 's/[ \/]/_/g')
    base_filename=$(basename "$file" .xlsx)
    output_file="${output_dir}/${base_filename}_${sheet_name}.txt"
    
    # シートをCSV出力→table整形→保存
    qsv excel -s "$sheet_name" "$file" | qsv table -o "$output_file"
    echo "  -> Saved $output_file"
  done
done

echo "Done."
