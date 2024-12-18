# transform a google doc into a full fledged website

usecase: Emerald Legacy documentation is in a massive google doc, that is slowed down by just visiting the document. it introduces unneccessary friction. this tool can run on a cron job and update a live website from a Google Doc.

## usage

```bash
./make_site.py "https://docs.google.com/document/u/0/export?format=html&id=1tfVTjH7erMEp7yKbpdDhucwOCXogjO2Ut32G4TNR7vg&token=AC4w5ViITN6Ftq0YudVEJTmfIeowjFbDRg%3A1734437163547&includes_info_params=true&usp=sharing&cros_files=false" -o out.html
```