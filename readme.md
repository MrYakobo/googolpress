# googolpress: transform a google doc into a static site

![googolpress logo](./assets/logo.svg)

usecase: Emerald Legacy documentation is in a massive google doc, that is slowed down by just visiting the document. it introduces unneccessary friction. this tool can run on a cron job and update a live website from a Google Doc. be warned, google seems to throttle the export api sometimes

## usage

You can use the tool with a google docs url directly:

```bash
# with url
./make_site.py "https://docs.google.com/document/d/1GP3hX7KoZTutrrdv9h02oUTdJS-bPJwsG6Gl3_7M3lA/edit?usp=sharing"
wrote site files to site/
```

You can also predownload the zip file from `https://docs.google.com/document/u/0/export?format=zip&id=$ID&includes_info_params=true&usp=sharing&cros_files=false` (replace $ID with your document id)

```bash
# with local zip file
wget -o site.zip "https://docs.google.com/document/u/0/export?format=zip&id=$ID&includes_info_params=true&usp=sharing&cros_files=false"
./make_site.py site.zip
```