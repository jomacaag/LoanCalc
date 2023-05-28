 
# My Personal Portfolio Website (PPW)
This is my personal webiste portfolio to showcase my multi-disiplinary projects in a easy-to-navigate, easy-to-search, and easily-presentable format.  

## Run in Docker 

Clone the project  

~~~bash  
  git clone https://github.com/jomacaag/PPW
~~~

Go to the project directory  

~~~bash  
  cd PPW
~~~

Initialize dependencies in pyhton vitrual enviroment  

~~~bash  
pip install virtualenv
virtualenv venv
source venve/bin/activate
pip install -r requirements.txt
~~~

Initialize databases
~~~bash
flask initdb
~~~

Start the server  

~~~bash  
flask run
~~~
