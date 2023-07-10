python3 json_builder.py
rm -r ../../docs/content/en/docs/sdk
python3 python_ref_builder.py ./data.json ../../docs/content/en/docs --json_start_path sdk --url_root "/docs"
