Spring Data - Redis Twitter Example
===================================

An improved Java implementation of the [Redis Twitter Clone](http://redis.io/topics/twitter-clone) using Spring Data. Tutorial available [here](http://static.springsource.org/spring-data/data-keyvalue/examples/retwisj/current/)


##Build
-----
The project creates a WAR file suitable for deployment in a Servlet 2.5 container (such as Tomcat). It uses [Gradle](http://gradle.org/) as a build system.
Simply type:

      gradlew build

##To run locally

start redis

      $REDIS_HOME/src/redis-server

deploy the app

      gradle tomcatRun

Open browser to view the app [http://localhost:8080/retwisj](http://localhost:8080/retwisj)
      
##To deploy to Cloud Foundry
Please ensure that you have have defined a Redis service called **ratings-redis**. If deploying to [Pivotal Web Services]  (http://run.pivotal.io) free Redis service is available from the Marketplace.

      cf push
      

