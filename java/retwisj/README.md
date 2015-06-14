Spring Data - Redis Twitter Example
===================================

An improved Java implementation of the [Redis Twitter Clone](http://redis.io/topics/twitter-clone) using Spring Data. Tutorial available [here](http://static.springsource.org/spring-data/data-keyvalue/examples/retwisj/current/)


##Build
-----
The project creates a WAR file suitable for deployment in a Servlet 2.5 container (such as Tomcat). It uses [Gradle](http://gradle.org/) as a build system.
Simply type:

      gradlew build

##To run locally
Start up an instance of the redis server, deploy your WAR and point your browser to (for the typical setup) [http://localhost:8080/retwisj](http://localhost:8080/retwisj)

start redis

      $REDIS_HOME/src/redis-server

deploy the app

      gradle tomcatRun
      
##To deploy to Cloud Foundry
Please ensure that you have have defined a Redis service called **ratings-redis**

      cf push
      

