import pathlib
path = pathlib.Path('backend/app/services/weather_service.py')
text = path.read_text(encoding='utf-8')
sys_out = open(1, 'w', encoding='utf-8', errors='replace')
sys_out.write(text)
