Popis projektu

Program slouži k extrakci výsledků voleb ze zadaného odkazu a zapsání indormací do csv souboru.
Jako oddělovač polí v soubou csv je použit znak „=“.

Instalace potřebných knihoven

Program vyžaduje před spuštěním instalaci použitých knihoven třetích stran. Seznam knihoven je v přiloženém souboru requirements.txt.
Instalace knihoven se provede spuštěním tohoto příkazu v příkazovém řádku: 
pip install -r requirements.txt

Předpoklady použití programu

Program je nutné spustit se 2 zadanými systémovými argumenty. První argument je odkaz na vybraný územní celek, druhý argument je název výstupního csv souboru. Pokud se nezadá platný odkaz nebo korektní název souboru, akce nebude provedena a bude vypsána odpovídající
výzva k zadání správného vstupu. Pokud se zadá název souboru, který již v aktuálním pracovním adresáři existuje, výstup také nebude zpracován, aby nedošlo k nechtěnému přepsání souboru.

Ukázka spuštění

Zadáním příkazu níže se provede stažení dat pro obec Benešov a zapsání výstupu do souboru
benesov.csv.

python projekt3.py " https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" "benesov.csv"




Snímek části výstupu:
