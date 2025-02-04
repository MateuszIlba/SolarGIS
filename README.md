<a name="readme-top"></a>
# SolarGIS

![k](https://github.com/MateuszIlba/SolarGIS/assets/50248287/d9d6daaa-2d57-4d85-86fd-9b65845d82c4)

## About The Project

This QGIS plugin calculates solar irradiance based on arbitrary 3D geometry and EPW weather data. Built on the open-source QGIS platform, version 1.0 incorporates solar radiation adjustments for surface tilt and azimuth. Additionally, the plugin computes the true surface area of a given 3D plane.<br>
This application is characterized by the following key features:<br>
<ul>
  <li>determination of real-time solar irradiation on a given plane using meteorological data (EPW)</li>
  <li>computationally scalable across an arbitrary number of planes</li>
  <li>when calculating solar radiation, corrections should be made for the three components: direct, diffuse, and reflected</li>
  <li>the results can be visualized in any way desired, and the calculations can be exported to any file format supported by QGIS</li>
</ul><br>


### Built With

The application utilizes software and libraries: 
<ul>
<li>QGIS</li>
<li>NumPy</li>
<li>Pandas</li>
</ul>
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started
### Prerequisites

To run this application, you need to have QGIS version 3.34 or later installed on your computer. You can download the latest version from <a href="https://qgis.org/en/site/forusers/download.html"> this website </a>

### Installation

To install the plugin, open the Processing Toolbox window and open the script:<br><br>
![image](https://github.com/MateuszIlba/SolarGIS/assets/50248287/ea75490a-5680-4c1b-901a-20a9de189bec)<br><br>
The application script can be found in the Scripts tab:<br><br>
![image](https://github.com/MateuszIlba/SolarGIS/assets/50248287/8dfe83c6-0e0f-42d2-bc25-a99125849560)<br><br>
Once the Python script has been added, the application can be launched by double-clicking the SolarGIS executable
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

This application calculates solar radiation on arbitrary planes defined in a 3D vector file, compatible with QGIS as polygon layers. Version 1.0 has undergone validation against established commercial software for solar radiation analysis on inclined planes under direct solar radiation. Currently, results for vertical planes may be inaccurate due to polygon topology and the winding order of vertices, which affects the calculation of the polygon's normal vector.

Upon launching the application, the graphical user interface (GUI) is displayed, enabling users to configure the analysis parameters:<br><br>
![image](https://github.com/MateuszIlba/SolarGIS/assets/50248287/6abd2d56-1498-4245-90d5-5f45b2aa501d)<br><br>
Main application settings:<br><br>
 `Input layer` - The layer within which the analysis will be performed, can only use the selected elements by checking the box under the input layer<br><br>
 `ID field` - The unique ID field in the attribute table facilitates the potential integration of results with source data. The selected IDs will be appended to the objects undergoing processing<br><br>
 `EPW file` - The EPW file, which will be used as a source of model average annual solar radiation, should be loaded. The EPW file should be loaded from a location as close as possible to the objects being analyzed. EPW files for locations around the world can be downloaded, for example, from the website <a href="https://www.ladybug.tools/epwmap/">ladybug.tools/epwmap</a><br><br>
 `Ground albedo` - Solar reflectance of the ground surface in the vicinity of the analyzed location. This dimensionless value ranges from 0 to 1, where higher values indicate greater reflectivity. A default value of `0.2` is representative of an urban environment<br><br>
 `Time Zone` - The time zone of the location under analysis, expressed as an integer between -12 and 12 inclusive, corresponding to the respective time zone <br><br>
 The user has the option to save data from preliminary calculations to the output file, among options `azimuth`, `tilt angle` and `real 3D area`. By default, all information is saved. <br><br>
 `Output layer` - The corrected solar insolation layer is, by default, saved as a temporary layer.  Alternatively, you can specify a spatial file or database (compatible with QGIS) for persistent storage. The layer will be automatically added to the map upon completion of the calculations<br>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Example of how the application works

To conduct an annual solar radiation analysis, open the sample 3D building dataset (layer: several_buildings). You will also require an EPW (EnergyPlus Weather) file containing meteorological data from the weather station nearest to the area of interest. A suitable EPW file, compatible with the spatial data, is located in the example_dataset directory. Additional EPW files can be obtained through an online search: <a href="https://www.ladybug.tools/epwmap/"> https://www.ladybug.tools/epwmap/ </a>

![dataset](https://github.com/user-attachments/assets/7420b8b6-7a99-4e11-b43e-4abc5282c807)

Note: If you are using the sample dataset with the complete 3D model, you must disable the object geometry filter:

![ustawianiepliku](https://github.com/user-attachments/assets/bd1c209d-1b28-42bc-862d-144217665bdd)
![ustawianiepliku2](https://github.com/user-attachments/assets/fae23552-1119-48da-bad2-a90d1a222350)

This option must be enabled to ensure correct geometry for vertical objects. QGIS performs geometry checks based on 2D XY coordinates. If a perfectly vertical rectangular polygon is exported without this option enabled, QGIS will only detect two distinct points, which are insufficient to define a 2D polygon, resulting in a geometry error. To ensure a complete export of all calculated data, verify that the SolarGIS tool is configured appropriately:

![ustawianiepliku3](https://github.com/user-attachments/assets/b5f11c20-4055-40aa-acf6-30779f65a770)

After configuring the settings, click the Run button to execute the process. The results can be visualized in either 2D or 3D. For enhanced 3D visualization, it is recommended to use the  <a href="https://plugins.qgis.org/plugins/Qgis2threejs/"> Qgis2threejs </a> plugin.

![wynik](https://github.com/user-attachments/assets/9042c79b-2bca-4bb4-b51f-79f1de279b2c)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Planned software updates and enhancements

We invite you to collaborate with us on improving this tool. We are currently planning to add several new features, including:
<ul>
<li>Optimizing the topology of ideally vertical objects and validating the accuracy of their surface normals</li>
<li>uShading analysis is performed using a digital terrain model (DTM) and 3D models of surrounding objects</li>
<li>Implement a feature to allow users to specify the time range for analysis, with options for daily, monthly, or annual data aggregation</li>
<li>The ability to divide planes using a defined grid will be added to enhance the accuracy of analyses</li>
</ul>

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
