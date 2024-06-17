import pathlib
import google.generativeai as genai

API_KEY = "AIzaSyBiK5CFXyVeEvnGNYpzr5M6lPhtEPKibKE"

generation_config = {
	'temperature':0,
	"top_p":1,
	"top_k":1,
	"max_output_tokens":400,
}

safety_settings = [
	{
		"category": "HARM_CATEGORY_HARASSMENT",
		"threshold": "BLOCK_NONE"
	},
	{
		"category": "HARM_CATEGORY_HATE_SPEECH",
		"threshold": "BLOCK_NONE"
	},
	{
		"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
		"threshold": "BLOCK_NONE"
	},
	{
		"category": "HARM_CATEGORY_DANGEROUS_CONTENT",
		"threshold": "BLOCK_NONE"
	}
]

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro', generation_config=generation_config, safety_settings=safety_settings)

def label_gen(filename):
	label = ''
	with open(filename, 'r') as f:
		html_code = f.read()
		# Which site is this html code looks like? Explain it in short word\n" + html_code 
		query = "Could you guess the original URL of the html code?\n" + html_code 
		if len(query) > 30000:
			query = query[0:1000]
		try:
			response = model.generate_content(query)
			
			for chunk in response:
				if chunk.text != None:
					label = chunk.text
			if "http" not in label:
				label = "None"
		except:
			label = "None"

		print(label)
		return label


def main():
	files = [f for f in pathlib.Path().glob("html/*")]
	
	with open("label_result.txt", 'w') as file:
		for filename in files:
			test = str(filename).replace('html/','')
			file.write("{%s, %s}\n"%(test, label_gen(str(filename))))


if __name__ == "__main__":
	main()
