## WooCommerce PDF: Backoffice App to generate PDFs given an order

## Linux

1. Create virtual enviroment and activate it

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Install [pango](https://pango.gnome.org/) (Required for [weasyprint](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html) )
```bash
sudo apt-get install -y libsdl-pango-dev
```