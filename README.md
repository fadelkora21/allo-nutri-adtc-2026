# ALLO NUTRI Feed Formulator — prototype ADTC 2026

Prototype hors ligne de formulation d'aliments pour poulets. Le moteur utilise une optimisation linéaire au moindre coût; le module d'explication peut fonctionner avec un modèle GGUF local via `llama.cpp`, sans cloud ni API.

## Lancer

```bash
python3 -m pip install -r requirements.txt
python3 app.py
```

Ouvrir `http://127.0.0.1:8080`.

## Ajouter le LLM local

Installer `llama.cpp`, choisir un petit modèle instruct GGUF dont la licence permet la redistribution et définir :

```bash
export LLAMA_CLI=/chemin/vers/llama-cli
export ALLO_NUTRI_MODEL=/chemin/vers/model.gguf
python3 app.py
```

Sans modèle, l'application utilise une explication déterministe hors ligne. Le moteur mathématique reste toujours la source des quantités; le LLM ne calcule pas la ration.

Pour la structure officielle ADTC, `bash download_model.sh` télécharge le modèle exactement au chemin déclaré dans `metadata.json`. Le script est idempotent et vérifie l'en-tête GGUF. `setup_model.sh` sert au développement local et compile aussi `llama.cpp`. Vérifier la licence actuelle du modèle avant toute redistribution. Le fichier GGUF n'est pas inclus dans cette archive.

## Benchmark préliminaire

Après avoir défini `LLAMA_CLI` et `ALLO_NUTRI_MODEL`, lancer `python3 benchmark.py`. Le résultat est écrit dans `benchmark_results.json`. Pour la candidature, remplacer ce préflight par les résultats de l'outil officiel ADTC.

## Préflight de soumission

Compléter dans `metadata.json` le Team ID DevPost, l'e-mail d'inscription et le nom d'utilisateur GitHub, puis lancer `python3 validate_submission.py`. Le validateur refuse explicitement toute soumission qui conserve ces champs incomplets.

## Tester

```bash
python3 -m unittest -v
```

## Avertissement

Les données d'ingrédients sont indicatives et servent au prototype. Une utilisation terrain exige des analyses locales, la validation des besoins selon la souche et l'âge, ainsi que la supervision d'un nutritionniste animal.
