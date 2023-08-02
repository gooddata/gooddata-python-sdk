python3 json_builder.py
echo "Trying to remove existing docs"
rm -r ../../docs/content/en/docs/api-reference/sdk
rm -r ../../docs/content/en/docs/api-reference/catalog
python3 python_ref_builder.py ./data.json ../../docs/content/en/docs/api-reference --json_start_path sdk catalog --url_root "/docs/api-reference"
cp data.json links.json ../../docs/layouts/shortcodes/data/
