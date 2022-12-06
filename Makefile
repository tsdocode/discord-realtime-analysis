install:
	pip install -r requirements.txt & pip install -e ./
bot:
	python discord_analysis/discord/bot.py
dashboard:
	streamlit run discord_analysis/app/app.py
run:
	make bot & make dashboard