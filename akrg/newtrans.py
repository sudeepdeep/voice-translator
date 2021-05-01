from translate import Translator
from flask import Flask,render_template,request
import os
import speech_recognition as sr
from google_trans_new import google_translator

app = Flask(__name__)

@app.route('/lang',methods = ['GET','POST'])
def lang():
	if request.method == "POST":


		src = request.form['src']
		dest = request.form['dest']
		dest1 = "en"

		org_text = request.form['text']

		translate = Translator(from_lang = src, to_lang = dest1)

		con_text = translate.translate(org_text).lower()

		print(con_text)

		path = "static/"

		with os.scandir(path) as files:
			for file in files:

				if file.name == con_text:
					folder = file.name
					filename = file.name + dest
					new_path = path + f"{file.name}/"
					with os.scandir(new_path) as records:
						for i in records:
							if i.name.endswith(".mp3") and i.is_file():
								if i.name == filename+".mp3":
									filepath = f"{filename}.mp3"
									full_file = f"{folder}/{filepath}"


									return render_template('res.html', filename = full_file)




	return render_template('lang.html')


@app.route('/voice',methods = ['GET','POST'])
def voice():
	if request.method == "POST":
		src = request.form['src']
		dest = request.form['dest']
		r = sr.Recognizer()
		with sr.Microphone() as source:
			r.adjust_for_ambient_noise(source)
			audio = r.listen(source)
			text = r.recognize_google(audio)
			translator = google_translator()
			trans_text = translator.translate(text,lang_src = src,lang_tgt = "english").lower()
		path = "static/"
		with os.scandir(path) as a:
			for b in a:
				if b.name == trans_text:
					mod_path = f"static/{b.name}/"
					filename = b.name + dest
					with open(mod_path) as m:
						for n in m:
							if n.name.endswith('.mp3') and n.is_file():
								if n.name == filename+".mp3":
									fname = filename + ".mp3"
									folder = f"{b.name}/{fname}"
									return render_template('res.html',filename = folder)

	return render_template('voice.html')

if __name__ == '__main__':
	app.run(debug = True)

