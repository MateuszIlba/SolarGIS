<a name="readme-top"></a>
# SolarGIS

![k](https://github.com/MateuszIlba/SolarGIS/assets/50248287/d9d6daaa-2d57-4d85-86fd-9b65845d82c4)

## About The Project

Aplikacja ma na celu realizację obliczeń nasłonecznienia na podstawie dowolnych danych przestrzennych 3D oraz danych pogodowych (w formacie EPW) w środowisku QGIS. Aplikacja działa w środowisku otwartego oprogramowania QGIS. W wersji 1.0 aplikacji stosowane są korekcje nasłonecznienia uwzględniające pochylenie płaszczyzny i jej azymut. Aplikacja umożliwia również obliczenie realnej powierzchni danej płaszczyzny 3D. <br>
Główne cechy aplikacji:<br>
<ul>
  <li>obliczanie realnego nasłonecznienia płaszczyzny na podstawie danych pogodowych (EPW)</li>
  <li>skalowalność obliczeń dla dowolnej liczby płaszczyzn</li>
  <li>uwzględnianie w obliczeniach korekcji dla trzech składowych nasłonecznienia: bezpośredniego, rozproszonego oraz odbitego</li>
  <li>możliwość dowolnej wizualizacji wyników a trakże możliwość eksportu obliczeń do dowolnego pliku obsługiwanego przez QGIS</li>
</ul><br>
W wersji 2.0 aplikacji planowane jest dodanie mozliwości podziału płaszczyzn poprzez zdefiniowaną siatkę w celu zagęszczenia dokładności analizy oraz uwzględnianie zacienienia (przez numeryczny model pokrycia terenu oraz sąsiadujące obiekty 3D).

### Built With

Aplikacja wykorzystuje oprogramowanie i biblioteki: 
<ul>
<li>QGIS</li>
<li>NumPy</li>
<li>Pandas</li>
</ul>
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started
### Prerequisites

W celu uruchomienia apllikacji wymagana jest instalacja aplikacji QGIS w wersji 3.34 lub nowszej. Najnowszą wersję można pobrać <a href="https://qgis.org/en/site/forusers/download.html">z tej strony</a>

### Installation

Aby zainstalować plugin należy otworzyć okno Processing Toolbox i otworzyć skrypt:<br><br>
![image](https://github.com/MateuszIlba/SolarGIS/assets/50248287/ea75490a-5680-4c1b-901a-20a9de189bec)<br><br>
Skrypt aplikacji będzie widoczny w zakładce Scripts:<br><br>
![image](https://github.com/MateuszIlba/SolarGIS/assets/50248287/8dfe83c6-0e0f-42d2-bc25-a99125849560)<br><br>
Po dodaniu skrytpu Python można uruchomić aplikację klikając dwyukrotnie na nazwę SolarGIS
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

Po otwarciu aplikacji uruchamia się GUI w którym można ustawić parametry analizy:<br><br>
![image](https://github.com/MateuszIlba/SolarGIS/assets/50248287/6abd2d56-1498-4245-90d5-5f45b2aa501d)<br><br>
Główne ustawienia aplikacji:<br><br>
 `Input layer` - warstwa w obrębie której będzie odbywała się analiza, można użyć tylko zaznaczonych elementów zaznaczając pole wyboru pod warstwą wejściową<br><br>
 `ID field` - pole w tabeli atrybutów z unikalnym ID - ma na celu ewentualne złączenie wyników z danymi źródłowymi - wybrane ID zostaną dopisane do obiektów podlegających processingowi<br><br>
 `EPW file` - plik EPW który będzie wykorzystywany jako źródło o modelowym średniorocznym nasłonecznieniu. Należy wczytać plik EPW z lokalizacji możliwie jak najbliższej obiektom podlegającym analizie. Pliki EPW dla lokalizacji dla całego świata można pobrać np. z strony <a href="https://www.ladybug.tools/epwmap/">ladybug.tools/epwmap</a><br><br>
 `Ground albedo` - poziom odbicia promieni słonecznych od podłoża wokół analizowanej lokalizacji. Wartość powinna zawierać się w wartościach od 0 do 1, im większa wartość tym większe odbijanie promieniowania słonecznego. Domyślna wartość `0.2` reprezentuje odbicie szacowane dla obszaru miejskiego<br><br>
 `Time Zone` - strefa czasowa dla analizowanej lokalizacji, wartość od -12 do 12 w zależności od strefy czasowej <br><br>
 Użytkownik może wybrać, czy zapisać dane pochodzące z wstępnych obliczeń do wynikowego pliku, między innymi `azimuth`, `tilt angle` oraz `real 3D area`. Domyślnie zapisywane są wszystkie informacje. <br><br>
 `Output layer` - wynikowa warstwa po korekcji nasłonecznienia, domyślnie wynik zapisywany jest jako warstwa tymczasowa, można zdefiniować zapis wyniku do określonego pliku warstwy przestrzennej lub bazodanowej (obsługiwanej przez QGIS). Warstwa zostanie automatycznie dodana do mapy po przeprowadzeniu obliczeń.<br>
 
###Example


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License
Distributed under the GNU General Public License v2.0. See file LICENSE for more information.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact
Mateusz Ilba - ilbam@uek.krakow.pl
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Acknowledgments
This plugin present the result of the Project no 019/ZII/2024/POT financed from the subsidy granted to the Krakow University of
Economics
<p align="right">(<a href="#readme-top">back to top</a>)</p>
