#!/bin/bash
javac -cp $(hadoop classpath) TestIO.java
java -cp .:$(hadoop classpath) TestIO
