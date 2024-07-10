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
W wersji 2.0 aplikacji planowane jest dodanie mozliwości podziału płaszczyzn poprzez zdefiniowaną siatkę oraz uwzględnianie zacienienia (przez numeryczny model pokrycia terenu oraz sąsiadujące obiekty 3D).

### Built With

Aplikacja wykorzystuje biblioteki: 
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

Aby zainstalować plugin należy otworzyć okno Processing Toolbox i otworzyć skrypt:
![image](https://github.com/MateuszIlba/SolarGIS/assets/50248287/ea75490a-5680-4c1b-901a-20a9de189bec)
Skrypt aplikacji będzie widoczny w zakładce Scripts:
![image](https://github.com/MateuszIlba/SolarGIS/assets/50248287/8dfe83c6-0e0f-42d2-bc25-a99125849560)
Po dodaniu skrytpu Python można uruchomić aplikację klikając dwyukrotnie na nazwę SolarGIS

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact
Mateusz Ilba - ilbam@uek.krakow.pl
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Acknowledgments
This plugin present the result of the Project no 019/ZII/2024/POT financed from the subsidy granted to the Krakow University of
Economics
<p align="right">(<a href="#readme-top">back to top</a>)</p>
