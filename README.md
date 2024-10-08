<h1>SearchGPT</h1>

<p>SearchGPT is a python script that uses SerpAPI, Browserless and OpenAI to search and summarize results including citations.</p>

[Live version can be tested here](https://seedgularity-searchgpt-st-main-xsacfx.streamlit.app/)

![image](https://github.com/seedgularity/SearchGPT/assets/131738679/2f36bb28-9863-41ca-bbad-4835e78135d6)

<h2>Updates</h2>

**Update 2024-09-17**

- Streamlit version not working as OAI API key missing
- Download it locally and add OAI API key

**Update 2023-06-18**

- Streamlit version has been updated and now running faster. 
- Number of searches has been increased to provide better accuracy in Streamlit version.
- Timer for OpenAI added to Streamlit version.

**Update 2023-06-17**

- Streamlit version has been added.

<h2>Installation</h2>

<p>For console version, add API codes in .env file. For Streamlit version, add API codes to secrets.toml.</p>

<p>Install the requirements and run the main.py.</p>

```sh  
$ pip install -r requirements.txt
$ python main.py
```

Streamlit version has been added as st_main.py. To run streamlit version, run the following command:

```sh
$ streamlit run st_main.py
```

<h2>Licence</h2>

MIT © [Seedgularity](https://github.com/seedgularity)
