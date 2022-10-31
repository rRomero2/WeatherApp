# WeatherApp
<h3>Summary</h3>
<strong>General overview</strong>: Basic HTML/CSS website providing weather data, using Flask framework

I used a Flask framework to create a simple website, linking main Python code and HTML. User input through the use of HTML forms was retrieved and sent to the main code.
Weather data was retrieved by using <em>OpenWeatherAPI</em> based on the information the user inputted into the form. Basic HTML/CSS was used to format the webpage.

I already had a foundation in Python prior to this, so this was less about learning Python and more about learning how to use APIs and integrating Python with HTML through Flask to create a very basic website. In the span of a week, I learned enough Flask, HTML, and CSS to put together this rudimentary website. It is far from aesthetically pleasing, but with these basics I am looking forward to learn more and improve to make even bigger and better sites. 😀

<strong>Skills learned for this project</strong>: APIs, Flask framework, HTML/CSS

<h3>Details and screenshots</h3>

<h4> Search city page </h4>

<img width="1434" alt="Screen Shot 2022-10-30 at 8 02 21 PM" src="https://user-images.githubusercontent.com/98653307/198908516-25c1f26b-bcc9-4cac-9c4f-e931e46d1092.png">
<img width="1431" alt="Screen Shot 2022-10-30 at 8 02 31 PM" src="https://user-images.githubusercontent.com/98653307/198908536-3c455916-c7c6-420d-9642-565e6d61c3aa.png">
<em> Form has inputs to search by city or zip code, and fields to enter the required information.
  There is also the option to change the default units from metric to imperial or kelvin.
  The user has the opportunity to pick what information they would like to display. Current temperature must always be displayed, but everything else is optional.
  Finally, they can save all the previous searches to be able to compare between different cities, or simply discard all previous searches.
  Disclaimer: when searching by city, the program automatically displays the information for the top result (eg. "London" will display weather information for London, UK) </em>
 <br><br><br>
<img width="1430" alt="Screen Shot 2022-10-30 at 8 02 51 PM" src="https://user-images.githubusercontent.com/98653307/198908660-2c6d43f8-e120-48a5-af14-8d9c91b089d2.png">
<em> When scrolling over possible weather information to display, the name will get a pale yellow hover area behind it that disappears once the cursor moves off. </em>
<br><br><br>

<img width="1432" alt="Screen Shot 2022-10-30 at 8 03 27 PM" src="https://user-images.githubusercontent.com/98653307/198908740-3f8893a3-3d0a-46f4-84da-ec11db6b208a.png">
<em>If one of the required fields are not filled out (eg. no city name when searching by city, no zip/country code when searching by country, etc), the form will reload and a message will flash at the top of the screen warning the user that they must fill out the required information.</em>
<br>

<h4>Weather page</h4>

<img width="1431" alt="Screen Shot 2022-10-30 at 8 03 09 PM" src="https://user-images.githubusercontent.com/98653307/198908860-3927098d-c96c-4041-aece-fcfc32d9f1a5.png">
<em>The weather information will be displayed on the front page once the user submits their form. City name, cordinates, a weather icon and the current temperature will always be displayed, plus any additional information that they selected.
